# ---------- Backend Lambda (needs DynamoDB read access) ----------

resource "aws_iam_role" "backend_lambda_role" {
  name = "${var.app_name}-backend-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Least privilege: only GetItem, only on this one table.
resource "aws_iam_role_policy" "backend_lambda_dynamodb" {
  name = "${var.app_name}-backend-dynamodb-policy"
  role = aws_iam_role.backend_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["dynamodb:GetItem"]
      Resource = aws_dynamodb_table.employees.arn
    }]
  })
}

resource "aws_iam_role_policy_attachment" "backend_lambda_logs" {
  role       = aws_iam_role.backend_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# ---------- UI Lambda (only needs to write CloudWatch logs) ----------

resource "aws_iam_role" "ui_lambda_role" {
  name = "${var.app_name}-ui-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ui_lambda_logs" {
  role       = aws_iam_role.ui_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
