# Verified on LinkedIn – Overview

The Verified on LinkedIn API allows you to access trusted verification signals from LinkedIn members, enabling you to display verified identity and workplace information directly within your platform.

Today, more than **100 million LinkedIn members** have confirmed their identity with a government-issued ID or verified their workplace using a company email. [Read more about LinkedIn verifications](https://www.linkedin.com/help/linkedin/answer/a1359065).

Build trust and authenticity into your platform by leveraging LinkedIn's verification ecosystem, helping you distinguish real professionals from fraudulent accounts.

##### Watch the Verified on LinkedIn overview video

## Try it Now - It only takes 10 minutes

It just takes **10 minutes** to make your first API call. Refer to our [Quickstart Guide](guides/quickstart).

## Use Cases

### What Verified on LinkedIn Can Be Used For

| Category | Examples |
| --- | --- |
| **Trust & Safety** | Professional communities, networking platforms, online marketplaces, peer-to-peer exchanges |
| **Communities & Networks** | Event registration, professional conferences, community moderation, alumni groups |
| **Marketplaces** | Buyer/seller verification, freelance platforms, service-sharing, resale platforms |

### What Verified on LinkedIn Cannot Be Used For

The API is designed for **trust enhancement**, not **regulatory compliance** or **eligibility decisions**. Use of the API is subject to LinkedIn's **Developer Terms and Verification Policies**.

| Restricted Use Case | Reason |
| --- | --- |
| **Hiring or employment decisions** | Not an employment screening tool. Do not use to rank or approve candidates. |
| **Background checks** | Does not include criminal, financial, or government background data. |
| **Credit, loans, or insurance** | Not related to creditworthiness or insurability. |
| **Housing eligibility** | Cannot be used for rental or housing determinations. |
| **Fintech or banking KYC** | Not a regulated KYC/AML service. |
| **Government or regulated identity checks** | Not a substitute for official ID verification systems. |
| **Platform safety or risk scoring** | Should complement — not replace your platform's trust and risk systems. |

## Verification Types

| Type | Description | Methods | Data Available |
| --- | --- | --- | --- |
| **Identity Verification** | Confirms the member's real identity | Government-issued ID | Verified Categories (all tiers), Verification details (Plus tier) |
| **Workplace Verification** | Confirms current association with a company | Work email, Microsoft Entra Verified ID | Verified Categories (all tiers), Organization details (Plus tier) |

## How It Works

- **Member Authorizes**: Grants your app permission to access their LinkedIn verification data via OAuth 2.0.
- **Fetch Verification Data**: Call LinkedIn APIs to retrieve verification status and profile information.
- **Optional Re-verification**: The `/verificationReport` API also supports the optional `verifiedWithinDays` query parameter, allowing your application to periodically prompt members to re-verify while continuing to display their existing verification data.
- **Display Verification Badges**: Show "Verified on LinkedIn" badges in your UI following our [branding guidelines](branding-ux-guidelines) if the member is verified.

## Quick Navigation

### By Role

| Who You Are | Where to Start |
| --- | --- |
| **Developer** | Pick a quickstart → [API Reference](api-reference/identity-me) → [Implementation Guide](guides/implementation-guide) |
| **Product Manager** | [Quickstart (Development Tier)](guides/quickstart) |
| **Marketing & Design** | [Branding Guidelines](branding-ux-guidelines) → Use Cases |

### By Goal

| I Want To... | Go Here |
| --- | --- |
| **Test the API quickly** | [Quickstart (Development Tier)](guides/quickstart) - 10 minutes |
| **Get enterprise features** | [Plus Tier Quickstart](guides/plus-tier/quickstart) |
| **See API docs** | [API Reference](api-reference/identity-me) |
| **Understand use cases** | Use Cases |
| **Display badges correctly** | [Branding Guidelines](branding-ux-guidelines) |

## API Reference

Both tiers use the same API endpoints with different access levels:

| API | Purpose | Development | Plus |
| --- | --- | --- | --- |
| **[/identityMe](api-reference/identity-me)** | Profile data | Basic profile | Basic profile + current Experience + recent Education |
| **[/verificationReport](api-reference/verification-report)** | Verification status | Categories only | Categories + Verification details |
| **[/validationStatus](api-reference/validation-status)** | Bulk validation | ❌ | Validation statuses of Profile + Verification Information |

[View complete API reference →](api-reference/authentication)

## Getting Started

### Step 1: Follow the Quickstart

- **[Quickstart (Development Tier)](guides/quickstart)** - Test with developer app admins (10 min)
- **[Plus Tier Quickstart](guides/plus-tier/quickstart)** - Enterprise features

### Step 2: Implement & Launch

- Follow the [Implementation Guide](guides/implementation-guide) for API Integration, OAuth, testing, and production best practices.
- Review [Branding Guidelines](branding-ux-guidelines)
- Check our [FAQ](faq) for common questions

## Support & Resources

### Documentation

- **[API Reference](api-reference/authentication)** - Complete API documentation
- **[Common FAQ](faq)** - Frequently asked questions
- **[Release Notes](release-notes)** - API updates and changes

### Tools

- **[Sample App](https://voli-app.dev/)** - Test OAuth flow and API calls
- **[Developer Portal](https://www.linkedin.com/developers/apps)** - Manage your applications
- **[OAuth Tool](https://www.linkedin.com/developers/tools/oauth)** - Generate test tokens

### Help

- **[LinkedIn API Status](https://www.linkedin-apistatus.com/)** - Monitor API health
- **[Partner Support](faq)** - Get help from LinkedIn team