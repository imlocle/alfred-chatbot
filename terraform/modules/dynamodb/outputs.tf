output "alfred_usage_tracker_table_arn" {
  value = module.alfred_usage_tracker_table.dynamodb_table_arn
}

output "alfred_usage_tracker_table_name" {
  value = module.alfred_usage_tracker_table.dynamodb_table_id
}
