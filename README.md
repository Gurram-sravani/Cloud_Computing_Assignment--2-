# Serverless HR Lookup Application

An end-to-end serverless HR app on AWS: API Gateway (REST) + Lambda + DynamoDB,
secured with Cognito Managed Login (OAuth 2.0 Authorization Code + PKCE).

```
Browser --HTTPS--> API Gateway --+-- GET /              --> UI Lambda (HTML/CSS/JS)
                                  +-- GET /employee/{id} --> Cognito Authorizer --> Backend Lambda --> DynamoDB
```

## Repository layout
```
terraform/        Infrastructure as code (DynamoDB, IAM, Lambda, Cognito, API Gateway)
lambda/backend/    Backend Lambda - employee lookup (lambda_function.py)
lambda/ui/         UI Lambda - serves the single-page app (lambda_function.py)
scripts/           seed_dynamodb.py (sample data), test_api.sh (smoke tests)
docs/              Functional spec template for your Canvas submission
```

## Prerequisites
- AWS account + credentials configured (`aws configure`), with permission to create
  the resources below.
- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.5
- Python 3.9+ and `boto3` installed locally (`pip install boto3`) for the seed script.

## 1. Deploy the infrastructure

Terraform needs the API's own URL as the Cognito callback URL, but that URL is only
known **after** the API Gateway is created — so this is a two-step apply.

```bash
cd terraform
terraform init

# Step 1: first apply (uses a placeholder callback URL)
terraform apply -var="cognito_domain_prefix=hr-lookup-<yourname>" \
                 -var="student_name=<Your Full Name>"

# Note the "api_url" output, e.g.:
#   https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/

# Step 2: re-apply, now pointing Cognito's callback/logout URL at the real app URL
terraform apply -var="cognito_domain_prefix=hr-lookup-<yourname>" \
                 -var="student_name=<Your Full Name>" \
                 -var="callback_url=https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/"
```

`cognito_domain_prefix` must be globally unique — use something like
`hr-lookup-<your-username>`.

## 2. Populate DynamoDB

Get your AWS user ARN and the table name from the Terraform outputs, then seed the table
(this also creates the required student record, Employee ID `1005`):

```bash
terraform output caller_arn
terraform output dynamodb_table_name

cd ../scripts
python seed_dynamodb.py <dynamodb_table_name> "Your Full Name" "<your-aws-user-arn>"
```

## 3. Test it

Open `terraform output api_url` in a browser, click **Log in**, authenticate via
Cognito Managed Login, then search for Employee ID `1001` (sample) and `1005` (your
student record).

For the scripted tests (Test 1, 3, 4, 5, 6 from the assignment):

```bash
cd scripts
chmod +x test_api.sh
# Unauthenticated checks (Test 1 and Test 6):
./test_api.sh "$(cd ../terraform && terraform output -raw api_url)"

# To also run the authenticated checks (Test 3, 4, 5), grab an ID token by logging
# into the app in a browser, opening DevTools > Application > Session Storage, and
# copying the `id_token` value, then:
./test_api.sh "$(cd ../terraform && terraform output -raw api_url)" "<id_token>"
```

| Test | What it checks | How |
|---|---|---|
| 1 – Application Access | App loads over HTTPS | Open the API URL in a browser |
| 2 – User Authentication | Cognito login works | Click "Log in", sign in via Managed Login |
| 3 – Valid Employee Lookup | All 5 fields returned | Search `1001` (or any seeded ID) |
| 4 – Student Employee Record | Your name + ARN shown | Search `1005` |
| 5 – Invalid Employee ID | Friendly error | Search e.g. `9999` |
| 6 – Unauthorized API Access | Request rejected without token | `curl` the `/employee/{id}` endpoint with no `Authorization` header — expect 401/403 |

## 4. Documentation to capture for Canvas
Use `docs/FUNCTIONAL_SPEC_TEMPLATE.md` as a starting point. You'll need:
- Architecture diagram + auth-flow diagram (from the assignment, or redraw your own)
- Full-browser screenshots (URL bar visible) for: app UI, Cognito login page,
  successful lookup, student record, invalid-ID error
- AWS console screenshots: DynamoDB table, Lambda config, API Gateway resources/authorizer,
  Cognito app client
- Exported API Gateway REST API definition (console → your API → **Export** → OpenAPI JSON)
- `terraform output` values: `cognito_client_id`, `cognito_domain`, `api_url`,
  and the Cognito **sub** (get this from the Cognito console → Users → your user, or
  decode your ID token at jwt.io)

## 5. AI tools used
This project's Terraform, Lambda code, and frontend PKCE flow were scaffolded with
AI assistance (Claude, Anthropic). All code was reviewed before deployment. Document
your own usage of AI tools per the assignment's requirements in your functional spec.

## 6. Cleanup

**Don't skip this** — Cognito domains and some resources can incur cost even idle.

```bash
cd terraform
terraform destroy -var="cognito_domain_prefix=hr-lookup-<yourname>" \
                   -var="student_name=<Your Full Name>" \
                   -var="callback_url=<your api_url>"
```

This removes the API Gateway API/stage, both Lambda functions, the DynamoDB table,
the Cognito User Pool (client + Managed Login domain), and both IAM roles/policies.
Verify in the AWS Console afterward that nothing was left behind.

## Security notes
- No AWS credentials are embedded in application code; the backend Lambda uses its
  IAM execution role.
- The backend Lambda's IAM policy grants only `dynamodb:GetItem` on the single
  employees table (least privilege).
- The Cognito app client has no client secret (required for a public SPA using PKCE)
  and never appears in this repo.
- `GET /employee/{id}` requires a valid Cognito **ID token** (validated by the API
  Gateway Cognito authorizer), not the access token.
