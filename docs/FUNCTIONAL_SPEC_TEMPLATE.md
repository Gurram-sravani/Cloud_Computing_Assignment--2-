# Functional Specification – Serverless HR Lookup Application

**Student Name:**
**Date:**
**GitHub Repository URL:**

## 1. Architecture Diagram
(Paste/insert the architecture diagram image here — the one from the assignment, or your own re-drawing of it.)

## 2. Authentication-Flow Diagram
(Paste/insert the OAuth 2.0 Authorization Code + PKCE diagram here.)

## 3. Deployed Resource Details
| Item | Value |
|---|---|
| API Gateway URL | |
| Cognito Managed Login domain | |
| Cognito Client ID | |
| Cognito User Pool Subject UUID (sub) | |

## 4. Test Evidence

### Test 1 – Application Access
(Full browser screenshot, URL bar visible, app UI loaded)

### Test 2 – User Authentication
(Full browser screenshot of the Cognito Managed Login page, URL bar visible)

### Test 3 – Valid Employee Lookup
(Screenshot of a successful lookup showing all 5 fields)

### Test 4 – Student Employee Record
(Screenshot showing your name and AWS user ARN)

### Test 5 – Invalid Employee ID
(Screenshot of the "not found" error)

### Test 6 – Unauthorized API Access
(Screenshot/output of curl or browser dev tools showing the request without a token being rejected)

## 5. AWS Service Configuration Screenshots
- DynamoDB table (items view)
- Lambda functions (configuration + IAM role)
- API Gateway (resources/methods + authorizer)
- Cognito User Pool (app client settings)

## 6. Exported API Gateway REST API Definition
(Attach the exported OpenAPI/Swagger JSON — API Gateway console → Export)

## 7. AI Tools Used
Document which AI tools were used, for what steps, and how outputs were reviewed/verified. For example:
- Claude (Anthropic) — used to scaffold Terraform IaC, Lambda functions, and the frontend PKCE flow; code was reviewed and tested manually before deployment.
