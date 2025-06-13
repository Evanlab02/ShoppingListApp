"""Contains tests for the logout view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestLogoutView(TestCase):
    """
    Test the logout view.

    Tests: authentication.views.logout_view
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        1. Setup the test client.
        2. Create a test user.
        3. Force login the test user.
        4. Call the super setup method.
        """
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        super().setUp()

    def tearDown(self) -> None:
        """
        Tear down the test environment.

        1. Logout the test user.
        2. Call the super teardown method.
        """
        self.client.logout()
        return super().tearDown()

    def test_logout_page(self) -> None:
        """
        Test the logout page.

        Given: The user is logged in.
        When: The user visits the logout page.
        Then: The user receives a 200 status code and is shown the logout page.
        """
        response = self.client.get(reverse("logout_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/logout.html")

    def test_post_logout_page_405(self) -> None:
        """
        Test the logout page returns 405 if a post request is made.

        Given: The user is logged in.
        When: The user visits the logout page using a post request.
        Then: The user receives a 405 status code as this method is not allowed.
        """
        response = self.client.post(reverse("logout_page"))
        self.assertEqual(response.status_code, 405)

    def test_logout_page_when_not_logged_in(self) -> None:
        """
        Test the logout page redirects to login page if the user is not logged in.

        Given: The user is not logged in.
        When: The user visits the logout page.
        Then: The user receives a 302 status code and is redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(reverse("logout_page"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login_page')}?error=You must be logged in to access that page.",
            302,
            200,
        )

    def test_logout_page_with_error_param(self) -> None:
        """
        Test the logout page with an error param.

        Given: The user is logged in.
        When: The user visits the logout page with an error param.
        Then: The error param is attached to the context.
        """
        response = self.client.get(reverse("logout_page") + "?error=test")
        context = response.context
        self.assertEqual(context["error"], "test")
