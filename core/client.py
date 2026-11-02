"""
Production-grade LinkedIn API Client.
Connects to official LinkedIn REST endpoints with automatic header management,
error handling, and token lifecycle support.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

from shield.models import (
    LinkedInPostRequest,
    LinkedInPostResponse,
    PostVisibility,
    PostLifecycleState
)
from shield.invariants import (
    check_zero_leak_invariant,
    check_markdown_hygiene,
    audit_150_char_fold,
    audit_boost_readiness
)
from shield.errors import map_http_error, LinkedInAuthError

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILE = BASE_DIR / "token.json"
ENV_FILE = BASE_DIR / ".env"

DEFAULT_API_VERSION = "202401"

class LinkedInClient:
    def __init__(self, token_file: Optional[Path] = None, api_version: str = DEFAULT_API_VERSION):
        self.token_file = token_file or TOKEN_FILE
        self.api_version = api_version
        self.token_data = self._load_token_data()
        self.access_token = self.token_data.get("access_token")
        self.default_author_urn = self.token_data.get("member_urn")

        if not self.access_token:
            raise LinkedInAuthError(401, "No access token found in token.json. Run auth.py first to authenticate.")

    def _load_token_data(self) -> Dict[str, Any]:
        if not self.token_file.exists():
            return {}
        try:
            with open(self.token_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _get_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": self.api_version,
            "Content-Type": content_type
        }
        return headers

    def get_me(self) -> Dict[str, Any]:
        """Fetches the authenticated member's OpenID userinfo profile."""
        url = "https://api.linkedin.com/v2/userinfo"
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            method="GET"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise map_http_error(e.code, e.read().decode("utf-8"))

    def publish_post(self, request: LinkedInPostRequest) -> LinkedInPostResponse:
        """
        Publishes a post to LinkedIn via the official /rest/posts API endpoint.
        Passes through Zero-Leak & Invariant Shields before sending.
        """
        # 1. Invariant & Security Shield
        check_zero_leak_invariant(request.text)
        md_warnings = check_markdown_hygiene(request.text)
        fold_ok, fold_msg = audit_150_char_fold(request.text)
        boost_warnings = audit_boost_readiness(request.text, request.article_url)

        author_urn = request.author_urn or self.default_author_urn
        if not author_urn:
            raise ValueError("No author URN provided or found in token.json.")

        # 2. Build Payload according to official Posts API specification
        payload: Dict[str, Any] = {
            "author": author_urn,
            "commentary": request.text,
            "visibility": request.visibility.value,
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": PostLifecycleState.PUBLISHED.value,
            "isReshareDisabledByAuthor": False
        }

        # Optional Article / Link Attachment
        if request.article_url:
            payload["content"] = {
                "article": {
                    "source": request.article_url,
                    "title": request.article_title or "Article Preview"
                }
            }

        # Dry Run Mode: Return formatted preview without mutating live LinkedIn feed
        if request.dry_run:
            return LinkedInPostResponse(
                success=True,
                post_urn="urn:li:post:DRY_RUN_PREVIEW",
                author=author_urn,
                status="DRY_RUN_VALIDATED",
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                post_url=None,
                dry_run=True,
                raw_response={
                    "payload_preview": payload,
                    "fold_audit": {"passed": fold_ok, "details": fold_msg},
                    "markdown_warnings": md_warnings,
                    "boost_readiness_warnings": boost_warnings
                }
            )

        # 3. Live Execution
        url = "https://api.linkedin.com/rest/posts"
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=req_data,
            headers=self._get_headers(),
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as resp:
                # LinkedIn Posts API returns 201 Created and puts post URN in x-restli-id header
                post_urn = resp.headers.get("x-restli-id", "")
                created_time = datetime.now(timezone.utc).isoformat()
                
                # Generate post URL if URN format is standard urn:li:share:ID or urn:li:ugcPost:ID
                post_url = None
                if post_urn:
                    parts = post_urn.split(":")
                    if len(parts) >= 4:
                        post_url = f"https://www.linkedin.com/feed/update/{post_urn}/"

                return LinkedInPostResponse(
                    success=True,
                    post_urn=post_urn,
                    author=author_urn,
                    status="PUBLISHED",
                    created_at_utc=created_time,
                    post_url=post_url,
                    dry_run=False,
                    raw_response={"headers": dict(resp.headers)}
                )
        except urllib.error.HTTPError as e:
            raw_err = e.read().decode("utf-8")
            raise map_http_error(e.code, raw_err)

