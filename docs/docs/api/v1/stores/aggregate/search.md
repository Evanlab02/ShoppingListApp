# Store Aggregation - With Search

**NOTE: The OpenAPI reference at `/api/v1/docs` is always the source of truth.**

PATH: `/api/v1/stores/aggregate/search`  
METHOD: **POST**  
AUTH: `X-API-Token` header

## Purpose of Endpoint

Retrieve high-level statistics for stores that match the supplied filters. Instead of returning the full list of store objects, this endpoint returns counts (totals, online only, in-store only, etc.) that are useful for dashboards and quick analytics.

Typical use-cases include:

• Displaying store totals for each type on an admin dashboard.  
• Generating reports over a subset of stores (e.g. *my* stores created this month).

## Schemas

### Input

All fields are **optional**.

```json
{
  "name": "string",
  "own": true,
  "ids": [0],
  "store_types": [0],
  "created_on": "2025-06-24",
  "created_before": "2025-06-24",
  "created_after": "2025-06-24",
  "updated_on": "2025-06-24",
  "updated_before": "2025-06-24",
  "updated_after": "2025-06-24"
}
```

#### Field reference

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Case-insensitive substring that must appear in the store name. |
| `own` | boolean | When `true`, only stores created by the calling user are considered. |
| `ids` | int[] | Aggregate only the stores whose IDs are in this list. |
| `store_types` | int[] | Filter by one or more store types. Use [`/api/v1/stores/types/mapping`](../types/mapping.md) to get the numeric mapping.<br/>`1` = Online, `2` = In-Store, `3` = Both. |
| `created_on` | date | Stores created **exactly** on this date (`YYYY-MM-DD`). |
| `created_before` | date | Stores created **on or before** this date. |
| `created_after` | date | Stores created **on or after** this date. |
| `updated_on` | date | Stores updated **exactly** on this date. |
| `updated_before` | date | Stores updated **on or before** this date. |
| `updated_after` | date | Stores updated **on or after** this date. |

### Output

200 OK

```json
{
  "total_stores": 0,
  "online_stores": 0,
  "in_store_stores": 0,
  "combined_stores": 0,
  "combined_online_stores": 0,
  "combined_in_store_stores": 0
}
```

#### Field reference

| Field | Description |
|-------|-------------|
| `total_stores` | Total number of stores that matched the supplied filters. |
| `online_stores` | Number of stores whose `store_type` is **Online** (`1`). |
| `in_store_stores` | Number of stores whose `store_type` is **In-Store** (`2`). |
| `combined_stores` | Number of stores whose `store_type` is **Both** (`3`). |
| `combined_online_stores` | `online_stores + combined_stores`. Useful when you want to treat "Both" as online-capable. |
| `combined_in_store_stores` | `in_store_stores + combined_stores`. Useful when you want to treat "Both" as in-store-capable. |

## Examples

### Request

```bash
curl -X POST https://localhost:8001/api/v1/stores/aggregate/search -H "X-API-Token: abcdefgh" -H "Content-Type: application/json" -d '{"own": true, "store_types": [1, 3], "created_after": "2025-01-01"}'
```

### Successful response

```json
{
  "total_stores": 42,
  "online_stores": 10,
  "in_store_stores": 12,
  "combined_stores": 20,
  "combined_online_stores": 30,
  "combined_in_store_stores": 32
}
```

### Possible Errors

| Status | Meaning | Description |
|--------|---------|-------------|
| 400 | Bad Request | One or more input fields failed validation. |
| 401 | Unauthorized | Missing or invalid `X-API-Token` header. |
| 500 | Internal Server Error | An unexpected error occurred on the server. |

For detailed request/response models and interactive testing, refer to the OpenAPI explorer at `/api/v1/docs`.
