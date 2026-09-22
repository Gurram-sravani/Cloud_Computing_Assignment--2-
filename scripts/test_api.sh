#!/usr/bin/env bash
# Quick smoke tests for the deployed API.
# Usage: ./test_api.sh <api_url> <id_token>
#   api_url:  e.g. https://abc123.execute-api.us-east-1.amazonaws.com/prod/
#   id_token: a valid Cognito ID token (optional, only needed for auth tests)

set -e
API_URL="${1:?Usage: $0 <api_url> [id_token]}"
ID_TOKEN="${2:-}"

echo "== Test 1: GET / (should return HTML, 200) =="
curl -s -o /dev/null -w "HTTP %{http_code}\n" "${API_URL}"

echo "== Test 6: GET /employee/1001 with NO token (should be 401/403) =="
curl -s -o /dev/null -w "HTTP %{http_code}\n" "${API_URL}employee/1001"

if [ -n "$ID_TOKEN" ]; then
  echo "== Test 3: GET /employee/1001 WITH token (should be 200 + JSON) =="
  curl -s -H "Authorization: Bearer ${ID_TOKEN}" "${API_URL}employee/1001"
  echo

  echo "== Test 4: GET /employee/1005 (student record) =="
  curl -s -H "Authorization: Bearer ${ID_TOKEN}" "${API_URL}employee/1005"
  echo

  echo "== Test 5: GET /employee/9999 (invalid id, should be 404) =="
  curl -s -w "\nHTTP %{http_code}\n" -H "Authorization: Bearer ${ID_TOKEN}" "${API_URL}employee/9999"
else
  echo "(Skipping authenticated tests - no ID token provided)"
fi
