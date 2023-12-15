"""Contains integration tests for the create store endpoint."""

from unittest import TestCase

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from authentication.constants import INPUT_MAPPING

CREATE_URL = "http://localhost:7001/api/v1/stores/create"
LOGIN_URL = "http://localhost:7001/"
TOKEN_URL = "http://localhost:7001/token/register"
DASHBOARD_URL = "http://localhost:7001/shopping/dashboard/"
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")
TOKEN_ID = "api-token"


class TestAuthEndpoints(TestCase):
    """Contains tests for the create store endpoint."""

    driver: webdriver.Chrome
    delay: int
    session: requests.Session

    @classmethod
    def setUpClass(cls) -> None:
        """Create a requests session."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # type: ignore
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        cls.delay = 3
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the requests session."""
        cls.session.close()
        cls.driver.close()

    def test_1_register(self) -> None:
        """Test that a user can register."""
        url = "http://localhost:7001/api/v1/auth/register"
        data = {
            "username": "CreateStoreTester1",
            "password": "CreateStoreTester1",
            "password_confirmation": "CreateStoreTester1",
            "email": "CreateStoreTester1@gmail.com",
            "first_name": "Create",
            "last_name": "Tester",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User successfully registered.")
        self.assertEqual(response.json()["detail"], "")

    def test_2_login(self) -> None:
        """Test that a user can login."""
        url = "http://localhost:7001/api/v1/auth/login"
        data = {
            "username": "CreateStoreTester1",
            "password": "CreateStoreTester1",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged in.")
        self.assertEqual(response.json()["detail"], "")

    def test_3_login_with_browser(self) -> None:
        self.driver.get(LOGIN_URL)

        self.driver.find_element(value=USERNAME_INPUT).send_keys("CreateStoreTester1")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("CreateStoreTester1")
        self.driver.find_element(value=SUBMIT_LOGIN).click()

        self.assertEqual(self.driver.current_url, DASHBOARD_URL)

    def test_4_create_store(self) -> None:
        """Test that a user can create a store."""
        self.driver.get(TOKEN_URL)
        api_token = self.driver.find_element(value=TOKEN_ID).text
        self.assertIsInstance(api_token, str)
        self.assertNotEqual(api_token, "")

        payload = {
            "name": "CreateStoreTester1",
            "description": "CreateStoreTester1",
            "store_type": 3,
        }
        headers = {"X-API-Key": api_token}
        response = self.session.post(CREATE_URL, json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "CreateStoreTester1")
        self.assertEqual(response.json()["description"], "CreateStoreTester1")
        self.assertEqual(response.json()["store_type"], "Both")
