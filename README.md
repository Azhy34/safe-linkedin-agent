# Safe LinkedIn Agent & FastMCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-Native-green.svg)](https://github.com/jlowin/fastmcp)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.0+-orange.svg)](https://docs.pydantic.dev/)
[![Zero-Leak Guarantee](https://img.shields.io/badge/Security-Zero--Leak%20Policy-success.svg)](#security--zero-leak-policy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade FastMCP server and deterministic agent operations framework for LinkedIn REST API v2. It replaces fragile, ban-prone browser automation with official developer endpoints, Pydantic guardrail shields, Exa post radar, and server-side Conversions API (CAPI) streaming.

---

## Why This Exists

Most LinkedIn automation relies on brittle Chrome extensions, cookie hijacking, or unguided LLMs calling raw APIs. This leads to account suspensions, burned reputations, and hallucinations.

**Safe LinkedIn Agent** establishes a deterministic boundary between AI models and LinkedIn:
1. **Official REST API:** Uses official LinkedIn developer products (`Share on LinkedIn` and `Community Management`). Zero browser scraping.
2. **Deterministic Shield:** Hardcoded Pydantic validators inspect every draft offline before any write operation reaches LinkedIn.
3. **Fail-Fast Rails:** If the model hallucinates formatting, leaks a key, or violates length boundaries, code terminates the execution immediately.
4. **Exa Radar:** Scans target industry discussions (PPC, AI Ops, B2B engineering) to draft high-signal thought leadership comments.
5. **Full Observability:** Structured audit logs and dry-run modes for every tool invocation.

---

## Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 1. DISCOVERY & RADAR (Exa Search Engine)                               │
│ • Real-time scan of high-signal discussions (Google Ads, AI Ops, B2B)  │
│ • Competitive debate extraction and community pain point analysis      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. DETERMINISTIC CONTENT SHIELD (Pydantic Invariants)                  │
│ • Zero-Leak Rule: regex scans block tokens and API keys                │
│ • 150-Char Mobile Fold: guarantees hook visibility before "see more"   │
│ • Formatting Hygiene: eliminates raw markdown asterisks and em-dashes  │
│ • Dry-Run Mode: pre-flight execution preview with JSON diffs           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. FASTMCP EXECUTION GATEWAY (Microservice Layer)                     │
│ • get_linkedin_profile_status: OAuth2 token health and scope check     │
│ • audit_linkedin_post: offline invariant audit without API cost        │
│ • publish_linkedin_post: official POST /rest/posts execution           │
│ • post_linkedin_comment: first-comment and nested thread replies       │
│ • stream_linkedin_conversion: SHA-256 hashed CAPI offline attribution │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. LINKEDIN REST API v2 (Official Platform Layer)                      │
│ • Member Social (w_member_social)                                      │
│ • Organization Social (w_organization_social)                          │
│ • Conversions API (CAPI) & Matched Audiences                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## FastMCP Tools Overview

| Tool Name | Type | Description |
| :--- | :--- | :--- |
| `get_linkedin_profile_status` | Read | Verifies OAuth2 token validity, active scopes, and authenticated member URN. |
| `audit_linkedin_post` | Read / Offline | Validates a draft against zero-leak invariants, mobile fold limits, and formatting rules. |
| `publish_linkedin_post` | Mutate | Publishes a post to member profile or company page via official `/rest/posts`. Supports `dry_run=True`. |
| `get_linkedin_comments` | Read | Fetches discussion threads and replies for a given post URN. |
| `post_linkedin_comment` | Mutate | Adds a first comment or replies to an existing user comment with guardrails. |
| `stream_linkedin_conversion` | Mutate | Streams server-side offline conversions (hashed email, lead value) to LinkedIn CAPI. |

---

## Quickstart & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Azhy34/safe-linkedin-agent.git
cd safe-linkedin-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

*(Or simply `pip install pydantic fastmcp requests`)*

### 3. Configure credentials
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Populate your `.env` with credentials from the [LinkedIn Developer Portal](https://www.linkedin.com/developers/):
```env
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000/callback
LINKEDIN_ORGANIZATION_ID=your_company_id_optional
```

### 4. Authenticate via OAuth 2.0
Run the local OAuth helper:
```bash
python core/auth.py
```
This starts a lightweight callback server on `http://localhost:8000/callback`, opens your browser to authenticate, and safely saves a 60-day token to `token.json` (git-ignored).

### 5. Run Offline Verification Tests
```bash
python -m unittest discover -s tests
```
All unit tests run offline in under 0.01s with zero API quota consumption.

---

## Integrating with AI Clients

### Claude Desktop / Gemini CLI / Antigravity MCP Config

Add the server to your MCP configuration file (`mcp_config.json`):

```json
{
  "mcpServers": {
    "safe-linkedin-mcp": {
      "command": "python",
      "args": [
        "-u",
        "C:/path/to/safe-linkedin-agent/server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

## Security & Zero-Leak Policy

- **Token Isolation:** `token.json` and `.env` are strictly excluded from version control via `.gitignore`.
- **Pre-Flight Regex Inspection:** The Pydantic validator scans every post body for patterns matching API keys, client secrets, and bearer tokens.
- **Fail-Fast Termination:** If an invariant fails, an unhandled exception is raised before any HTTP request is dispatched.

---

## License

MIT License. Designed and maintained by [Mikhail Azhyshchev](https://azhyshchev.de).
