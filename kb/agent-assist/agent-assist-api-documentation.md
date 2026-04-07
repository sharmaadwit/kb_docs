---
source_url: https://console-docs.gupshup.io/docs/agent-assist-api-documentation
---

# Agent Assist API Documentation

This page summarizes **Agent Assist–related HTTP APIs** extracted from the product API documentation: **Transcript API**, **External Agent Assignment API**, **Business Hours API**, and **Tags API**. Base URLs use placeholders such as `{brandURL}` or `{brandName}` as deployed for your tenant.

## Version history

| Version | Details | Date | Author |
|--------|---------|------|--------|
| 2.0 | Transcript API, Business Hours API, External Assignment API & Tags API | 09/12/23 | — |

## Transcript API

**Methods supported:** `POST`  
**Authorization:** `apiKey` (header)

### Request body (POST)

Fields may be multi-valued to filter search. Important fields include:

- `startDate`, `endDate` (epoch millis)
- `pageSize`, `currentPage`
- `sessionIds`

### GET transcript

- **URL:** `https://{brandURL}/mgateway/v1/transcript`
- **Limitation:** `pageSize` maximum **50**.

**Query parameters** (names may match UI configuration):

| Param | Description | Mandatory |
|-------|-------------|-----------|
| `startDate` | Start of transcript range (epoch millis) | Yes |
| `endDate` | End of transcript range (epoch millis) | Yes |
| `pageSize` | Sessions per page | Yes |
| `currentPage` | Page index | Yes |
| `sessionIds` | Session IDs to fetch | No |

**Headers:**

| Type | Description | Mandatory |
|------|-------------|-----------|
| `apiKey` | Brand API key | Yes |

**Sample cURL (POST):**

```bash
curl --location 'https://{brandURL}/mgateway/v1/transcript' \
  --header 'Content-Type: application/json' \
  --header 'apiKey: {apiKey}' \
  --data '{
    "startDate": 1667673000000,
    "endDate": 1667759400000,
    "pageSize": "25",
    "currentPage": 1,
    "sessionIds": "{sessionId1},{sessionId2}"
  }'
```

### Transcript API responses

- **200 OK:** Chat data for requested sessions; includes fields such as `sessionStartTime`, `sessionEndTime`, `assignedTo`, `conversation`, `tagsName`, `chatFields`, etc.
- **400:** Invalid API key, `pageSize` > 50, or more than 50 `sessionIds` in body.
- **500:** Internal server error when request body data is incorrect.

## External Agent Assignment API

**Methods supported:** `GET`, `POST`  
**Authorization:** None, Basic, or Bearer token (configurable).

### GET

- **URL pattern:** `https://<Client URL>?key1=value1&key2=value2`
- **Example:** `https://abc.com/whatsapp/api?phoneNo=918010264005&email=abc@gmail.com`

Query/body fields may include customer identifiers (e.g. phone, chat fields such as `leadId`, customer fields such as `email`) depending on UI configuration.

**Responses** may include:

- Team name: `{ "teamName": "Team name" }`
- Agent email: `{ "agentEmail": "agentEmail Address" }`

### POST

- **URL:** `https://<Client URL>`  
- Example: `https://abc.com/whatsapp/api`  
- Body parameters mirror the GET query fields (phone, chat fields, customer fields) as configured.

Sample cURL patterns are documented for None, Basic, and Bearer authorization.

## Business Hours API

### Check in business hour

**Method:** `GET`  
**Authorization:** API key

Validates whether a timestamp falls within configured business hours. Response is boolean (`true` / `false`).

**Example URL:**

`https://{{brandName}}.onedirect.in/mgateway/public/v1/checkInBusinessHour?businessHourId=13102&timeZone=Africa%2FAbidjan&actionTimeStamp=1702037192000`

**Query parameters:**

| Param | Description | Mandatory |
|-------|-------------|-----------|
| `businessHourId` | Business hour ID | Yes |
| `timeZone` | Time zone | Yes |
| `actionTimeStamp` | Timestamp to evaluate | Yes |

**Header:** `apiKey`

**Sample response field:** `isBusinessHour` — `true` or `false`.

### Get business hours

**Method:** `GET`  
**Authorization:** API key  

Retrieves all system business hours.

**Example URL:** `https://{{brandName}}.onedirect.in/mgateway/public/v1/getBusinessHours`

**Response** includes lists with fields such as `businessHourId`, `businessHourName`.

## Tags API

**Method:** `POST`  
**Authorization:** API key  

Adds tags to a customer profile using channel, brand account, customer ID, and tag lists (`chatTags`, `customerTags`).

**Example URL:** `https://<BrandName/projectId>.onedirect.in/kong/mgateway/public/v1/tag/add`

**Body parameters (examples):**

| Param | Description | Mandatory |
|-------|-------------|-----------|
| `channel` | Channel (e.g. PROXY) | Yes |
| `brandAccount` | Brand account id | Yes |
| `customerId` | Customer ID | Yes |
| `chatTags` | Array of chat tags | No |
| `customerTags` | Array of customer tags | No |

**Sample response** includes `sessionId`, updated `chatTags` / `customerTags`, and `responseMsg`.
