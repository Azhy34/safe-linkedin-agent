"""
LinkedIn OAuth 2.0 Authorization & Token Manager.
Runs a local callback server on http://localhost:8000/callback to receive the OAuth code,
exchanges it for an access token, discovers Member URN and Organization IDs,
and saves tokens safely to token.json (ignored by git).
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import json
import webbrowser
import urllib.parse
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Load .env manually without external dependencies
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
TOKEN_FILE = Path(__file__).resolve().parent.parent / "token.json"

def load_env():
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
    return env_vars

env = load_env()
CLIENT_ID = env.get("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = env.get("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = env.get("LINKEDIN_REDIRECT_URI", "http://localhost:8000/callback")

# Standard approved scopes for OpenID Connect + Share on LinkedIn
SCOPES = [
    "openid",
    "profile",
    "email",
    "w_member_social"
]

auth_code = None

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/callback":
            query_params = urllib.parse.parse_qs(parsed_url.query)
            if "code" in query_params:
                auth_code = query_params["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"""
                <html>
                <body style="font-family:sans-serif;text-align:center;padding:50px;background:#0f172a;color:#b9ddb7;">
                    <h2>&#x2705; LinkedIn Authorization Successful!</h2>
                    <p style="color:#cbd5e1;">You can close this tab and return to your terminal.</p>
                </body>
                </html>
                """)
            elif "error" in query_params:
                error_desc = query_params.get("error_description", ["Unknown error"])[0]
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h2>Authorization Error</h2><p>{error_desc}</p>".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress noisy HTTP server logs
        pass

def exchange_token(code: str) -> dict:
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        print(f"❌ Error exchanging token: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)

def fetch_user_info(access_token: str) -> dict:
    url = "https://api.linkedin.com/v2/userinfo"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        method="GET"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️ Could not fetch userinfo: {e}")
        return {}

def fetch_administered_orgs(access_token: str) -> list:
    url = "https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        method="GET"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elements = data.get("elements", [])
            org_urns = [e.get("organizationalTarget") for e in elements if "organizationalTarget" in e]
            return org_urns
    except Exception:
        # Scope might not be granted yet, fallback gracefully
        return []

def run_auth_flow():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Error: LINKEDIN_CLIENT_ID or LINKEDIN_CLIENT_SECRET is missing in .env")
        print("Please paste them into safe-linkedin-mcp/.env before running.")
        sys.exit(1)

    scope_str = "%20".join(SCOPES)
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={CLIENT_ID}&"
        f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
        f"scope={scope_str}&state=safe_linkedin_state_123"
    )

    print("\n" + "="*60, flush=True)
    print("🔐 Starting LinkedIn OAuth 2.0 Authorization Flow", flush=True)
    print("="*60, flush=True)
    print("\n1. Opening your browser to authorize with LinkedIn...", flush=True)
    print(f"If browser doesn't open automatically, visit this URL:\n\n{auth_url}\n", flush=True)

    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", 8000), OAuthCallbackHandler)
    print("2. Waiting for callback on http://localhost:8000/callback ...", flush=True)

    while auth_code is None:
        server.handle_request()

    print("\n✅ Authorization code received from LinkedIn!")
    print("3. Exchanging code for Access Token...")
    token_data = exchange_token(auth_code)

    access_token = token_data.get("access_token")
    expires_in = token_data.get("expires_in")
    print(f"✅ Access Token obtained (valid for {expires_in // 86400} days)!")

    # Fetch User Profile Info
    print("4. Fetching member profile & organization details...")
    user_info = fetch_user_info(access_token)
    member_sub = user_info.get("sub", "")
    member_name = user_info.get("name", "")
    member_email = user_info.get("email", "")

    # Check Organizations
    orgs = fetch_administered_orgs(access_token)

    saved_data = {
        "access_token": access_token,
        "expires_in": expires_in,
        "member_sub": member_sub,
        "member_urn": f"urn:li:person:{member_sub}" if member_sub else "",
        "member_name": member_name,
        "member_email": member_email,
        "organizations": orgs
    }

    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(saved_data, f, indent=2)

    print("\n" + "="*60)
    print("🎉 SUCCESS: LinkedIn Authentication Complete!")
    print("="*60)
    print(f"👤 Member Name : {member_name}")
    print(f"📧 Member Email: {member_email}")
    print(f"🆔 Member URN  : urn:li:person:{member_sub}")
    if orgs:
        print(f"🏢 Organizations: {', '.join(orgs)}")
    print(f"\n📁 Tokens and IDs safely saved to: {TOKEN_FILE}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_auth_flow()

