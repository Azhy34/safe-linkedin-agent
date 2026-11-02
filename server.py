"""
Safe LinkedIn FastMCP Server.
Exposes deterministic, zero-leak tools to AI agents for publishing, auditing,
and managing LinkedIn presence via the official REST API.
"""

import sys
import os
from pathlib import Path

# Ensure package roots are in path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp.server.fastmcp import FastMCP
from tools.publish_tools import tool_publish_post, tool_audit_post_draft
from core.client import LinkedInClient

mcp = FastMCP("Safe-LinkedIn-MCP", dependencies=["pydantic"])

@mcp.tool()
def get_linkedin_profile_status() -> dict:
    """
    Checks the current LinkedIn connection health and returns the authenticated member info.
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
def audit_linkedin_post(text: str, article_url: str = None) -> dict:
    """
    Deterministically audits a post draft before publishing:
    checks zero-leak invariants, mobile 150-char fold, and Boost / Thought Leader readiness.
    """
    return tool_audit_post_draft(text, article_url)

@mcp.tool()
def publish_linkedin_post(
    text: str,
    visibility: str = "PUBLIC",
    article_url: str = None,
    article_title: str = None,
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

if __name__ == "__main__":
    mcp.run()
