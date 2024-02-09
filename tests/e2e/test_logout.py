"""Contains end-to-end tests for the logout page."""

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from authentication.constants import INPUT_MAPPING

# Urls
REGISTER_URL = "http://localhost:7001/register"
LOGIN_URL = "http://localhost:7001/"
LOGOUT_URL = "http://localhost:7001/logout"
DASHBOARD_URL = "http://localhost:7001/shopping/dashboard/"

# Element IDs
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
CONFIRM_PASSWORD_INPUT = INPUT_MAPPING.get("password-confirm-input", "password-confirm-input")
EMAIL_INPUT = INPUT_MAPPING.get("email-input", "email-input")
FIRST_NAME_INPUT = INPUT_MAPPING.get("first-name-input", "first-name-input")
LAST_NAME_INPUT = INPUT_MAPPING.get("last-name-input", "last-name-input")
SUBMIT_REGISTRATION = INPUT_MAPPING.get("submit-register", "submit-register")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")
SUBMIT_REGISTRATION = INPUT_MAPPING.get("submit-register", "submit-register")
SUBMIT_CANCEL_LOGOUT = INPUT_MAPPING.get("submit-cancel", "submit-cancel")
SUBMIT_LOGOUT = INPUT_MAPPING.get("submit-logout", "submit-logout")
ERROR_TEXT = "error-text"

# Mock data
MOCK_USERNAME = "Logout Test User"
MOCK_PASSWORD = "TestLogout"
MOCK_FIRST_NAME = "Selenium"
MOCK_LAST_NAME = "Logout"
MOCK_EMAIL = "testlogout@selenium.com"


class TestLogoutPage(TestCase):
    """Contains end-to-end tests for the logout page."""

    driver: webdriver.Chrome
    delay: int

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test driver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # type: ignore
        options.add_argument("--start-maximized")  # type: ignore
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        cls.driver.set_window_size(1920, 1080, cls.driver.window_handles[0])

        cls.delay = 3

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the test driver."""
        cls.driver.close()

    def test_1_register(self) -> None:
        """Test that a user can register."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys(MOCK_EMAIL)
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.get_screenshot_as_file("./screenshots/logout/register_pre_submit.png")
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()
        self.driver.get_screenshot_as_file("./screenshots/logout/register_post_submit.png")
        self.assertEqual(self.driver.current_url, LOGIN_URL)

    def test_2_login(self) -> None:
        self.driver.get(LOGIN_URL)

        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.get_screenshot_as_file("./screenshots/logout/login_pre_submit.png")
        self.driver.find_element(value=SUBMIT_LOGIN).click()
        self.driver.get_screenshot_as_file("./screenshots/logout/login_post_submit.png")
        self.assertEqual(self.driver.current_url, DASHBOARD_URL)

    def test_3_logout_cancel(self) -> None:
        self.driver.get(LOGOUT_URL)
        self.driver.get_screenshot_as_file("./screenshots/logout/logout_1.png")
        self.driver.find_element(value=SUBMIT_CANCEL_LOGOUT).click()
        self.driver.get_screenshot_as_file("./screenshots/logout/logout_cancel.png")
        self.assertEqual(self.driver.current_url, DASHBOARD_URL)

    def test_4_logout(self) -> None:
        self.driver.get(LOGOUT_URL)
        self.driver.get_screenshot_as_file("./screenshots/logout/logout_2.png")
        self.driver.find_element(value=SUBMIT_LOGOUT).click()
        self.driver.get_screenshot_as_file("./screenshots/logout/logout_submit.png")
        self.assertEqual(self.driver.current_url, LOGIN_URL)
