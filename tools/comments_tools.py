"""
Comments and Social Actions Tools for LinkedIn.
Supports retrieving comments and posting replies / first comments via the official /rest/socialActions API.
"""

import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from core.client import LinkedInClient
from shield.errors import map_http_error

def tool_get_post_comments(post_urn: str) -> Dict[str, Any]:
    """
    Retrieves comments for a specific LinkedIn post.
    Args:
        post_urn: The URN of the post (e.g. urn:li:share:123 or urn:li:ugcPost:123)
    """
    client = LinkedInClient()
    url = f"https://api.linkedin.com/rest/socialActions/{post_urn}/comments"
    req = urllib.request.Request(url, headers=client._get_headers(), method="GET")

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elements = data.get("elements", [])
            parsed_comments = []
            for el in elements:
                actor = el.get("actor", "")
                text = el.get("message", {}).get("text", "")
                comment_urn = el.get("object", "")
                parsed_comments.append({
                    "comment_urn": comment_urn,
                    "actor": actor,
                    "text": text,
                    "created_at": el.get("created", {}).get("time")
                })
            return {
                "success": True,
                "post_urn": post_urn,
                "total_comments": len(parsed_comments),
                "comments": parsed_comments
            }
    except urllib.error.HTTPError as e:
        raise map_http_error(e.code, e.read().decode("utf-8"))

def tool_create_comment(post_urn: str, text: str, parent_comment_urn: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a top-level comment (e.g. First Comment with link) or a reply to an existing comment.
    Args:
        post_urn: The target post URN.
        text: The content of the comment.
        parent_comment_urn: Optional URN of a comment to reply to (nested comment).
    """
    client = LinkedInClient()
    actor_urn = client.default_author_urn

    target_urn = parent_comment_urn if parent_comment_urn else post_urn
    url = f"https://api.linkedin.com/rest/socialActions/{target_urn}/comments"

    payload: Dict[str, Any] = {
        "actor": actor_urn,
        "message": {
            "text": text.strip()
        }
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers=client._get_headers(), method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            comment_urn = resp.headers.get("x-restli-id", "")
            return {
                "success": True,
                "post_urn": post_urn,
                "comment_urn": comment_urn,
                "text": text,
                "status": "COMMENT_CREATED"
            }
    except urllib.error.HTTPError as e:
        raise map_http_error(e.code, e.read().decode("utf-8"))
