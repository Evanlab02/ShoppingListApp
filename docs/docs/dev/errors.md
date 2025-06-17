# Error Handling Guidelines for Developers

This document provides comprehensive guidelines for implementing consistent error handling across the Shopping List App. Following these patterns ensures a unified user experience and maintainable codebase.

## Overview

The Shopping List App implements a standardized error handling approach across:

- **API Endpoints**: Using `ErrorSchema` for consistent JSON responses
- **Web Views**: Custom error pages with proper HTTP status codes
- **Forms**: Field-level and form-level validation with user-friendly messages
- **Templates**: Consistent error display patterns using DaisyUI components

## API Error Handling

### Django Ninja Built-in Error Handling

Django Ninja provides comprehensive error handling through its built-in exception system. The framework automatically handles various error types and provides mechanisms for custom error handling as documented in the [Django Ninja error handling guide](https://django-ninja.dev/guides/errors/).

#### Default Exception Handlers

Django Ninja registers default exception handlers for these types:

| Exception Type | Status Code | Description |
|----------------|-------------|-------------|
| `ninja.errors.AuthenticationError` | 401 | Authentication data is not valid |
| `ninja.errors.AuthorizationError` | 403 | Valid authentication but insufficient permissions |
| `ninja.errors.ValidationError` | 422 | Request data validation failures |
| `ninja.errors.HttpError` | Variable | HTTP error with custom status code |
| `django.http.Http404` | 404 | Django's default 404 exception |
| `Exception` | 500 | Any other unhandled exception |

#### Validation Error Handling

Request validation failures raise `ninja.errors.ValidationError` (not `pydantic.ValidationError`) and return **422 Unprocessable Content** responses with this format:

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

### Standard Error Response Schema

For business logic errors and custom exceptions, include `ErrorSchema` in your response definitions:

```python
from shoppingapp.schemas.shared import ErrorSchema

@item_router.post(
    "",
    response={201: ItemSchema, 400: ErrorSchema, 401: ErrorSchema, 404: ErrorSchema, 500: ErrorSchema},
    url_name="item_create",
)
async def create_item(request: HttpRequest, new_item: NewItem) -> ItemSchema:
    # Implementation
```

#### Recommended Error Response Status Codes

Include these status codes in your API endpoint response definitions where applicable:

| Status Code | Schema | Usage |
|-------------|--------|-------|
| `400` | `ErrorSchema` | Bad request, business rule violations |
| `401` | `ErrorSchema` | Authentication required or invalid credentials |
| `403` | `ErrorSchema` | Access denied, insufficient permissions |
| `404` | `ErrorSchema` | Requested resource does not exist |
| `422` | Built-in | Request validation errors (handled automatically) |
| `500` | `ErrorSchema` | Internal server errors |

### ErrorSchema Definition

The `ErrorSchema` provides a consistent error response format for custom errors:

```python
class ErrorSchema(Schema):
    """Error schema for custom application errors."""
    detail: str
```

### Custom Exception Handlers

You can create custom exception handlers using the `@api.exception_handler` decorator:

```python
from ninja.errors import HttpError

class ServiceUnavailableError(Exception):
    pass

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"detail": "Service temporarily unavailable. Please retry later."},
        status=503,
    )
```

### Throwing HTTP Errors

Use `ninja.errors.HttpError` to throw HTTP responses with specific status codes:

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if not resource_available:
        raise HttpError(503, "Service Unavailable. Please retry later.")
    return {"data": "success"}
```

### Handling Custom Application Exceptions

For application-specific exceptions, create custom exception handlers:

```python
from authentication.errors.exceptions import InvalidCredentials
from shoppingapp.schemas.shared import ErrorSchema

@api.exception_handler(InvalidCredentials)
def handle_invalid_credentials(request, exc):
    return api.create_response(
        request,
        {"detail": "Invalid username or password."},
        status=401,
    )
```

### Complete API Error Implementation Example

```python
from authentication.auth import TOKEN_AUTH
from ninja.errors import HttpError
from shoppingapp.schemas.shared import ErrorSchema
from stores.errors.exceptions import StoreDoesNotExist

@store_router.get(
    "/{store_id}",
    response={
        200: StoreSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        404: ErrorSchema,
        500: ErrorSchema,
    },
    url_name="store_detail",
)
async def get_store_detail(request: HttpRequest, store_id: int) -> Store:
    """
    Get store detail with proper error handling.
    
    - 200: Successfully returns store data
    - 400: Bad request (invalid store_id format)
    - 401: Authentication required  
    - 404: Store not found
    - 422: Validation errors (handled automatically by Django Ninja)
    - 500: Internal server error
    """
    try:
        return await store_service.get_store_detail(store_id=store_id) # Could raise `StoreDoesNotExist` which will be handled by a exception handler.
    except ValueError:
        # Use HttpError for immediate HTTP responses
        raise HttpError(400, "Invalid store ID format")
```

### Configuring Exception Handlers in urls.py

Configure your API's exception handlers in your main API configuration:

```python
from ninja import NinjaAPI
from stores.errors.exceptions import StoreDoesNotExist
from items.errors.exceptions import ItemDoesNotExist

api = NinjaAPI()

@api.exception_handler(StoreDoesNotExist)
def handle_store_not_found(request, exc):
    return api.create_response(
        request,
        {"detail": "Store not found."},
        status=404,
    )

@api.exception_handler(ItemDoesNotExist)  
def handle_item_not_found(request, exc):
    return api.create_response(
        request,
        {"detail": "Item not found."},
        status=404,
    )
```

---

## Web View Error Handling

### Centralized Error Handlers

The application uses centralized error handlers defined in `backend/shoppingapp/core/urls.py`:

```python
handler400 = "dashboard.views.bad_request_view"
handler403 = "dashboard.views.permission_denied_view"
handler404 = "dashboard.views.not_found_view"
handler500 = "dashboard.views.server_error_view"
```

### Error View Implementation Pattern

Follow this pattern when implementing error views:

```python
def bad_request_view(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """
    Handle 400 Bad Request errors.

    Args:
        request (HttpRequest): The request object.
        exception (Exception | None): The exception object.

    Returns:
        HttpResponse: The response object.
    """
    LOG.error(f"400 Bad Request: {exception}")
    context = {"exception": GENERIC_ERROR_MESSAGE}
    return render(request, "dashboard/err/400.html", context, status=400)
```

### Raising HTTP Exceptions in Views

Use Django's built-in exceptions to trigger error handlers:

```python
from django.http import Http404
from django.core.exceptions import PermissionDenied, BadRequest

# For 404 errors
try:
    item = Item.objects.get(id=item_id, user=user)
except Item.DoesNotExist:
    raise Http404("Item does not exist.")

# For 403 errors
if not user.has_permission():
    raise PermissionDenied("Access denied.")

# For 400 errors
if not valid_input:
    raise BadRequest("Invalid request data.")
```

---

## Form Error Handling

### Django Forms Integration

Use Django's built-in form validation and error handling:

```python
class ItemForm(ModelForm):
    """Form for creating and updating items."""

    class Meta:
        model = Item
        fields = ["name", "store", "price", "description"]

    def clean(self) -> dict[str, Any] | None:
        """Custom validation logic."""
        cleaned_data = super().clean()
        name: str = cleaned_data.get("name")
        store: Store | None = cleaned_data.get("store")

        if not store:
            self.add_error("store", "Store does not exist.")
        elif self.does_item_exist(name=name, store_id=store.id):
            self.add_error("name", "Item with this name already exists in this store.")

        return cleaned_data
```

### View Form Error Handling Pattern

Handle form errors consistently in views:

```python
@require_http_methods(["GET", "POST"])
@login_required
def create_page(request: HttpRequest) -> HttpResponse:
    """Create page with proper form error handling."""
    if request.method == "POST":
        form = ItemForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save()
            url = reverse("item_detail_page", kwargs={"item_id": item.id})
            return HttpResponseRedirect(url)
    else:
        form = ItemForm(user=request.user)

    context = BaseContext(page_title="Create Item")
    return render(request, "items/create.html", context.attach_form(form))
```

### BaseContext Form Integration

Use the `BaseContext.attach_form()` method for consistent form handling:

```python
from shoppingapp.schemas import BaseContext

context = BaseContext(page_title="Create Item")
return render(request, "items/create.html", context.attach_form(form))
```

---

## Template Error Display Patterns

### Form Error Display

Display form errors consistently using DaisyUI components:

```html
<!-- General form errors -->
{% if form.errors %}
<div class="alert alert-error mb-4">
    <i class="fas fa-exclamation-circle"></i>
    <span>{{ form.errors.as_text }}</span>
</div>
{% endif %}

<!-- Field-specific errors -->
{% for field in form %}
<div class="form-control w-full">
    <label for="{{ field.id_for_label }}" class="label">
        <span class="label-text">{{ field.label }}</span>
    </label>
    {{ field }}
    {% if field.errors %}
    <div class="text-red-500 text-sm flex flex-row items-center gap-2">
        <i class="fas fa-exclamation-circle"></i>
        <span>{{ field.errors }}</span>
    </div>
    {% endif %}
</div>
{% endfor %}
```

### Error Query Parameter Handling

Handle error messages passed via query parameters:

```html
{% if error %}
<div class="alert alert-error mb-4">
    <i class="fas fa-exclamation-circle"></i>
    <span>{{ error }}</span>
</div>
{% endif %}
```

### Error Page Template Structure

Error pages follow this structure:

```html
{% extends "dashboard/err/base.html" %}

{% block error_content %}
<div class="mb-6">
    <i class="fas fa-exclamation-triangle text-6xl text-warning mb-4"></i>
    <h1 class="text-3xl font-bold text-error mb-2">400</h1>
    <h2 class="text-xl font-semibold mb-4">Bad Request</h2>
    <div class="alert alert-warning">
        <i class="fas fa-info-circle"></i>
        <span>User-friendly error message explaining what went wrong.</span>
    </div>
    {% if exception %}
    <div class="alert alert-error mt-4">
        <i class="fas fa-bug"></i>
        <div>
            <div class="font-semibold">Exception Details:</div>
            <div class="text-sm mt-1 font-mono">{{ exception }}</div>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}
```

---

## Error Handling Best Practices

### 1. Consistent Error Messages

Use descriptive, user-friendly error messages:

```python
# Good
raise Http404("Item does not exist.")

# Bad
raise Http404("Not found.")
```

### 2. Proper Logging

Log errors at appropriate levels:

```python
import logging

LOG = logging.getLogger(__name__)

def error_handler(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    LOG.error(f"Error occurred: {exception}")
    # Handle error response
```

### 3. Exception Context

Provide context in error handlers without exposing sensitive information:

```python
def bad_request_view(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    # Log detailed error for developers
    LOG.error(f"400 Bad Request: {exception}")
    
    # Provide generic message to users
    context = {"exception": GENERIC_ERROR_MESSAGE}
    return render(request, "dashboard/err/400.html", context, status=400)
```

### 4. Input Validation

Validate input at multiple levels:

```python
class ItemForm(ModelForm):
    def clean_price(self):
        """Validate price field."""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError("Price cannot be negative.")
        return price
```

### 5. Graceful Degradation

Handle errors gracefully without breaking the application:

```python
try:
    # Risky operation
    result = complex_operation()
except SpecificException as e:
    LOG.warning(f"Operation failed: {e}")
    # Provide fallback behavior
    result = default_value
```

---

## Testing Error Handling

### Test Error Scenarios

Write tests for error conditions:

```python
def test_item_create_view_missing_fields(self) -> None:
    """Test form validation with missing fields."""
    data = {
        "name": "Test Item",
        "store": f"{self.stores[0].id}",
        "price": "",  # Missing required field
        "description": "",
    }
    response = self.client.post(self.url, data)
    
    self.assertEqual(response.status_code, 200)
    form = response.context["form"]
    self.assertEqual(form.errors["price"], ["This field is required."])
```

### Test Error Views

Test custom error handlers:

```python
def test_not_found_view(self) -> None:
    """Test 404 error page rendering."""
    response = self.client.get(self.get_url(404))
    self.assertEqual(response.status_code, 404)
    self.assertTemplateUsed(response, "dashboard/err/404.html")
```

---

## Common Patterns

### View Error Handling Pattern

```python
@require_http_methods(["GET"])
@login_required
def detail_view(request: HttpRequest, item_id: int) -> HttpResponse:
    """Standard detail view with error handling."""
    try:
        item = Item.objects.get(id=item_id, user=request.user)
        context = BaseContext(page_title=f"Item: {item.name}")
        return render(request, "items/detail.html", context.model_dump())
    except Item.DoesNotExist:
        raise Http404("Item does not exist.")
```

### Redirect with Error Pattern

```python
try:
    # Operation that might fail
    await service.update_item(item_id, data)
    return HttpResponseRedirect(reverse('success_page'))
except ValidationException as error:
    return HttpResponseRedirect(
        f"{reverse('error_page')}?error={error}"
    )
```

This comprehensive error handling approach ensures consistent user experience and maintainable code across the Shopping List App.
