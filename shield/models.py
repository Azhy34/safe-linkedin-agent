"""
Pydantic contracts for LinkedIn API Gateway.
Enforces strict schema validation for Posts, Conversions (CAPI), and Identity Verification.
"""

from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class PostVisibility(str, Enum):
    PUBLIC = "PUBLIC"
    CONNECTIONS = "CONNECTIONS"

class PostLifecycleState(str, Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"

class LinkedInPostRequest(BaseModel):
    """Input contract for publishing an organic post."""
    text: str = Field(..., min_length=1, max_length=3000, description="The body of the post.")
    author_urn: Optional[str] = Field(None, description="Optional override: urn:li:person:... or urn:li:organization:...")
    visibility: PostVisibility = Field(default=PostVisibility.PUBLIC, description="Audience visibility.")
    article_url: Optional[str] = Field(None, description="Optional link attachment URL.")
    article_title: Optional[str] = Field(None, description="Title for the link preview.")
    dry_run: bool = Field(default=False, description="If True, validates and previews payload without mutating LinkedIn.")

    @field_validator("text")
    def validate_text(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Post text cannot be empty or whitespace only.")
        return clean

class LinkedInPostResponse(BaseModel):
    """Output contract after post creation."""
    success: bool
    post_urn: str
    author: str
    status: str
    created_at_utc: str
    post_url: Optional[str] = None
    dry_run: bool = False
    raw_response: Optional[Dict[str, Any]] = None

class CAPIFunnelEvent(BaseModel):
    """Input contract for Conversions API (CAPI) server-to-server events."""
    event_name: str = Field(..., description="e.g. Lead_Qualified, Calendly_Booked, Demo_Completed")
    hashed_email: str = Field(..., description="64-character lowercase SHA-256 hex string.")
    currency: str = Field(default="EUR", description="Currency code (e.g. EUR, USD)")
    amount: float = Field(default=0.0, ge=0.0, description="Conversion value")
    click_id: Optional[str] = Field(None, description="li_fat_id cookie value if present")

    @field_validator("hashed_email")
    def validate_sha256(cls, v: str) -> str:
        clean = v.strip().lower()
        if len(clean) != 64 or not all(c in "0123456789abcdef" for c in clean):
            raise ValueError("hashed_email must be a valid 64-character lowercase SHA-256 hex string.")
        return clean

class MemberVerificationReport(BaseModel):
    """Output contract for Verified on LinkedIn profile verification."""
    is_verified: bool
    member_urn: str
    verification_categories: List[str] = Field(default_factory=list)
    verified_workplace: Optional[str] = None
    verified_at: Optional[str] = None
