"""
Deterministic Business Invariants for LinkedIn Operations.
Prevents malformed, leaking, or algorithm-penalized posts from reaching the API.
"""

import re
from typing import List, Tuple

# Patterns that indicate leaked secrets
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{16,}"),
    re.compile(r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}"),
    re.compile(r"(?i)client[_-]?secret\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{16,}"),
    re.compile(r"(?i)password\s*[:=]\s*['\"]?[^\s'\"]{6,}"),
]

def check_zero_leak_invariant(text: str) -> None:
    """Raises ValueError if any potential secret, API key, or token is detected in post text."""
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise ValueError("SECURITY INVARIANT VIOLATION: Potential secret or API key detected in text payload. Aborting mutation.")

def check_markdown_hygiene(text: str) -> List[str]:
    """
    LinkedIn does not render standard Markdown.
    Warns if '**bold**' or '## heading' or '```' formatting is used.
    """
    warnings = []
    if "**" in text or "__" in text:
        warnings.append("Raw markdown bold (**text**) detected. LinkedIn renders literal asterisks. Use plain Unicode or clean text.")
    if re.search(r"^#{1,6}\s", text, re.MULTILINE):
        warnings.append("Markdown headers (# Heading) detected. Use uppercase or Unicode styling instead.")
    return warnings

def audit_150_char_fold(text: str) -> Tuple[bool, str]:
    """
    Evaluates whether the opening hook fits before the mobile fold (approx 140-150 characters).
    """
    first_paragraph = text.split("\n\n")[0].strip()
    if len(first_paragraph) <= 160:
        return True, f"Hook fits within mobile fold ({len(first_paragraph)} chars)."
    return False, f"Opening paragraph is {len(first_paragraph)} chars (exceeds 150-char fold before '...see more')."

def audit_boost_readiness(text: str, article_url: str = None) -> List[str]:
    """
    LinkedIn Thought Leader Ads and boost algorithms penalize posts with links in the body.
    """
    warnings = []
    url_pattern = re.compile(r"https?://[^\s]+")
    body_links = url_pattern.findall(text)
    if body_links or article_url:
        warnings.append("External link present in body. Post will have lower organic reach and may be restricted from Thought Leader Ads. (Best Practice: put link in First Comment).")
    return warnings
