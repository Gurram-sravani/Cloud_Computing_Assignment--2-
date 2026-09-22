import json
import os
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    path_params = event.get("pathParameters") or {}
    employee_id = path_params.get("id")

    if not employee_id:
        return _response(400, {"error": "Employee ID is required"})

    try:
        result = table.get_item(Key={"EmployeeID": employee_id})
    except Exception:
        return _response(500, {"error": "Internal server error"})

    item = result.get("Item")
    if not item:
        return _response(404, {"error": f"Employee {employee_id} not found"})

    body = {
        "employeeId": item.get("EmployeeID"),
        "name": item.get("Name"),
        "salary": _to_number(item.get("Salary")),
        "dateOfJoin": item.get("DateOfJoin"),
        "description": item.get("Description"),
    }
    return _response(200, body)


def _to_number(value):
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    return value


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }
