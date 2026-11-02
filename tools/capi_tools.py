"""
Conversions API (CAPI) Tools for LinkedIn.
Streams server-to-server conversion events directly into Campaign Manager for retargeting and attribution.
"""

import time
import json
import hashlib
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from core.client import LinkedInClient
from shield.models import CAPIFunnelEvent
from shield.errors import map_http_error

def tool_send_capi_conversion(
    event_name: str,
    raw_email: str,
    conversion_urn: str,
    amount: float = 0.0,
    currency: str = "EUR",
    click_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Streams a server-side conversion event to LinkedIn CAPI with automated SHA-256 PII hashing.
    
    Args:
        event_name: Name of milestone (e.g. 'Lead_Qualified', 'Calendly_Booked').
        raw_email: Plain email (will be sanitized and SHA-256 hashed locally before sending).
        conversion_urn: The conversion rule URN from LinkedIn Campaign Manager (e.g. 'urn:lla:llaPartnerConversion:12345').
        amount: Monetary value of conversion.
        currency: 'EUR', 'USD', etc.
        click_id: Optional li_fat_id cookie value.
    """
    # 1. Local Normalization & Hashing (Zero raw PII leaves server)
    clean_email = raw_email.strip().lower()
    hashed_email = hashlib.sha256(clean_email.encode("utf-8")).hexdigest()

    event = CAPIFunnelEvent(
        event_name=event_name,
        hashed_email=hashed_email,
        currency=currency,
        amount=amount,
        click_id=click_id
    )

    client = LinkedInClient()
    url = "https://api.linkedin.com/rest/conversions"

    user_ids = [
        {
            "idType": "SHA256_EMAIL",
            "idValue": event.hashed_email
        }
    ]
    if event.click_id:
        user_ids.append({
            "idType": "LINKEDIN_FIRST_PARTY_ADS_TRACKING_UUID",
            "idValue": event.click_id
        })

    payload = {
        "conversion": conversion_urn,
        "conversionHappenedAt": int(time.time() * 1000),
        "user": {
            "userIds": user_ids
        },
        "conversionValue": {
            "currencyCode": event.currency,
            "amount": f"{event.amount:.2f}"
        }
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers=client._get_headers(), method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            return {
                "success": True,
                "event_name": event.event_name,
                "hashed_email_prefix": f"{event.hashed_email[:8]}...",
                "status": "CONVERSION_STREAMED",
                "http_status": resp.status
            }
    except urllib.error.HTTPError as e:
        raise map_http_error(e.code, e.read().decode("utf-8"))
