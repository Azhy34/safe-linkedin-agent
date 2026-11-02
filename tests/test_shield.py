"""
Offline Unit Tests for safe-linkedin-mcp Shield & Invariants.
Runs without network calls or API credits.
"""

import unittest
from shield.models import LinkedInPostRequest, PostVisibility
from shield.invariants import (
    check_zero_leak_invariant,
    check_markdown_hygiene,
    audit_150_char_fold,
    audit_boost_readiness
)
from core.client import LinkedInClient

class TestLinkedInShield(unittest.TestCase):

    def test_post_request_validation(self):
        req = LinkedInPostRequest(
            text="Testing post on LinkedIn.",
            visibility=PostVisibility.PUBLIC,
            dry_run=True
        )
        self.assertEqual(req.text, "Testing post on LinkedIn.")
        self.assertTrue(req.dry_run)

    def test_empty_post_rejection(self):
        with self.assertRaises(ValueError):
            LinkedInPostRequest(text="   ")

    def test_zero_leak_invariant_blocks_api_key(self):
        malicious_text = "Check out my new system! API_KEY='sk-1234567890abcdef1234567890'"
        with self.assertRaises(ValueError) as ctx:
            check_zero_leak_invariant(malicious_text)
        self.assertIn("SECURITY INVARIANT VIOLATION", str(ctx.exception))

    def test_markdown_hygiene_detects_bold_and_headers(self):
        raw_md = "# Big News\n\nThis is **very important** to read."
        warnings = check_markdown_hygiene(raw_md)
        self.assertEqual(len(warnings), 2)
        self.assertTrue(any("bold" in w for w in warnings))
        self.assertTrue(any("header" in w.lower() for w in warnings))

    def test_150_char_fold_auditing(self):
        short_hook = "Connect an AI agent directly to Google Ads and it will burn your daily budget."
        fits, msg = audit_150_char_fold(short_hook)
        self.assertTrue(fits)

        long_hook = (
            "This is an extremely long and bloated introduction that goes on and on without taking a breath, "
            "repeating buzzwords and marketing clichés until it stretches well past the one hundred and sixty character threshold "
            "and gets mercilessly truncated by the LinkedIn mobile app."
        )
        fits_long, _ = audit_150_char_fold(long_hook)
        self.assertFalse(fits_long)

    def test_dry_run_post_execution(self):
        client = LinkedInClient()
        req = LinkedInPostRequest(
            text="Connect an AI agent directly to Google Ads and it will burn your daily budget.",
            dry_run=True
        )
        res = client.publish_post(req)
        self.assertTrue(res.success)
        self.assertTrue(res.dry_run)
        self.assertEqual(res.status, "DRY_RUN_VALIDATED")
        self.assertIn("payload_preview", res.raw_response)

if __name__ == "__main__":
    unittest.main()

