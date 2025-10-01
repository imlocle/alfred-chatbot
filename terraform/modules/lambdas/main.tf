module "ask_function" {
  source      = "./ask_function"
  environment = var.environment

  api_id                          = var.api_id
  api_execution_arn               = var.api_execution_arn
  project_name                    = var.project_name
  knowledge_bucket                = var.knowledge_bucket
  runtime                         = var.runtime
  aws_region                      = var.aws_region
  alfred_usage_tracker_table_arn  = var.alfred_usage_tracker_table_arn
  alfred_usage_tracker_table_name = var.alfred_usage_tracker_table_name
}
