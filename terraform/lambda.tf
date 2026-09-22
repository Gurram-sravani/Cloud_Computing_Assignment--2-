data "archive_file" "backend_lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/backend/lambda_function.py"
  output_path = "${path.module}/build/backend_lambda.zip"
}

resource "aws_lambda_function" "backend" {
  function_name    = "${var.app_name}-backend"
  role             = aws_iam_role.backend_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.backend_lambda_zip.output_path
  source_code_hash = data.archive_file.backend_lambda_zip.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.employees.name
    }
  }
}

data "archive_file" "ui_lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/ui/lambda_function.py"
  output_path = "${path.module}/build/ui_lambda.zip"
}

resource "aws_lambda_function" "ui" {
  function_name    = "${var.app_name}-ui"
  role             = aws_iam_role.ui_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.ui_lambda_zip.output_path
  source_code_hash = data.archive_file.ui_lambda_zip.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      COGNITO_DOMAIN    = "https://${var.cognito_domain_prefix}.auth.${var.aws_region}.amazoncognito.com"
      COGNITO_CLIENT_ID = aws_cognito_user_pool_client.app_client.id
    }
  }
}
