"""Utility functions for the shoppingapp application."""

import logging

from django.http import HttpRequest

log = logging.getLogger(__name__)
log.info("Loading utils...")


async def get_overview_params(request: HttpRequest) -> dict[str, int]:
    """
    Get overview page params from request object.

    The overview page params includes the following values:
    - Page: The page number for pagination.
    - Limit: The number of table rows to show per page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict[str, int]: Dictionary containing the page and limit values grabbed from the
        request object.
    """
    log.info("Loading overview params...")
    page = request.GET.get("page", 1)
    limit = request.GET.get("limit", 10)

    try:
        if isinstance(page, str):
            page = int(page)
    except ValueError:
        log.warning("Failed to load page param, defaulting to 1")
        page = 1

    try:
        if isinstance(limit, str):
            limit = int(limit)
    except ValueError:
        log.warning("Failed to load limit param, defaulting to 10")
        limit = 10

    log.info("Loaded overview params.")
    return {"page": page, "limit": limit}


log.info("Loaded utils.")
