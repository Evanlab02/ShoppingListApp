"""Load testing for auth endpoints."""

from time import sleep
from uuid import uuid4

from bs4 import BeautifulSoup, NavigableString
from faker import Faker
from locust import FastHttpUser, tag, task

faker = Faker()


class TestCase(FastHttpUser):
    """Test the API."""

    def on_start(self) -> None:
        """On test user start up."""
        self.client.post(
            "/api/v1/auth/login",
            json={"username": "AnimalAlpaca", "password": "devadmin"},
            headers={"Content-Type": "application/json"},
        )

    def on_stop(self) -> None:
        """On user close."""
        self.client.post("/api/v1/auth/logout", headers={"Content-Type": "application/json"})

    @tag("write")
    @tag("store")
    @tag("api")
    @tag("api_store_create")
    @task
    def create_store(self) -> None:
        """Create a store via the API."""
        self.client.post(
            "/api/v1/stores/create",
            json={
                "name": faker.company() + uuid4().hex,
                "store_type": faker.random_element(elements=[1, 2, 3]),
                "description": faker.sentence(),
            },
            headers={"Content-Type": "application/json"},
        )
        sleep(1)

    @tag("read")
    @tag("store")
    @tag("view")
    @tag("view_store_create")
    @task
    def view_store_create(self) -> None:
        """View the store create page."""
        self.client.get("/stores/create")
        sleep(1)

    @tag("write")
    @tag("store")
    @tag("view")
    @tag("view_store_create_action")
    @task
    def view_store_create_action(self) -> None:
        """Post to the the store create action view."""
        # Get CSRF middleware token from form
        response = self.client.get("/stores/create")
        sleep(1)

        if response.status_code != 200 or response.text is None:
            raise Exception(f"Failed to get store create page: {response.status_code}")

        # Parse the HTML and find the CSRF token using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token_element = soup.find("input", {"name": "csrfmiddlewaretoken"})

        if csrf_token_element is None or isinstance(csrf_token_element, NavigableString):
            raise Exception("Failed to find CSRF element in the form")

        csrf_token = csrf_token_element.get("value")

        if csrf_token is None:
            raise Exception("Failed to find CSRF token value in the form")

        if not isinstance(csrf_token, str):
            raise Exception("CSRF token is not a string")

        self.client.post(
            "/stores/create/action",
            data={
                "csrfmiddlewaretoken": csrf_token,
                "store-input": faker.company() + uuid4().hex,
                "store-type-input": faker.random_element(elements=["Both", "Online", "In-Store"]),
                "description-input": faker.sentence(),
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        sleep(1)
