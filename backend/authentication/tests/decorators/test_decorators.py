"""Contains the tests for the decorators."""

import asyncio
from unittest import TestCase

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import AsyncRequestFactory, RequestFactory, TestCase
from django.urls import reverse

from authentication.decorators.login import (
    async_login_required,
    async_redirect_if_logged_in,
    login_required,
    redirect_if_logged_in,
)
from authentication.tests.factory import UserFactory


class TestDecorators(TestCase):
    """Test the decorators."""

    def setUp(self):
        """Set up the test."""
        self.user = UserFactory()
        self.factory = RequestFactory()
        self.async_factory = AsyncRequestFactory()
        self.view = lambda request: HttpResponse("OK")
        self.async_view = lambda request: asyncio.to_thread(lambda: HttpResponse("OK"))

    def test_login_required_is_logged_in(self):
        """Test the login required decorator."""
        request = self.factory.get(reverse("dashboard"))
        request.user = self.user
        response = login_required(self.view)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")

    def test_login_required_is_not_logged_in(self):
        """Test the login required decorator."""
        request = self.factory.get(reverse("dashboard"))
        request.user = AnonymousUser()
        response = login_required(self.view)(request)
        self.assertEqual(response.status_code, 302)

    async def test_async_login_required_is_logged_in(self):
        """Test the login required decorator."""
        request = self.async_factory.get(reverse("dashboard"))
        request.auser = lambda: asyncio.to_thread(lambda: self.user)
        response = await async_login_required(self.async_view)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")

    async def test_async_login_required_is_not_logged_in(self):
        """Test the login required decorator."""
        request = self.async_factory.get(reverse("dashboard"))
        request.auser = lambda: asyncio.to_thread(lambda: AnonymousUser())
        response = await async_login_required(self.async_view)(request)
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_logged_in(self):
        """Test the redirect if logged in decorator."""
        request = self.factory.get(reverse("dashboard"))
        request.user = self.user
        response = redirect_if_logged_in(self.view)(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))

    def test_redirect_if_logged_in_when_not_logged_in(self):
        """Test the redirect if logged in decorator."""
        request = self.factory.get(reverse("dashboard"))
        request.user = AnonymousUser()
        response = redirect_if_logged_in(self.view)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")

    async def test_async_redirect_if_logged_in(self):
        """Test the redirect if logged in decorator."""
        request = self.async_factory.get(reverse("dashboard"))
        request.auser = lambda: asyncio.to_thread(lambda: self.user)
        response = await async_redirect_if_logged_in(self.async_view)(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))

    async def test_async_redirect_if_logged_in_when_not_logged_in(self):
        """Test the redirect if logged in decorator."""
        request = self.async_factory.get(reverse("dashboard"))
        request.auser = lambda: asyncio.to_thread(lambda: AnonymousUser())
        response = await async_redirect_if_logged_in(self.async_view)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")
