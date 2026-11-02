# Using the Conversions API Payload Builder
## Procedure
8.  Note
 Use the standard `ISO 4217` currency code.
9. (Optional) If you want to use deduping, provide the `eventId` in the **Event Data** field. 
9.  Note
 In the right-side **Code** section, the payload is rendered in both **JSON** and **cURL** based on the parameters you have added.
10. (Optional) To make an API call with the payload:
10.1. In the **Make an API Call** section, choose an app. **Note:** Use the **Generate OAuth access token** option to generate a LinkedIn access token for an app that has access to the Conversions API. Alternatively, you can use an existing OAuth access token that has the following permission scopes: `r_ads`, `rw_conversions`.
10.2. Enter your **OAuth access Token** or generate a new one.
10.3. Select the required **Ad Account** from the dropdown. **Note:** Ensure that the ad account contains at least one conversion rule. If you don't have an ad account, refer to [Create Ad Account](https://www.linkedin.com/help/linkedin/answer/a426102/create-an-ad-account-in-campaign-manager-as-a-new-advertiser) to create one. To create a conversion rule, see [create a conversion rule](https://www.linkedin.com/help/lms/answer/a1657171).
11. Choose the required Conversion rule from the dropdown.
12. Select **Call API** to execute the request.. Now view the following upon choosing to call the API:
13. View the payload in the **Code** section, which can be used for further consumption.
14. The API response will be displayed in the **Response** panel.
15. The event gets created in the production environment.