output "alfred_ask_lambda_arn" {
  value = aws_lambda_function.alfred_ask_lambda.arn
}

output "alfred_ask_lambda_name" {
  value = aws_lambda_function.alfred_ask_lambda.function_name
}
