variable "aws_region" {
  type    = string
  default = "us-west-1"
}

variable "environment" {
  type        = string
  description = "Deployment environment (e.g. dev, prod)"
  default     = "dev"
}

variable "s3_bucket_name" {
  type    = string
  default = "alfred-knowledge-bucket"
}

variable "lambda_function_name" {
  type    = string
  default = "AlfredLambda"
}

variable "project_name" {
  type    = string
  default = "alfred"
}

variable "runtime" {
  type    = string
  default = "python3.13"
}
