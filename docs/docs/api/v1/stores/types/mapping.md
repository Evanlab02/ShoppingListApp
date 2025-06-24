# Store Types Mapping

**NOTE: The OpenAPI reference at `/api/v1/docs` is always the source of truth.**

PATH: `/api/v1/stores/types/mapping`  
METHOD: **GET**  
AUTH: `X-API-Token` header

## Purpose of Endpoint

Return the canonical mapping between the integer codes used throughout the API and their human-readable store type labels.  This is useful if your application needs to convert between the numeric `store_type` values returned by the API and friendly strings for display or filtering.

## Output

200 OK

```json
{
  "1": "Online",
  "2": "In-Store",
  "3": "Both"
}
```

### Mapping table

| Code | Label     | Description                       |
|------|-----------|-----------------------------------|
| `1`  | Online    | Store that operates exclusively online. |
| `2`  | In-Store  | Brick-and-mortar (physical) store.     |
| `3`  | Both      | Store that supports both online and physical shopping. |

## Examples

### Request

```bash
curl -X GET https://localhost:8001/api/v1/stores/types/mapping -H "X-API-Token: abcdefgh"
```

### Successful response

```json
{
  "1": "Online",
  "2": "In-Store",
  "3": "Both"
}
```

## Possible Errors

| Status | Meaning | Description |
|--------|---------|-------------|
| 401 | Unauthorized | Missing or invalid `X-API-Token` header. |
| 500 | Internal Server Error | An unexpected error occurred on the server. |

For interactive exploration of this endpoint, refer to `/api/v1/docs`.
