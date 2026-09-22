variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Short name used as a prefix for all resources"
  type        = string
  default     = "hr-lookup"
}

# Must be globally unique across all of Cognito in this region, e.g. "hr-lookup-jsmith"
variable "cognito_domain_prefix" {
  description = "Unique prefix for the Cognito Hosted UI (Managed Login) domain"
  type        = string
}

# On the FIRST apply you won't know the API Gateway URL yet, so leave the default.
# After the first apply, copy the `api_url` output and re-apply with
#   terraform apply -var="callback_url=<api_url from output>"
# so Cognito is configured to allow redirects back to the real app URL.
variable "callback_url" {
  description = "URL Cognito redirects to after login (the app's own URL, ending in /)"
  type        = string
  default     = "https://example.com/"
}

variable "student_name" {
  description = "Your full name, stored in the student employee record"
  type        = string
}
