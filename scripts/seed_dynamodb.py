"""
Seed the employees DynamoDB table with sample data, including the
required student record.

Usage:
    python seed_dynamodb.py <table_name> "<Your Full Name>" "<your-aws-user-arn>"

Example:
    python seed_dynamodb.py hr-lookup-employees "Jane Smith" \\
        "arn:aws:iam::123456789012:user/jsmith"
"""
import sys
import boto3

def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    table_name, student_name, student_arn = sys.argv[1], sys.argv[2], sys.argv[3]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    employees = [
        {"EmployeeID": "1001", "Name": "Alice Chen", "Salary": 92000,
         "DateOfJoin": "2024-01-15", "Description": "Cloud Engineering employee"},
        {"EmployeeID": "1002", "Name": "Brian Okafor", "Salary": 78000,
         "DateOfJoin": "2023-06-01", "Description": "DevOps engineer"},
        {"EmployeeID": "1003", "Name": "Carla Mendes", "Salary": 105000,
         "DateOfJoin": "2022-03-20", "Description": "Senior Backend Engineer"},
        {"EmployeeID": "1004", "Name": "David Kim", "Salary": 88000,
         "DateOfJoin": "2025-02-10", "Description": "Frontend Engineer"},
        # Required student record
        {"EmployeeID": "1005", "Name": student_name, "Salary": 95000,
         "DateOfJoin": "2026-01-15", "Description": student_arn},
    ]

    for emp in employees:
        table.put_item(Item=emp)
        print(f"Inserted {emp['EmployeeID']} - {emp['Name']}")

if __name__ == "__main__":
    main()
