"""Contains the base test case for the auth app e2e tests."""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from authentication.constants import INPUT_MAPPING


USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")

class BaseEndToEndTestCase(StaticLiveServerTestCase):
    """Contains the BaseTestCase class for end-to-end tests."""

    driver: webdriver.Chrome
    delay: int

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test driver."""
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        cls.driver.set_window_size(1920, 1080, cls.driver.window_handles[0])
        cls.delay = 3

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the test driver."""
        cls.driver.close()
        super().tearDownClass()


    def login(self, username: str, password: str) -> None:
        """Login to the application."""
        self.driver.get(self.live_server_url)
        self.driver.find_element(value=USERNAME_INPUT).send_keys(username)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(value=SUBMIT_LOGIN).click()
