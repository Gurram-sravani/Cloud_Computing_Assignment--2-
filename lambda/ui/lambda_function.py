import os

COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN", "")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID", "")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>HR Employee Lookup</title>
<style>
  body { font-family: Arial, Helvetica, sans-serif; max-width: 640px; margin: 48px auto; padding: 0 20px; color: #1c1c1c; }
  h1 { font-size: 22px; }
  #userbar { margin-bottom: 24px; padding: 10px 14px; background: #f0f4f8; border-radius: 6px; font-size: 14px; }
  #userbar button { padding: 6px 14px; cursor: pointer; }
  #app { display: none; }
  .row { display: flex; gap: 8px; margin-bottom: 16px; }
  input { flex: 1; padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 6px; }
  button.search { padding: 10px 18px; font-size: 14px; cursor: pointer; border: none; border-radius: 6px; background: #2563eb; color: white; }
  #result { margin-top: 12px; white-space: pre-wrap; background: #f4f4f4; padding: 16px; border-radius: 6px; font-family: monospace; font-size: 13px; min-height: 20px; }
  .error { color: #b00020; }
</style>
</head>
<body>
<h1>HR Employee Lookup</h1>
<div id="userbar">Checking session...</div>
<div id="app">
  <div class="row">
    <input id="empId" placeholder="Employee ID (e.g. 1001)" />
    <button class="search" id="searchBtn">Search</button>
  </div>
  <div id="result"></div>
</div>

<script>
const COGNITO_DOMAIN = "__COGNITO_DOMAIN__";
const CLIENT_ID = "__CLIENT_ID__";
const REDIRECT_URI = "__REDIRECT_URI__";

function base64UrlEncode(buffer) {
  return btoa(String.fromCharCode(...new Uint8Array(buffer)))
    .replace(/\\+/g, '-').replace(/\\//g, '_').replace(/=+$/, '');
}

async function sha256(plain) {
  const data = new TextEncoder().encode(plain);
  return await crypto.subtle.digest('SHA-256', data);
}

function randomString(len) {
  const arr = new Uint8Array(len);
  crypto.getRandomValues(arr);
  return base64UrlEncode(arr.buffer);
}

async function login() {
  const verifier = randomString(64);
  sessionStorage.setItem('pkce_verifier', verifier);
  const challenge = base64UrlEncode(await sha256(verifier));
  const url = COGNITO_DOMAIN + "/oauth2/authorize" +
    "?response_type=code&client_id=" + encodeURIComponent(CLIENT_ID) +
    "&redirect_uri=" + encodeURIComponent(REDIRECT_URI) +
    "&scope=" + encodeURIComponent("openid email profile") +
    "&code_challenge_method=S256&code_challenge=" + challenge;
  window.location.href = url;
}

function logout() {
  sessionStorage.clear();
  const url = COGNITO_DOMAIN + "/logout?client_id=" + encodeURIComponent(CLIENT_ID) +
    "&logout_uri=" + encodeURIComponent(REDIRECT_URI);
  window.location.href = url;
}

async function exchangeCodeForToken(code) {
  const verifier = sessionStorage.getItem('pkce_verifier');
  const body = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: CLIENT_ID,
    code: code,
    redirect_uri: REDIRECT_URI,
    code_verifier: verifier,
  });
  const resp = await fetch(COGNITO_DOMAIN + "/oauth2/token", {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body,
  });
  if (!resp.ok) throw new Error('Token exchange failed');
  const tokens = await resp.json();
  sessionStorage.setItem('id_token', tokens.id_token);
}

async function search() {
  const id = document.getElementById('empId').value.trim();
  const resultDiv = document.getElementById('result');
  if (!id) { resultDiv.innerHTML = '<span class="error">Enter an Employee ID</span>'; return; }
  resultDiv.textContent = 'Loading...';
  const idToken = sessionStorage.getItem('id_token');
  try {
    const resp = await fetch(window.location.pathname.replace(/\\/?$/, '/') + "employee/" + encodeURIComponent(id), {
      headers: { 'Authorization': 'Bearer ' + idToken },
    });
    const data = await resp.json();
    if (!resp.ok) {
      resultDiv.innerHTML = '<span class="error">' + (data.error || 'Error') + '</span>';
      return;
    }
    resultDiv.textContent =
      "Employee ID: " + data.employeeId + "\\n" +
      "Name: " + data.name + "\\n" +
      "Salary: " + data.salary + "\\n" +
      "Date of Join: " + data.dateOfJoin + "\\n" +
      "Description: " + data.description;
  } catch (e) {
    resultDiv.innerHTML = '<span class="error">Request failed</span>';
  }
}

async function init() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get('code');
  if (code) {
    await exchangeCodeForToken(code);
    window.history.replaceState({}, document.title, REDIRECT_URI);
  }
  const idToken = sessionStorage.getItem('id_token');
  const userbar = document.getElementById('userbar');
  if (idToken) {
    userbar.innerHTML = 'Logged in. <button onclick="logout()">Log out</button>';
    document.getElementById('app').style.display = 'block';
  } else {
    userbar.innerHTML = '<button onclick="login()">Log in</button>';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('searchBtn').addEventListener('click', search);
  init();
});
</script>
</body>
</html>
"""


def lambda_handler(event, context):
    headers = event.get("headers") or {}
    host = headers.get("Host") or headers.get("host") or ""
    stage = (event.get("requestContext") or {}).get("stage", "")
    redirect_uri = f"https://{host}/{stage}/" if host else ""

    html = (
        HTML_TEMPLATE.replace("__COGNITO_DOMAIN__", COGNITO_DOMAIN)
        .replace("__CLIENT_ID__", CLIENT_ID)
        .replace("__REDIRECT_URI__", redirect_uri)
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": html,
    }
