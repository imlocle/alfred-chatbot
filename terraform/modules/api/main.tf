resource "aws_apigatewayv2_api" "this" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_headers = ["Content-Type", "X-Amz-Date", "Authorization"]
    allow_methods = ["OPTIONS", "POST"]
    allow_origins = ["http://localhost:5173", "https://imlocle.com", "https://imlocle.github.io"]
    max_age       = 3600
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.this.id
  name        = "$default"
  auto_deploy = true
}
