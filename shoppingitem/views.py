"""Contains the shoppingitem app views."""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .services import ItemViewService, StoreViewService

ITEM_SERVICE = ItemViewService()
STORE_SERVICE = StoreViewService()


@login_required(login_url="/")
@require_http_methods(["GET"])
def item_user_overview_page(request: HttpRequest) -> HttpResponse:
    """
    Render the item user overview page.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered item user overview page.
    """
    context = ITEM_SERVICE.user_overview_page(request)
    rendered_page = render(request, "items/items_list_view.html", context=context)
    return rendered_page


@login_required(login_url="/")
@require_http_methods(["GET"])
def item_overview_page(request: HttpRequest) -> HttpResponse:
    """
    Render the item overview page.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered item overview page.
    """
    context = ITEM_SERVICE.overall_overview_page(request)
    rendered_page = render(request, "items/items_list_view.html", context=context)
    return rendered_page


@login_required(login_url="/")
@require_http_methods(["GET"])
def get_item_detail_view(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Render the item detail view.

    Args:
        request(HttpRequest): The request object.
        item_id(int): The id of the item to render.

    Returns:
        HttpResponse: The rendered item detail view.
    """
    context = ITEM_SERVICE.detail_page(item_id)
    rendered_page = render(request, "items/item_detail.html", context=context)
    return rendered_page


@login_required(login_url="/")
@require_http_methods(["GET"])
def get_item_create_page(request: HttpRequest) -> HttpResponse:
    """
    Render the item create page.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered item create page.
    """
    context = ITEM_SERVICE.create_page(request)
    rendered_page = render(request, "items/item_create.html", context=context)
    return rendered_page


@login_required(login_url="/")
@require_http_methods(["POST"])
def create_item(request: HttpRequest) -> HttpResponse:
    """
    Create an item.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: Redirect to the item detail page or the item create page with an error.
    """
    redirect_url = ITEM_SERVICE.create_item(request)
    return HttpResponseRedirect(redirect_url)


@login_required(login_url="/")
@require_http_methods(["GET"])
def get_user_store_view(request: HttpRequest) -> HttpRequest:
    """
    Render the user store view.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered user store view.
    """
    context = STORE_SERVICE.user_overview_page(request)
    rendered_page = render(request, "items/store_list_view.html", context=context)
    return rendered_page


@login_required(login_url="/")
@require_http_methods(["GET"])
def get_store_view(request: HttpRequest) -> HttpRequest:
    """
    Render the store view.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered store view.
    """
    context = STORE_SERVICE.overall_overview_page(request)
    rendered_page = render(request, "items/store_list_view.html", context=context)
    return rendered_page


@login_required(login_url="/")
@require_http_methods(["GET"])
def get_store_detail_view(request: HttpRequest, store_id: int) -> HttpResponse:
    """
    Render the store detail view.

    Args:
        request(HttpRequest): The request object.
        store_id(int): The id of the store to render.

    Returns:
        HttpResponse: The rendered store detail view.
    """
    context = STORE_SERVICE.detail_view(request, store_id)
    rendered_page = render(request, "items/store_detail.html", context=context)
    return rendered_page


@login_required(login_url="/")
@require_http_methods(["GET"])
def get_store_create_page(request: HttpRequest) -> HttpResponse:
    """
    Render the store create page.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered store create page.
    """
    context = STORE_SERVICE.create_page(request)
    rendered_page = render(request, "items/store_create.html", context=context)
    return rendered_page


@login_required(login_url="/")
@require_http_methods(["POST"])
def create_store(request: HttpRequest) -> HttpResponse:
    """
    Create a store.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: Redirect to the store detail page or the store create page with an error.
    """
    redirect_url = STORE_SERVICE.create_store(request)
    return HttpResponseRedirect(redirect_url)
