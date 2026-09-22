# Functional Specification – Serverless HR Lookup Application

**Student Name:** Sravani Gurram
**GitHub Repository URL:** https://github.com/Gurram-sravani/Cloud_Computing_Assignment--2-

## 1. Architecture Diagram

```
                        User Browser
                              |
                              | HTTPS
                              v
                       API Gateway REST API
                        /               \
                       /                 \
                  GET /              GET /employee/{id}
                    |                       |
                    v                       v
               UI Lambda             Cognito Authorizer
                    |                       |
             HTML/CSS/JavaScript            |
                                            v
                                      Backend Lambda
                                            |
                                       IAM Role
                                            |
                                            v
                                        DynamoDB
```

## 2. Authentication-Flow Diagram

```
Browser -> Cognito Managed Login -> User Authentication -> Authorization Code
        -> Token Exchange (PKCE) -> Cognito ID Token
        -> Authorization: Bearer <token> -> API Gateway
        -> Cognito Authorizer -> Backend Lambda
```

## 3. Deployed Resource Details

| Item | Value |
|---|---|
| API Gateway URL | https://ec0nt4zxta.execute-api.us-east-1.amazonaws.com/prod/ |
| Cognito Managed Login domain | https://hr-lookup-sravani.auth.us-east-1.amazoncognito.com |
| Cognito Client ID | 7ksoktbmg46oj2hhs26qvlmuio |
| Cognito User Pool ID | us-east-1_DJNvZ52aK |
| Cognito User Pool Subject UUID (sub) | 147844f8-a0b1-705a-28b6-ac3d0e54b2a0 |
| AWS Account ID | 329504364784 |
| Deploying IAM User ARN | arn:aws:iam::329504364784:user/saathi-deployer |

## 4. Test Evidence

### Test 1 – Application Access
The application UI loads successfully over HTTPS at the deployed API Gateway URL.
![Test 1 - Application Access](screenshots/test1-app-access.png)

### Test 2 – User Authentication
Cognito Managed Login page, showing the OAuth 2.0 authorization request (response_type=code, client_id, redirect_uri) and a valid user signing in.
![Test 2 - Cognito Login](screenshots/test2-cognito-login.png)

### Test 3 – Valid Employee Lookup
Searching Employee ID `1001` returns the complete record (Employee ID, Name, Salary, Date of Join, Description).
![Test 3 - Valid Lookup](screenshots/test3-valid-lookup.png)

### Test 4 – Student Employee Record
Searching Employee ID `1005` returns the student record containing the student's name and AWS user ARN in the Description field.
![Test 4 - Student Record](screenshots/test4-student-record.png)

### Test 5 – Invalid Employee ID
Searching a nonexistent Employee ID (`999`) returns a clean "not found" error with no data leakage.
![Test 5 - Invalid ID](screenshots/test5-invalid-id.png)

### Test 6 – Unauthorized API Access
Calling `GET /employee/{id}` with no Authorization header is rejected by the Cognito authorizer at API Gateway before reaching the Lambda function, returning `401 Unauthorized`.
![Test 6 - Unauthorized Access](screenshots/test6-unauthorized.png)

## 5. AWS Service Configuration Screenshots

### DynamoDB table (Items view)
All 5 employee records, including the required student record (EmployeeID 1005).
![DynamoDB Table](screenshots/dynamodb-table.png)

### Lambda functions

**UI Lambda (`hr-lookup-ui`)** — serves the HTML/CSS/JS interface, triggered by API Gateway:
![UI Lambda Config](screenshots/lambda-ui-config.png)

**Backend Lambda (`hr-lookup-backend`)** — performs the DynamoDB lookup, triggered by API Gateway:
![Backend Lambda Config](screenshots/lambda-backend-config.png)

### API Gateway resources and Cognito authorizer

Resource tree showing `GET /`, `GET /employee/{id}`:
![API Gateway Resources](screenshots/apigateway-resources.png)

`GET /employee/{id}` method configuration, showing the `hr-lookup-cognito-authorizer` (COGNITO_USER_POOLS) attached as its Authorization method — confirming this endpoint is protected:
![API Gateway Cognito Authorizer](screenshots/apigateway-authorizer.png)

### Cognito User Pool
![Cognito User Pool](screenshots/cognito-user-pool.png)

### Decoded ID Token (proof of correct token usage)
The frontend sends the Cognito **ID token** (not the access token) to the API, as required. Decoded payload confirms `token_use: "id"`, the correct `iss` (user pool), `aud` (client ID), and the user's `sub`.
![Decoded JWT](screenshots/jwt-sub-decoded.png)

## 6. Exported API Gateway REST API Definition
See `apigateway-export.json` in this `docs/` folder (exported via API Gateway console → Stages → prod → Export → OpenAPI 3).

## 7. AI Tools Used
Claude (Anthropic, Claude.ai) was used throughout this assignment to:
- Scaffold the Terraform infrastructure-as-code (DynamoDB, IAM least-privilege policies, Lambda functions, Cognito User Pool/App Client, API Gateway REST API with a Cognito authorizer)
- Write the backend Lambda (DynamoDB lookup) and UI Lambda (HTML/CSS/JS single-page app implementing OAuth 2.0 Authorization Code + PKCE)
- Debug deployment issues (PowerShell command syntax errors, missing Python dependencies, Cognito user setup)
- Walk through and interpret test results (curl output, JWT decoding, DynamoDB/Lambda/API Gateway console configuration)

All generated code and infrastructure was reviewed, deployed, and manually tested by the student before submission. Every test scenario (Tests 1–6) was independently executed and verified against the live, deployed AWS resources.
