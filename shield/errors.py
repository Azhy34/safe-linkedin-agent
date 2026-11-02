"""
LinkedIn API Error Handling & Structured Contracts.
Translates raw LinkedIn HTTP 4xx/5xx responses into typed exceptions.
"""

from typing import Optional, Dict, Any

class LinkedInAPIError(Exception):
    def __init__(self, status_code: int, message: str, error_details: Optional[Dict[str, Any]] = None):
        super().__init__(f"LinkedIn API Error [{status_code}]: {message}")
        self.status_code = status_code
        self.message = message
        self.error_details = error_details or {}

class LinkedInAuthError(LinkedInAPIError):
    """Raised on 401 Unauthorized (expired token or invalid credentials)."""
    pass

class LinkedInForbiddenError(LinkedInAPIError):
    """Raised on 403 Forbidden (insufficient scopes or permissions)."""
    pass

class LinkedInRateLimitError(LinkedInAPIError):
    """Raised on 429 Too Many Requests."""
    pass

def map_http_error(status_code: int, response_body: str) -> LinkedInAPIError:
    import json
    try:
        data = json.loads(response_body)
        msg = data.get("message") or data.get("error_description") or response_body
    except Exception:
        data = {}
        msg = response_body

    if status_code == 401:
        return LinkedInAuthError(status_code, f"Token expired or unauthorized. Run auth.py to refresh. Details: {msg}", data)
    elif status_code == 403:
        return LinkedInForbiddenError(status_code, f"Access forbidden. Check product scopes. Details: {msg}", data)
    elif status_code == 429:
        return LinkedInRateLimitError(status_code, f"Rate limit exceeded on LinkedIn API. Backing off. Details: {msg}", data)
    else:
        return LinkedInAPIError(status_code, msg, data)
