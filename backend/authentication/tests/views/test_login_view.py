"""Contains tests for the login view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestLoginView(TestCase):
    """
    Test the login view.

    Tests: authentication.views.login_view
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        1. Setup the test client.
        2. Create a test user.
        3. Call the super setup method.
        """
        self.client = Client()
        self.user = UserFactory.create()
        super().setUp()

    def tearDown(self) -> None:
        """
        Tear down the test environment.

        1. Logout the test user.
        2. Call the super teardown method.
        """
        self.client.logout()
        return super().tearDown()

    def test_get_login_page(self) -> None:
        """
        Test the login page returns 200 and uses the correct template.

        Given: The user is not logged in.
        When: The user visits the login page.
        Then: The user receives a 200 status code and is shown the login page.
        """
        response = self.client.get(reverse("login_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/index.html")

    def test_post_login_page_405(self) -> None:
        """
        Test the login page returns 405 if post request is made.

        Given: The user is not logged in.
        When: The user visits the login page using a post request.
        Then: The user receives a 405 status code as this method is not allowed.
        """
        response = self.client.post(reverse("login_page"))
        self.assertEqual(response.status_code, 405)

    def test_get_login_page_when_already_logged_in(self) -> None:
        """
        Test the login page returns 302 and redirects to the dashboard if already logged in.

        Given: The user is logged in.
        When: The user visits the login page.
        Then: The user receives a 302 status code and is redirected to the dashboard.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("login_page"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"), 302, 200)

    def test_error_params_get_attached_to_context(self) -> None:
        """
        Test the error params get attached to the context.

        Given: The user is not logged in.
        When: The user visits the login page with an error param.
        Then: The error param is attached to the context.
        """
        response = self.client.get(reverse("login_page") + "?error=test")
        context = response.context
        self.assertEqual(context["error"], "test")
