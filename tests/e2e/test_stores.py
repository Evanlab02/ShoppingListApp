"""
Contains end-to-end tests for the store pages.
"""

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from authentication.constants import INPUT_MAPPING

# Urls
STORE_CREATE_URL = "http://localhost:7001/stores/create"
LOGIN_URL = "http://localhost:7001/"
REGISTER_URL = "http://localhost:7001/register"
DASHBOARD_URL = "http://localhost:7001/shopping/dashboard/"

# Element IDs
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
CONFIRM_PASSWORD_INPUT = INPUT_MAPPING.get(
    "password-confirm-input", "password-confirm-input"
)
EMAIL_INPUT = INPUT_MAPPING.get("email-input", "email-input")
FIRST_NAME_INPUT = INPUT_MAPPING.get("first-name-input", "first-name-input")
LAST_NAME_INPUT = INPUT_MAPPING.get("last-name-input", "last-name-input")
SUBMIT_REGISTRATION = INPUT_MAPPING.get("submit-register", "submit-register")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")
SUBMIT_REGISTRATION = INPUT_MAPPING.get("submit-register", "submit-register")
ERROR_TEXT = "error-text"

# Mock data
MOCK_USERNAME = "StoreTestUser"
MOCK_PASSWORD = "TestStore"
MOCK_FIRST_NAME = "Selenium"
MOCK_LAST_NAME = "Stores"
MOCK_EMAIL = "teststores@selenium.com"


class TestStorePages(TestCase):
    """Contains end-to-end tests for the store create page."""

    driver: webdriver.Chrome
    delay: int

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test driver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # type: ignore
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        cls.delay = 3

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the test driver."""
        cls.driver.close()

    def test_01_get_create_page_without_being_logged_in(self) -> None:
        """Test that a user cannot access the create store page without being logged in."""
        self.driver.get(STORE_CREATE_URL)
        self.assertEqual(
            self.driver.current_url,
            f"{LOGIN_URL}?error=You%20must%20be%20logged%20in%20to%20access%20that%20page.",
        )

    def test_02_register(self) -> None:
        """Test that a user can register."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys(MOCK_EMAIL)
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.assertEqual(self.driver.current_url, LOGIN_URL)

    def test_03_login(self) -> None:
        self.driver.get(LOGIN_URL)

        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=SUBMIT_LOGIN).click()

        self.assertEqual(self.driver.current_url, DASHBOARD_URL)

    def test_04_get_create_page(self) -> None:
        """Test that a user can access the create store page."""
        self.driver.get(STORE_CREATE_URL)
        self.assertEqual(self.driver.current_url, STORE_CREATE_URL)

        heading = self.driver.find_element(value="form-heading").text
        self.assertEqual(heading, "Create Store")

        tag_name = self.driver.find_element(value="store-input").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="store-type-input").tag_name
        self.assertEqual(tag_name, "select")

        tag_name = self.driver.find_element(value="description-input").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="submit-create-store").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="cancel-create-store").tag_name
        self.assertEqual(tag_name, "input")

    def test_05_get_create_page_with_error(self) -> None:
        """Test that a user can access the create store page with an error."""
        self.driver.get(f"{STORE_CREATE_URL}?error=This+is+an+error")
        self.assertEqual(
            self.driver.current_url, f"{STORE_CREATE_URL}?error=This+is+an+error"
        )

        error_text = self.driver.find_element(value="form-error").text
        self.assertEqual(error_text, "This is an error")

    def test_06_create_store(self) -> None:
        """Test that a user can create a store."""
        self.driver.get(STORE_CREATE_URL)

        self.driver.find_element(value="store-input").send_keys("Test Store")
        self.driver.find_element(value="store-type-input").send_keys("Both")
        self.driver.find_element(value="description-input").send_keys(
            "Test Description"
        )
        self.driver.find_element(value="submit-create-store").click()

        current_url = self.driver.current_url
        self.assertTrue(current_url.startswith("http://localhost:7001/stores/detail/"))
