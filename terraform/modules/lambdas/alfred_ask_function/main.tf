data "aws_caller_identity" "current" {}

# Lambda Role
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}_ask-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda Policy
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}_ask-lambda-policy"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.knowledge_bucket}",
          "arn:aws:s3:::${var.knowledge_bucket}/*",
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "bedrock:InvokeModel"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Lambda Basic Execution Role
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

#####################################
# Lambda Function
#####################################

resource "aws_lambda_function" "alfred_ask_lambda" {
  function_name = "${var.project_name}_ask"
  handler       = "handlers.alfred_handler.lambda_handler"
  runtime       = var.runtime
  role          = aws_iam_role.lambda_role.arn

  filename         = "${path.root}/builds/${var.project_name}_ask.zip"
  source_code_hash = filebase64sha256("${path.root}/builds/${var.project_name}_ask.zip")

  layers = [aws_lambda_layer_version.common_dependencies.arn]
  depends_on = [null_resource.force_lambda_update,
    aws_lambda_layer_version.common_dependencies
  ]

  environment {
    variables = {
      KNOWLEDGE_BUCKET = var.knowledge_bucket
      MODEL_ID         = "arn:aws:bedrock:${var.aws_region}:${data.aws_caller_identity.current.account_id}:inference-profile/us.amazon.nova-lite-v1:0"
    }
  }
}

#####################################
# Lambda Layer
#####################################

resource "aws_lambda_layer_version" "common_dependencies" {
  filename            = "${path.root}/builds/python.zip"
  layer_name          = "${var.project_name}-common-deps"
  compatible_runtimes = [var.runtime]

  lifecycle {
    create_before_destroy = true
  }

  # 👇 Force new version on changes
  source_code_hash = filebase64sha256("${path.root}/builds/python.zip")
}

#####################################
# API Gateway Integration
#####################################

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.alfred_ask_lambda.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

resource "aws_apigatewayv2_integration" "alfred_ask_integration" {
  api_id                 = var.api_id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.alfred_ask_lambda.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "promoted_route" {
  api_id    = var.api_id
  route_key = "POST /ask"
  target    = "integrations/${aws_apigatewayv2_integration.alfred_ask_integration.id}"
}


#####################################
# Trigger a deployment
#####################################
resource "null_resource" "force_lambda_update" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "touch ${path.root}/builds/${var.project_name}_ask.zip"
  }
}
