"""
FastMCP Tools for LinkedIn Publishing and Content Auditing.
"""

from typing import Dict, Any, Optional
from core.client import LinkedInClient
from shield.models import LinkedInPostRequest, PostVisibility
from shield.invariants import (
    check_zero_leak_invariant,
    check_markdown_hygiene,
    audit_150_char_fold,
    audit_boost_readiness
)

def tool_publish_post(
    text: str,
    visibility: str = "PUBLIC",
    article_url: Optional[str] = None,
    article_title: Optional[str] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Publishes a post to LinkedIn with strict deterministic security guardrails.
    
    Args:
        text: The content of the post.
        visibility: 'PUBLIC' (default) or 'CONNECTIONS'.
        article_url: Optional URL attachment for rich preview.
        article_title: Optional title for article preview.
        dry_run: If True, validates and previews payload without mutating live LinkedIn feed.
    """
    client = LinkedInClient()
    req = LinkedInPostRequest(
        text=text,
        visibility=PostVisibility(visibility.upper()),
        article_url=article_url,
        article_title=article_title,
        dry_run=dry_run
    )
    res = client.publish_post(req)
    return res.model_dump()

def tool_audit_post_draft(text: str, article_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Audits a draft post before publishing against LinkedIn algorithm and safety rules:
    1. Zero-Leak Check (detects accidental API keys/tokens)
    2. Mobile 150-char fold verification
    3. Markdown formatting hygiene
    4. Thought Leader / Boost readiness (checks for external body links)
    """
    try:
        check_zero_leak_invariant(text)
        leak_safe = True
        leak_msg = "PASSED: Zero confidential patterns detected."
    except ValueError as e:
        leak_safe = False
        leak_msg = str(e)

    md_warnings = check_markdown_hygiene(text)
    fold_ok, fold_msg = audit_150_char_fold(text)
    boost_warnings = audit_boost_readiness(text, article_url)

    is_ready = leak_safe and fold_ok and len(md_warnings) == 0

    return {
        "ready_to_publish": is_ready,
        "zero_leak_check": {"passed": leak_safe, "message": leak_msg},
        "mobile_fold_check": {"passed": fold_ok, "details": fold_msg},
        "markdown_warnings": md_warnings,
        "boost_readiness_warnings": boost_warnings,
        "character_count": len(text)
    }
