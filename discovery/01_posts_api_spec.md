# Posts API

Warning

**Deprecation Notice:** The Marketing Version 202511 (Marketing November 2025) will be sunset on November 16, 2026. We recommend that you migrate to the latest [versioned APIs](../../versioning?view=li-lms-2026-10) to avoid disruptions. For information on all the supported versions, refer to the [migrations](../../integrations/migrations?view=li-lms-2026-10#api-migration-status) documentation. If you haven’t yet migrated and have questions, submit a request on the [LinkedIn Developer Support Portal](https://www.linkedin.com/help/linkedin/ask/dsapi).

The Posts API facilitates the creation and retrieval of organic and sponsored posts.

You can include various types of content in a post. The following table indicates the content types that support organic (non-sponsored) and sponsored posts.

| Content Types | Organic (non-sponsored) | Sponsored |
| --- | --- | --- |
| Text only | Yes | Yes |
| Images | Yes | Yes |
| Videos | Yes | Yes |
| Documents | Yes | Yes |
| Article | Yes | Yes |
| Carousels | No | Yes |
| MultiImage | Yes | No |
| Poll | Yes | No |
| [Celebration](celebration-post-api?view=li-lms-2026-10) | Yes | No |

Note

- The Posts API replaces the ugcPosts API. For more information, refer to the [Migration Guide](../contentapi-migration-guide?view=li-lms-2026-10).
- All APIs require the request header Linkedin-Version: {Version in YYYYMM format}. All APIs require the request header `X-Restli-Protocol-Version: 2.0.0`

## Permissions

| Permission | Description |
| --- | --- |
| w\_organization\_social | Post, comment, and like posts on behalf of an organization. Restricted to organizations where the authenticated member has one of the following company page roles: <br>- ADMINISTRATOR<br>- DIRECT\_SPONSORED\_CONTENT\_POSTER<br>- CONTENT\_ADMIN |
| r\_organization\_social | Retrieve organizations' posts, comments, and likes. Restricted to organizations in which the authenticated member has one of the following company page roles:<br>- ADMINISTRATOR<br>- DIRECT\_SPONSORED\_CONTENT\_POSTER<br>- CONTENT\_ADMIN |
| w\_member\_social | Post, comment, and like posts on behalf of an authenticated member. |
| r\_member\_social | Retrieve posts, comments, and likes on behalf of an authenticated member. This permission is **restricted** and is available to **approved users only**. |

For more information on company page roles, refer [Organization Access Control](../organizations/organization-access-control-by-role?view=li-lms-2026-10).

### Post Schema

For detailed schema information, refer [Post API Schema](post-api-schema?view=li-lms-2026-10#post-schema).

## Create a Post

- Create Organic Posts
- Reshare a Post
- Create Targeted Organic Posts
- Create Dark Posts

### Create Organic Posts

#### Text-Only Post Creation Sample Request

# [http](#tab/http)
```http
POST https://api.linkedin.com/rest/posts
```

```json
{
  "author": "urn:li:organization:5515715",
  "commentary": "Sample text Post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}
```

# [curl](#tab/curl)
```curl
curl -X POST 'https://api.linkedin.com/rest/posts' \
-H 'Authorization: Bearer {INSERT_TOKEN}' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Content-Type: application/json' \
--data '{
  "author": "urn:li:organization:5515715",
  "commentary": "Sample text Post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}'
```

---

You should get a 201 response and the response header x-restli-id contains the Post ID such as `urn:li:share:6844785523593134080` or `urn:li:ugcPost:68447855235931240`.

#### Single Post Creation Sample Request

The following methods are available for creating different types of posts:

- Creating a post with an image requires uploading an image asset to obtain an Image URN (urn:li:image:{id}) for use in the post. For more information, refer to the [Images API](images-api?view=li-lms-2026-10).
- Creating a post with a video requires uploading a video asset to obtain a Video URN (urn:li:video:{id}) for use in the post. For more information, refer to the [Videos API](videos-api?view=li-lms-2026-10).
- Creating a post with a document requires uploading a document asset to obtain a Document URN (urn:li:document:{id}) for use in the post. For more information, refer to the [Documents API](documents-api?view=li-lms-2026-10).

The following methods are available for creating different types of posts with multiple images:

- If you want to create an organic (non-sponsored) post with multiple images, refer to the [MultiImage API](multiimage-post-api?view=li-lms-2026-10).
- If you want to create a sponsored post with multiple images, refer to the [Carousel API](../../integrations/ads/advertising-targeting/version/carousel-ads-integrations?view=li-lms-2026-10).

# [http](#tab/http)
```http
POST https://api.linkedin.com/rest/posts
```

```json
{
  "author": "urn:li:organization:5515715",
  "commentary": "Sample video Post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "content": {
    "media": {
      "title":"title of the video",
      "id": "urn:li:video:C5F10AQGKQg_6y2a4sQ"
    }
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}
```

# [curl](#tab/curl)
```curl
curl -X POST 'https://api.linkedin.com/rest/posts' \
-H 'Authorization: Bearer {INSERT_TOKEN}' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Content-Type: application/json' \
--data '{
    "author": "urn:li:organization:5515715",
    "commentary": "Sample video Post",
    "visibility": "PUBLIC",
    "lifecycleState": "PUBLISHED",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "content": {
        "media": {
            "title":"title of the video",
            "id": "urn:li:video:C5F10AQGKQg_6y2a4sQ"
        }
    },
    "isReshareDisabledByAuthor": false
}'
```

---

You should get a 201 response and the response header x-restli-id contains the Post ID such as `urn:li:share:6844785523593134080` or `urn:li:ugcPost:68447855235931240`.

#### Poll Post Creation Sample Request

Only create non-sponsored poll posts. For more information, refer to the [Poll API](poll-post-api?view=li-lms-2026-10).

#### MultiImage Post Creation Sample Request

Only create non-sponsored multiImage posts. Multi-Image post is a post containing multiple images. For more information, refer to the [MultiImage API](multiimage-post-api?view=li-lms-2026-10).

#### Article Post Creation Sample Request

The Posts API does not support URL scraping for article post creation, as it introduces unpredictability in how a post will appear when created by API partners. Instead, API partners must set article fields such as thumbnail, title, and description within the post when creating an article post. To create an article post with thumbnail image, please use [Images API](images-api?view=li-lms-2026-10) to upload thumbnail image and use the ImageUrn on thumbnail field. For more information, refer to the [ArticleContent API](../../integrations/ads/advertising-targeting/version/article-ads-integrations?view=li-lms-2026-10#workflow).

# [http](#tab/http)
```http
POST https://api.linkedin.com/rest/posts
```

```json
{
 "author": "urn:li:organization:5515715",
 "commentary": "test article post",
 "visibility": "PUBLIC",
 "distribution": {
   "feedDistribution": "MAIN_FEED",
   "targetEntities": [],
   "thirdPartyDistributionChannels": []
 },
 "content": {
     "article": {
         "source": "https://lnkd.in/eabXpqi",
         "thumbnail": "urn:li:image:C49klciosC89",
         "title": "prod test title two",
         "description": "test description"
     }
 },
 "lifecycleState": "PUBLISHED",
 "isReshareDisabledByAuthor": false
}
```

# [curl](#tab/curl)
```curl
curl -X POST 'https://api.linkedin.com/rest/posts' \
-H 'Authorization: Bearer {INSERT_TOKEN}' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Content-Type: application/json' \
--data '{
 "author": "urn:li:organization:5515715",
 "commentary": "test article post",
 "visibility": "PUBLIC",
 "distribution": {
   "feedDistribution": "MAIN_FEED",
   "targetEntities": [],
   "thirdPartyDistributionChannels": []
 },
 "content": {
     "article": {
         "source": "https://lnkd.in/eabXpqi",
         "thumbnail": "urn:li:image:C49klciosC89",
         "title": "prod test title two",
         "description": "test description"
     }
 },
 "lifecycleState": "PUBLISHED",
 "isReshareDisabledByAuthor": false
}'
```

---

You should get a 201 response and the response header x-restli-id contains the Post ID such as `urn:li:share:6844785523593134080` or `urn:li:ugcPost:68447855235931240`.

#### Carousel Post Creation Sample Request

Only create sponsored carousel post. Organic carousel is currently not supported. For more information, refer to the [Carousel API](../../integrations/ads/advertising-targeting/version/carousel-ads-integrations?view=li-lms-2026-10).

#### Post Creation Response

The Post is created with a `201` response and the response header `x-restli-id` contains the `Post ID` such as `urn:li:share:6844785523593134080` or `urn:li:ugcPost:68447855235931240`.

### Reshare a post

#### Reshare Creation Request

The following example reshares a post (urn:li:share:6957408550713184256) on the main feed. You must specify `reshareContext.parent` field as shown in the request for resharing that post. `reshareContext.root` is the greatest ancestor of the post - can also be the parent. This read-only field is derived from the parent.

# [http](#tab/http)
```http
POST https://api.linkedin.com/rest/posts
```

```json
{
  "author": "urn:li:organization:5515715",
  "commentary": "Sample reshare post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false,
  "reshareContext": {
    "parent": "urn:li:share:6957408550713184256"
  }
}
```

# [curl](#tab/curl)
```curl
curl -X POST 'https://api.linkedin.com/rest/posts' \
-H 'Authorization: Bearer {INSERT_TOKEN}' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Content-Type: application/json' \
--data '{
  "author": "urn:li:organization:5515715",
  "commentary": "Sample text Post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false,
  "reshareContext": {
    "parent": "urn:li:share:6957408550713184256"
  }
}'
```

---

#### Reshare Creation Sample Response

The reshare is created with a `201` response and the response header `x-restli-id` contains the `Post ID` such as `urn:li:share:6844785523593134080` or `urn:li:ugcPost:68447855235931240`.

#### Reshare Get Response

When you fetch a reshare post, the response appears as follows.

```json
{
  "author": "urn:li:organization:5515715",
  "commentary": "Sample reshare post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false,
  "reshareContext": {
    "parent": "urn:li:share:6957408550713184256",
    "root": "urn:li:share:6957408550713184256"
  }
}
```

### Create Targeted Organic Posts

To increase the engagement and impact of your message, you can target organizational posts to a subset of your followers. You select a target audience within your company's existing follower base by using predefined criteria known as targeting facets.

Examples of possible targeting facets include geography, job function, industry, and seniority level. Refer to [Ads Targeting](../../integrations/ads/advertising-targeting/ads-targeting?view=li-lms-2026-10) and [Standardized Data](../../../shared/references/v2/standardized-data?view=li-lms-2026-10&amp;context=linkedin/marketing/context) to create a segment of a specific audience you want to target.

The audience you target for your UGC Post must be greater than 300 members. Use the [Audience Counts API](../../integrations/ads/advertising-targeting/audience-counts?view=li-lms-2026-10) to calculate the approximate size of your audience. Make sure to pass in your organization URN in the `followedCompanies` field of the `targetingFacet` parameter so your audience count is filtered down to only members who follow your company.

#### Sample Request for Audience Count

# [http](#tab/http)
```http
GET https://api.linkedin.com/rest/audienceCounts?q=targetingCriteria&target.includedTargetingFacets.industries[0]=urn:li:industry:4&target.includedTargetingFacets.seniorities[0]=urn:li:seniority:3&target.includedTargetingFacets.locations[0]=urn:li:geo:103644278&target.includedTargetingFacets.followedCompanies[0]=urn:li:organization:2414183
```

# [curl](#tab/curl)
```curl
curl -X GET 'https://api.linkedin.com/rest/audienceCounts?q=targetingCriteria&target.includedTargetingFacets.industries[0]=urn:li:industry:4&target.includedTargetingFacets.seniorities[0]=urn:li:seniority:3&target.includedTargetingFacets.locations[0]=urn:li:geo:103644278&target.includedTargetingFacets.followedCompanies[0]=urn:li:organization:2414183' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Authorization: Bearer {INSERT_TOKEN}'
```

---

#### Sample Response

```json
{
    "elements": [
        {
            "active": 0,
            "total": 380
        }
    ],
    "paging": {
        "count": 10,
        "links": [],
        "start": 0
    }
}
```

In this example, since the audience size exceeds 300, you can create a targeted organic UGC Post with the targeting details in the targetEntities object. The targetEntities object is structured as an array that accepts a single object, which contains multiple targeting entity arrays. Each targeting facet array accepts targeting entity URNs. Refer to the following sample request for an example.

#### Organic Targeted Post Creation Sample Request

Demonstrates how to create an organic video post targeting `urn:li:geo:103644278` (geo-target) and `urn:li:seniority:3`.

# [http](#tab/http)
```http
POST https://api.linkedin.com/rest/posts
```

```json
{
  "author": "urn:li:organization:5515715",
  "commentary": "Sample targeted video Post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [{
                "geoLocations": [
                    "urn:li:geo:103644278"
                ],
                "seniorities": [
                    "urn:li:seniority:3"
                ]
            }],
    "thirdPartyDistributionChannels": []
  },
  "content":{
    "media":{
      "title":"title of the video",
      "id": "urn:li:video:C5F10AQGKQg_6y2a4sQ"
      }
    },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}
```

# [curl](#tab/curl)
```curl
curl -X POST 'https://api.linkedin.com/rest/posts \
-H 'Authorization: Bearer {INSERT_TOKEN}' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Content-Type: application/json' \
--data '{
  "author": "urn:li:organization:5515715",
  "commentary": "Sample targeted video Post",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [{
                "geoLocations": [
                    "urn:li:geo:103644278"
                ],
                "seniorities": [
                    "urn:li:seniority:3"
                ]
            }],
    "thirdPartyDistributionChannels": []
  },
  "content":{
    "media":{
      "title":"title of the video",
      "id": "urn:li:video:C5F10AQGKQg_6y2a4sQ"
      }
    },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}'
```

---

### Create Dark Posts

Dark posts are used to create content that doesn't appear as organic content on a LinkedIn company page. Dark posts can be used in Ad Campaigns as DSC. For more information, refer to the [Direct Sponsored Content Overview](https://www.linkedin.com/help/lms/answer/49014).

- Create a dark post using an `author` as an organization `urn:li:organization:{id}`, `visibility` as `PUBLIC`, `feedDistribution` as `NONE`, and setting details of the `adContext` type.
- Dark posts can be created as inline posts for usage in an ad campaign. For more information, refer to the [Video Ads](../../integrations/ads/advertising-targeting/create-and-manage-video?view=li-lms-2026-10).
- When a UGC Post is published (`"lifecycleState": "PUBLISHED"`), an authorized member can view the post using the follow URL structure: `https://www.linkedin.com/feed/update/urn:li:ugcPost:<id>/`

## Get Posts by URN

To retrieve posts, use URNs such as: `ugcPostUrn``(urn:li:ugcPost:{id})` or `shareUrn``(urn:li:share:{id})`.

Note

Also provide an optional parameter, `viewContext` to all GET, BATCH\_GET, and Finders to retrieve posts. By default, `viewContext` is `READER`, which specifies the version of the post that has been published and is viewable to a general audience.

The `AUTHOR` viewContext can be used to retrieve the latest version of a post, which has not yet been published; it can be in a number of possible states such as: `PUBLISHED`, `DRAFT` or `PROCESSING`.

Note

Use the [Images API](images-api?view=li-lms-2026-10) and [Videos API](videos-api?view=li-lms-2026-10) to retrieve additional details about image and video assets such as the downloadUrl for article thumbnails.

Note

URNs included in the URL params must be URL encoded. Example: `urn:li:ugcPost:12345` becomes `urn%3Ali%3AugcPost%3A12345`.

#### Sample Request

# [http](#tab/http)
```http
GET https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}
```

# [curl](#tab/curl)
```curl
curl -X GET 'https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}?viewContext=AUTHOR' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Authorization: Bearer {INSERT_TOKEN}'
```

---

If your request exceeds the [maximum length requirement](../../../shared/api-guide/concepts/query-tunneling?view=li-lms-2026-10), please utilize query tunneling:

```curl
curl -X POST 'https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn} \
-H 'Authorization: Bearer redacted' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
--data 'viewContext=AUTHOR'
```

#### Sample Response

```json
{
  "lifecycleState": "PUBLISHED",
  "lastModifiedAt": 1634790968774,
  "visibility": "PUBLIC",
  "publishedAt": 1634790968774,
  "author": "urn:li:organization:5515715",
  "distribution": {
    "feedDistribution": "NONE",
    "thirdPartyDistributionChannels": []
  },
  "content": {
    "media": {
      "id": "urn:li:video:C5F10AQGKQg_6y2a4sQ"
    }
  },
  "lifecycleStateInfo": {
    "isEditedByAuthor": false
  },
  "isReshareDisabledByAuthor": false,
  "createdAt": 1634790968743,
  "id": "urn:li:ugcPost:6856810298419044352",
  "commentary": "comment on Oct 20",
  "adContext": {
    "dscStatus": "ACTIVE",
    "dscAdType": "VIDEO",
    "isDsc": true,
    "dscAdAccount": "urn:li:sponsoredAccount:520866471"
  }
}
```

## Batch Get Posts

Multiple posts can be retrieved and viewed in a single API call by passing multiple UGC Post or share URNs into the ids parameter. The UGC Post URNs should be passed in List format and encoded as shown in the examples.

Note

Make sure to add header `X-RestLi-Method` with value of `BATCH_GET` in the request. The comma `(,)` separating each URN in the `List` does not need to be encoded.

#### Sample Request

# [http](#tab/http)
```http
GET https://api.linkedin.com/rest/posts?ids=List({encoded ugcPostUrn},{encoded ugcPostUrn})
```

# [curl](#tab/curl)
```curl
curl -X GET 'https://api.linkedin.com/rest/posts?ids=List({encoded ugcPostUrn},{encoded ugcPostUrn})' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'X-RestLi-Method: BATCH_GET' \
-H 'Authorization: Bearer {INSERT_TOKEN}'
```

---

#### Sample Response

```json
{
    "results": {
        "urn:li:share:6844785523593134080": {
            "lifecycleState": "PUBLISHED",
            "lastModifiedAt": 1631924039162,
            "visibility": "PUBLIC",
            "publishedAt": 1631924038940,
            "author": "urn:li:organization:5515715",
            "distribution": {
                "feedDistribution": "NONE",
                "thirdPartyDistributionChannels": []
            },
            "content": {},
            "lifecycleStateInfo": {
                "isEditedByAuthor": false
            },
            "isReshareDisabledByAuthor": true,
            "createdAt": 1631924038940,
            "id": "urn:li:share:6844785523593134080",
            "commentary": "Test Org commentary-Updated Config"
        }
    },
    "statuses": {},
    "errors": {}
}
```

## Find Posts by Authors

Retrieve all posts for a member or organization using the following parameters.

```http
GET https://api.linkedin.com/rest/posts?author={encoded PersonURN|OrganizationURN}
```

| Field | Format | Description | Required |
| --- | --- | --- | --- |
| author | Person URN or Organization URN | Author of the post (can be either posted from a member or their company page). | Required |
| viewContext | enum: `READER` or `AUTHOR` | The viewContext in which you're looking at the posts. Use `AUTHOR` when viewing post as the author of the post and `READER` when viewing post as the a non-author. By default, `viewContext` is `READER`, which specifies the version of the post that has been published and is viewable to general audience. | Optional (Default=`READER`) |
| start | int | The index of the first item you want results for. | Optional (Default=0) |
| count | int | The number of items you want included on each page of results. There could be fewer items remaining than the value you specify. The default is 10 and maximum allowed count is 100. | Optional (Default=10) |
| sortBy | enum: `LAST_MODIFIED` or `CREATED` | The sort order for the results in descending order. `LAST_MODIFIED` (for last modified time) or `CREATED` (for created time). | Optional (Default=`LAST_MODIFIED`) |

Note

To retrieve all posts authored by a person, `r_member_social` permission is required. Refer to [Retrieve Current Member's Profile API](../../../shared/integrations/people/profile-api?view=li-lms-2026-10#retrieve-current-members-profile) to fetch their `id` and construct a Person URN in the format of `urn:li:person:{id}`. To retrieve all posts authored by an organization, `r_organization_social` permission is required. Refer to [Find a Member's Organization API](../organizations/organization-access-control-by-role?view=li-lms-2026-10#find-a-members-organization-access-control-information) to fetch their `organization` and validate their organization access role. By default, all Posts API finder results are sorted by post last modified time (`lastModifiedAt` field) in descending order (latest to oldest). Configure this using the optional `sortBy` param. `isDsc` parameter has been deprecated. Previously, `isDsc=true` returned sponsored posts only and `isDsc=false` returned both organic and sponsored posts. Now, by default, it will return both organic and sponsored posts together (same behaviour as `isDsc=false`). This matches the legacy /ugcPosts author finder endpoint's behavior. Receive less than the `count` number of results in a page, when there are more posts available in the subsequent paginated requests. The `links` field in the response will provide a link to the next page for more posts.

#### Sample Request

# [http](#tab/http)
```http
GET https://api.linkedin.com/rest/posts?author={urn%3Ali%3Aperson%3A5abc_dEfgH or urn%3Ali%3Aorganization%3A2414183}&q=author&count=10&sortBy=LAST_MODIFIED
```

# [curl](#tab/curl)
```curl
curl -X GET 'https://api.linkedin.com/rest/posts?author={urn%3Ali%3Aperson%3A5abc_dEfgH or urn%3Ali%3Aorganization%3A2414183}&q=author&count=10&sortBy=LAST_MODIFIED' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'X-RestLi-Method: FINDER' \
-H 'Authorization: Bearer {INSERT_TOKEN}'
```

---

#### Sample Response

```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "links": []
  },
  "elements": [
    {
      "lifecycleState": "PUBLISHED",
      "lastModifiedAt": 1634817395768,
      "visibility": "PUBLIC",
      "publishedAt": 1634817394721,
      "author": "urn:li:organization:2414183",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "thirdPartyDistributionChannels": []
      },
      "content": {},
      "lifecycleStateInfo": {
        "isEditedByAuthor": false
      },
      "isReshareDisabledByAuthor": false,
      "createdAt": 1634817394721,
      "id": "urn:li:share:6856921137721544704",
      "commentary": ""
    },
    {
      "lifecycleState": "PUBLISHED",
      "lastModifiedAt": 1634814069101,
      "visibility": "PUBLIC",
      "publishedAt": 1634813460041,
      "author": "urn:li:organization:2414183",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "thirdPartyDistributionChannels": []
      },
      "lifecycleStateInfo": {
        "isEditedByAuthor": false
      },
      "isReshareDisabledByAuthor": false,
      "createdAt": 1634813460041,
      "id": "urn:li:share:6856904634360066048",
      "commentary": ""
    }
  ]
}
```

## Find Posts by Account

Retrieve all posts with the specific Sponsored Account and the content types with the following parameters:

| Field | Format | Description | Required |
| --- | --- | --- | --- |
| dscAdAccount | URN: Sponsored Ad Account | URN of the DSC Ad Account associated with a post | Required |
| viewContext | enum `READER` or `AUTHOR` - Default=`READER` | viewContext in which you're looking at the posts | Optional |
| dscAdTypes | record of list [dscAdType](post-api-schema?view=li-lms-2026-10#dscadtype) | DSC ad types to search for | Optional |

#### Sample Request

# [http](#tab/http)
```http
GET https://api.linkedin.com/rest/posts?dscAdAccount={encode dscAdAccount}&q=dscAdAccount&dscAdTypes=List(STANDARD,VIDEO)
```

# [curl](#tab/curl)
```curl
curl -X GET 'https://api.linkedin.com/rest/posts?dscAdAccount={encode dscAdAccount}&q=dscAdAccount&dscAdTypes=List(STANDARD,VIDEO)' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'X-RestLi-Method: FINDER' \
-H 'Authorization: Bearer {INSERT_TOKEN}'
```

---

#### Sample Response

```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "links": []
  },
  "elements": [
    {
      "lifecycleState": "PUBLISHED",
      "lastModifiedAt": 1634817395768,
      "visibility": "PUBLIC",
      "publishedAt": 1634817394721,
      "author": "urn:li:organization:2414183",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "thirdPartyDistributionChannels": []
      },
      "content": {},
      "lifecycleStateInfo": {
        "isEditedByAuthor": false
      },
      "isReshareDisabledByAuthor": false,
      "createdAt": 1634817394721,
      "id": "urn:li:share:6856921137721544704",
      "commentary": ""
    },
    {
      "lifecycleState": "PUBLISHED",
      "lastModifiedAt": 1634814069101,
      "visibility": "PUBLIC",
      "publishedAt": 1634813460041,
      "author": "urn:li:organization:2414183",
      "distribution": {
        "feedDistribution": "MAIN_FEED",
        "thirdPartyDistributionChannels": []
      },
      "lifecycleStateInfo": {
        "isEditedByAuthor": false
      },
      "isReshareDisabledByAuthor": false,
      "createdAt": 1634813460041,
      "id": "urn:li:share:6856904634360066048",
      "commentary": ""
    }
  ]
}
```

## Update Posts

When you perform an update, the header `X-RestLi-Method` must be included in the request and set to `PARTIAL_UPDATE`.

Only the following `posts` fields are available to update through the Posts API.

| Field | Description |
| --- | --- |
| commentary | The user generated commentary of this post in `little` format |
| contentCallToActionLabel | The call to action label that a member can act on that opens a landing page, that can be associated with the content. If empty, then there's no call to action associated with the content |
| contentLandingPage | URL of the landing page |
| lifecycleState | The state of the content. PUBLISHED is the only accepted field during creation. The following values can be returned in responses: <br>- DRAFT - Represents content that's accessible only to the author and is not yet published.<br>- PUBLISHED - Represents content that's accessible to all entities. This is the only accepted field during creation.<br>- PUBLISH\_REQUESTED - Represents content that has been submitted for publishing but is not yet ready for rendering. The content will be published asynchronously once the processing has successfully completed.<br>- PUBLISH\_FAILED - Represents content that has been submitted for publishing but was not processed. An edit is required in order to re-attempt publishing. |
| adContext | - dscName: Update the name of the sponsored content<br>- dscStatus: Update the status of the sponsored content |

# [http](#tab/http)
```http
POST 'https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}' 
```

```json
{
    "patch":
    {
        "$set":
        {
            "commentary": "Update to the post",
            "contentCallToActionLabel": "LEARN_MORE"
        },
        "adContext":
        {
            "$set":
            {
                "dscName": "Updating name!"
            }
        }
    }
}
```

# [curl](#tab/curl)
```curl
curl -X POST 'POST 'https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}' \
-H 'Authorization: Bearer {INSERT_TOKEN}' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Content-Type: application/json \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'X-RestLi-Method: PARTIAL_UPDATE' \
--data '{
"patch": 
  {
        "$set":
        {
            "commentary": "Update to the post",
            "contentCallToActionLabel": "LEARN_MORE"
        },
        "adContext":
        {
            "$set":
            {
                "dscName": "Updating name!"
            }
        }
    }
}'
```

---

A successful response returns a `204` code.

## Delete Posts

Post deletions are idempotent. Deletion requests for a previously deleted UGC Post will return a `204` code - No Content.

Important

Batch delete of Posts is not supported.

#### Sample Request

# [http](#tab/http)
```http
DELETE https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}
```

# [curl](#tab/curl)
```curl
curl -X DELETE 'https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'X-RestLi-Method: DELETE' \
-H 'Authorization: Bearer {INSERT_TOKEN}'
```

---

A successful response returns a 204 code notification.

## Mentions and Hashtags using Posts commentary

The Posts API has a commentary field that can be used to mention or hashtag of other Linkedin entities, such as organizations or members. To specify an annotation, provide the URN for the referenced entity and indicate which part of the text should be rendered as a link to that entity.

The text linking to the annotated entity must match the name of the member or organization for link conversion. Matching is case sensitive. If there's no match, text appears as normal text. This includes cases where the provided text length is longer or shorter than the name of the member or organization. The exception to this is member annotations. Member annotations only need to match one name in the full text naming. For example, consider the name `Jane Smith`. A share can match either on `Jane`, `Smith`, or `Jane Smith`.

Organization mentions can be schools (such as Universities), organization brands (previously known as Showcase Pages), and Organizations (companies). Organization annotations must match the full name.

#### Sample Objects

##### Organization URN Examples

- `urn:li:organization:11832` (School - Boise State University)
- `urn:li:organization:2414183` (Organization - Devtestco)

#### Mention an Organization

In the following example, `Devtestco` is being tagged.

# [http](#tab/http)
```http
POST https://api.linkedin.com/rest/posts
```

```json
{
  "author": "urn:li:organization:123456789",
  "commentary": "Hello @[Devtestco](urn:li:organization:2414183)",
  "visibility": "PUBLIC",
  "distribution": {
      "feedDistribution": "MAIN_FEED",
      "targetEntities": [],
      "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}
```

# [curl](#tab/curl)
```curl
curl -X POST 'https://api.linkedin.com/rest/posts' \
-H 'Authorization: Bearer {INSERT_TOKEN}' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Content-Type: application/json' \
--data '{
  "author": "urn:li:organization:123456789",
  "commentary": "Hello @[Devtestco](urn:li:organization:2414183)",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
    },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}'
```

---

The Post is created with a `201` response and the response header `x-restli-id` contains the Post ID such as `urn:li:share:6844785523593134080` or `urn:li:ugcPost:68447855235931240`.

### Get Posts by URN For above mentioned Organization

To retrieve posts, use URNs such as: `ugcPostUrn``(urn:li:ugcPost:{id})` or `shareUrn``(urn:li:share:{id})` as shown in the previous example post.

#### Sample Request

# [http](#tab/http)
```http
GET https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}
```

# [curl](#tab/curl)
```curl
curl -X GET 'https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}?viewContext=AUTHOR' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Authorization: Bearer {INSERT_TOKEN}'
```

---

#### Sample Response

```json
{
   "isReshareDisabledByAuthor": false,
   "createdAt": 1636669884769,
   "lifecycleState": "PUBLISHED",
   "lastModifiedAt": 1636669884769,
   "visibility": "PUBLIC",
   "publishedAt": 1636669884769,
   "author": "urn:li:organization:18799005",
   "id": "urn:li:share:6864691044148133888",
   "distribution": {
       "feedDistribution": "MAIN_FEED",
       "thirdPartyDistributionChannels": []
   },
   "commentary": "Hello @[Devtestco](urn:li:organization:2414183)",
   "lifecycleStateInfo": {
       "isEditedByAuthor": false
   }
}
```

Note

Organization mention data is returned in the commentary field.

#### Hashtag a keyword

In the following example, `coding` is being tagged.

# [http](#tab/http)
```http
POST https://api.linkedin.com/rest/posts
```

```json
{
   "author": "urn:li:organization:123456789",
   "commentary": "Follow best practices #coding",
   "visibility": "PUBLIC",
   "distribution": {
       "feedDistribution": "MAIN_FEED",
       "targetEntities": [],
       "thirdPartyDistributionChannels": []
   },
   "lifecycleState": "PUBLISHED",
   "isReshareDisabledByAuthor": false
}
```

# [curl](#tab/curl)
```curl
curl -X POST 'https://api.linkedin.com/rest/posts' \
-H 'Authorization: Bearer {INSERT_TOKEN}' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Content-Type: application/json' \
--data '{
  "author": "urn:li:organization:123456789",
  "commentary": "Follow best practices #coding",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
    },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}'
```

---

The Post is created with a `201` response and the response header `x-restli-id` contains the Post ID such as `urn:li:share:6844785523593134080` or `urn:li:ugcPost:68447855235931240`.

### Get Posts by URN For above Hashtag of the keyword

To retrieve posts, use URNs such as: `ugcPostUrn``(urn:li:ugcPost:{id})` or `shareUrn``(urn:li:share:{id})` from the previous created post example.

#### Sample Request

# [http](#tab/http)
```http
GET https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}
```

# [curl](#tab/curl)
```curl
curl -X GET 'https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}?viewContext=AUTHOR' \
-H 'X-Restli-Protocol-Version: 2.0.0' \
-H 'Linkedin-Version: {version number in the format YYYYMM}' \
-H 'Authorization: Bearer {INSERT_TOKEN}'
```

---

#### Sample Response

```json
{
   "isReshareDisabledByAuthor": false,
   "createdAt": 1636688348505,
   "lifecycleState": "PUBLISHED",
   "lastModifiedAt": 1636688348559,
   "visibility": "PUBLIC",
   "publishedAt": 1636688348505,
   "author": "urn:li:organization:18799005",
   "id": "urn:li:share:6864768486615375872",
   "distribution": {
       "feedDistribution": "MAIN_FEED",
       "thirdPartyDistributionChannels": []
   },
   "commentary": "Follow best practices {hashtag|\\#|coding}",
   "lifecycleStateInfo": {
       "isEditedByAuthor": false
   }
}
```

Note

The commentary field hashtag data is returned with a template. For more information about the hashtag template, refer to the [little Text Format](little-text-format?view=li-lms-2026-10#hashtagtemplate).

## Enable or Disable Comments Section on a Post

To enable or disable the comments section on a post, refer to the [Social Metadata API](social-metadata-api?view=li-lms-2026-10#enable-or-disable-comments-on-a-thread) using share or UGC URN.

## API Error Details

| HTTP Status Code | Error Message | Description |
| --- | --- | --- |
| 400 | INVALID\_URN\_TYPE | `{field}` value `{value}` must be a `{urnType}` URN. Verify the URN type used for fields such as `author` or `content.media.id`. |
| 400 | INVALID\_URN\_ID | The URN ID provided is invalid. Check the format of any URNs in the request. |
| 400 | MISSING\_FIELD | A required field is missing. Ensure all required fields such as `author`, `visibility`, `distribution`, and `lifecycleState` are present. |
| 400 | INVALID\_VALUE\_FOR\_FIELD | `{field}` cannot be set to `{value}`. Verify that enum values for fields such as `visibility`, `feedDistribution`, and `lifecycleState` are valid. |
| 400 | FIELD\_LENGTH\_TOO\_LONG | `{field}` length exceeds the allowed maximum. Reduce the length of the `commentary` or other text fields. |
| 400 | INVALID\_VALUE\_BLANK\_FIELD | `{field}` cannot be blank. Ensure required string fields are not empty. |
| 401 | EMPTY\_ACCESS\_TOKEN | Empty or missing OAuth2 access token. Include a valid token in the `Authorization` header. |
| 403 | ACCESS\_DENIED | Insufficient permissions to perform the requested action. Ensure the required OAuth scope (`w_organization_social`, `w_member_social`, `r_organization_social`, or `r_member_social`) is granted and that the authenticated member has the necessary company page role. |
| 404 | NOT\_FOUND | The requested post was not found. Verify that the URN provided in the request is correct. |
| 409 | CONFLICT | A write conflict occurred. Retry the request. |
| 422 | UNPROCESSABLE\_ENTITY | The request was well-formed but could not be processed due to semantic errors. Review field values for logical consistency. |
| 429 | TOO\_MANY\_REQUESTS | The API rate limit has been exceeded. Reduce request frequency and retry after a delay. |
| 500 | INTERNAL\_SERVER\_ERROR | An unexpected server-side error occurred. Retry the request. If the issue persists, contact LinkedIn support. |
| 503 | SERVICE\_UNAVAILABLE | The service is temporarily unavailable. Retry the request after a brief delay. |