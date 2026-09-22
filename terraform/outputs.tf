output "api_url" {
  description = "Base URL of the application. Open this in a browser."
  value       = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.aws_region}.amazonaws.com/prod/"
}

output "cognito_domain" {
  description = "Cognito Managed Login domain"
  value       = "https://${var.cognito_domain_prefix}.auth.${var.aws_region}.amazoncognito.com"
}

output "cognito_client_id" {
  description = "Cognito App Client ID"
  value       = aws_cognito_user_pool_client.app_client.id
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = aws_cognito_user_pool.pool.id
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.employees.name
}

output "caller_arn" {
  description = "Your current AWS identity ARN (put this in the student employee record's Description field)"
  value       = data.aws_caller_identity.current.arn
}
