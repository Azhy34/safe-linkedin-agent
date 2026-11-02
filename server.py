"""
Safe LinkedIn FastMCP Server.
Exposes deterministic, zero-leak tools to AI agents for publishing, auditing,
commenting, and streaming Conversions API (CAPI) events via official LinkedIn REST APIs.
"""

import sys
import os
from pathlib import Path
from typing import Optional

# Ensure package roots are in path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp.server.fastmcp import FastMCP
from tools.publish_tools import tool_publish_post, tool_audit_post_draft
from tools.comments_tools import tool_get_post_comments, tool_create_comment
from tools.capi_tools import tool_send_capi_conversion
from core.client import LinkedInClient

mcp = FastMCP("Safe-LinkedIn-MCP", dependencies=["pydantic"])

@mcp.tool()
def get_linkedin_profile_status() -> dict:
    """
    Checks the current LinkedIn connection health and returns authenticated member info.
    """
    try:
        client = LinkedInClient()
        me = client.get_me()
        return {
            "status": "HEALTHY",
            "member_name": me.get("name"),
            "member_email": me.get("email"),
            "member_urn": client.default_author_urn,
            "sub_id": me.get("sub")
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e)
        }

@mcp.tool()
def audit_linkedin_post(text: str, article_url: Optional[str] = None) -> dict:
    """
    Deterministically audits a post draft before publishing:
    checks zero-leak invariants, mobile 150-char fold, and Boost / Thought Leader readiness.
    """
    return tool_audit_post_draft(text, article_url)

@mcp.tool()
def publish_linkedin_post(
    text: str,
    visibility: str = "PUBLIC",
    article_url: Optional[str] = None,
    article_title: Optional[str] = None,
    dry_run: bool = False
) -> dict:
    """
    Publishes a verified post to LinkedIn with deterministic safety shields.
    Set dry_run=True to preview payload and inspect warnings without mutating LinkedIn.
    """
    return tool_publish_post(
        text=text,
        visibility=visibility,
        article_url=article_url,
        article_title=article_title,
        dry_run=dry_run
    )

@mcp.tool()
def get_linkedin_comments(post_urn: str) -> dict:
    """
    Retrieves comments and discussion threads for a LinkedIn post.
    Args:
        post_urn: Target post URN (e.g. urn:li:share:123 or urn:li:ugcPost:123).
    """
    return tool_get_post_comments(post_urn)

@mcp.tool()
def post_linkedin_comment(post_urn: str, text: str, parent_comment_urn: Optional[str] = None) -> dict:
    """
    Posts a first comment on your own post (for links/sources) or replies to an existing user comment.
    Args:
        post_urn: The target post URN.
        text: The text content of the comment.
        parent_comment_urn: Optional URN of a specific comment to reply to (nested reply).
    """
    return tool_create_comment(post_urn=post_urn, text=text, parent_comment_urn=parent_comment_urn)

@mcp.tool()
def stream_linkedin_conversion(
    event_name: str,
    email: str,
    conversion_urn: str,
    amount: float = 0.0,
    currency: str = "EUR"
) -> dict:
    """
    Streams a server-side conversion event to LinkedIn Conversions API (CAPI)
    for attribution and populating dynamic Retargeting Matched Audiences.
    Email is normalized and SHA-256 hashed locally before transmission.
    """
    return tool_send_capi_conversion(
        event_name=event_name,
        raw_email=email,
        conversion_urn=conversion_urn,
        amount=amount,
        currency=currency
    )

if __name__ == "__main__":
    mcp.run()
