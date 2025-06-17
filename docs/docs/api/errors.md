# API Error Handling

This document outlines the standardized error handling approach implemented across all API endpoints in the Shopping List App. Consistent error handling ensures a predictable and reliable API experience for all consumers.

## Error Responses 

All API endpoints in the Shopping List App can return errors using a standardized `ErrorSchema` format.

### Standard Error Response Schema

```json
{
  "detail": "string"
}
```

**Fields:**

- `detail` (string, required): A human-readable error message describing what went wrong

#### HTTP Status Codes

The API uses standard HTTP status codes to indicate the type of error:

| Status Code | Description | Usage |
|-------------|-------------|-------|
| `400` | Bad Request | Invalid request data, validation errors, business rule violations |
| `401` | Unauthorized | Authentication required or invalid credentials |
| `403` | Forbidden | Access denied, insufficient permissions |
| `404` | Not Found | Requested resource does not exist |
| `500` | Internal Server Error | Unexpected server errors |

---

### Django Ninja Validation Errors

The Shopping List App uses [Django Ninja](https://django-ninja.dev/guides/errors/) for API development, which includes built-in validation error handling that differs from the standard `ErrorSchema` format.

#### Validation Error Format

When request validation fails, Django Ninja returns a **422 Unprocessable Content** response with this format:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "name"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {"min_length": 1}
    }
  ]
}
```

**Key Differences from ErrorSchema:**

- Status code is `422` instead of `400`
- `detail` is an **array** of error objects, not a simple string
- Each error object contains validation-specific fields (`type`, `loc`, `msg`, `input`, `ctx`)

---

### Handling Non-Standard Error Responses

While most errors should be handled and return the standard error response, sometimes errors slip through the system and end up returning non-standard responses. This will often be HTML or text responses, which are not of value to API consumers and should be treated as complete failures.

### TypeScript Example - Handling All Error Scenarios

Here's how to properly handle both standard and non-standard error responses:

```ts
// Interfaces for error responses
interface ValidationErrorDetail {
  type: string;
  loc: (string | number)[];
  msg: string;
  input?: any;
  ctx?: Record<string, any>;
}

interface ValidationErrorResponse {
  detail: ValidationErrorDetail[];
}

interface ErrorSchema {
  detail: string;
}

// Union type for all possible error responses
type ApiErrorResponse = ErrorSchema | ValidationErrorResponse;

// Type guards
function isValidationError(obj: any): obj is ValidationErrorResponse {
  return obj && 
         typeof obj === 'object' && 
         Array.isArray(obj.detail) && 
         obj.detail.length > 0 &&
         typeof obj.detail[0] === 'object' &&
         'type' in obj.detail[0];
}

function isErrorSchema(obj: any): obj is ErrorSchema {
  return obj && typeof obj === 'object' && typeof obj.detail === 'string';
}

// API Call function with error handling
async function makeApiRequest<T = any>(
  url: string, 
  options: ApiRequestOptions = {}
): Promise<T> {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    let responseData: unknown;
    try {
      responseData = await response.json();
    } catch (parseError) {
      throw new Error(
        `API returned non-JSON response (${response.status}): ${response.statusText}`
      );
    }

    if (!response.ok) {
      if (isValidationError(responseData)) {
        // Django Ninja validation error (422)
        const errorMessages = responseData.detail.map(err => err.msg).join(', ');
        throw new Error(`Validation failed: ${errorMessages}`);
      } else if (isErrorSchema(responseData)) {
        // Standard error response
        throw new Error(responseData.detail);
      } else {
        // Non-standard error response
        throw new Error(
          `API error (${response.status}): Received non-standard error format`
        );
      }
    }

    return responseData as T;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}
```
