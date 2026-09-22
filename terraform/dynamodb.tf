resource "aws_dynamodb_table" "employees" {
  name         = "${var.app_name}-employees"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "EmployeeID"

  attribute {
    name = "EmployeeID"
    type = "S"
  }

  tags = {
    Project = var.app_name
  }
}
