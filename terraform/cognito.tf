resource "aws_cognito_user_pool" "pool" {
  name = "${var.app_name}-user-pool"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = false
    require_uppercase = true
  }
}

# Public client, no secret, Authorization Code + PKCE (PKCE is enforced client-side
# by sending code_challenge/code_challenge_method to the /oauth2/authorize endpoint;
# Cognito requires it for public clients using the code grant).
resource "aws_cognito_user_pool_client" "app_client" {
  name         = "${var.app_name}-client"
  user_pool_id = aws_cognito_user_pool.pool.id

  generate_secret = false

  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_scopes                 = ["openid", "email", "profile"]

  callback_urls = [var.callback_url]
  logout_urls   = [var.callback_url]

  supported_identity_providers = ["COGNITO"]
  explicit_auth_flows          = ["ALLOW_USER_SRP_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]

  prevent_user_existence_errors = "ENABLED"
}

resource "aws_cognito_user_pool_domain" "domain" {
  domain       = var.cognito_domain_prefix
  user_pool_id = aws_cognito_user_pool.pool.id
}
