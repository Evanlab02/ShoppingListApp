# Consuming the API

You can access the OpenAPI documentation at the following url: <host>/api/v1/docs

**NOTE: The dashboard endpoints are secured using session/cookie auth and do not require an API token.**

## Accessing endpoints that are secured by the token

There is combination of session and token auth used here to secure the endpoints. This means you will need to login using the /api/v1/auth/login endpoint before using other endpoints with your token.

**Currently this will be using your account username and password, in future we will allow you to create an alternative username and password for these endpoints that still link to your account for extra security.**

This means you will also have to have some sort of session in your implementation when querying these endpoints to keep the cookie saved between API calls. You could login everytime you make an API call but this is expensive on the API and in future this will be prevented using rate-limiting.

**In future, I would also like to create a package that you can consume to access this API but that is not in the works right now.**

## Examples

### Python - Using requests

```python
from requests import Session

session = Session()

result = session.post(
    "http://localhost:80/api/v1/auth/login",
    json={"username": "", "password": ""},
)

result = session.get(
    "http://localhost:80/api/v1/stores", headers={"X-API-Key": ""}
)
```