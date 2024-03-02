"""Contains the base test case for the auth app e2e tests."""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class BaseEndToEndTestCase(StaticLiveServerTestCase):
    """Contains the BaseTestCase class for end-to-end tests."""

    driver: webdriver.Chrome
    delay: int
    mock_username: str
    mock_password: str

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
        cls.driver.implicitly_wait(10)
        cls.delay = 3

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the test driver."""
        cls.driver.close()
        super().tearDownClass()
