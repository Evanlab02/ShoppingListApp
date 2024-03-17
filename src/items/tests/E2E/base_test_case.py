"""Contains the base test case for the items app e2e tests."""

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from authentication.tests.helpers import create_test_user
from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store

USERNAME_INPUT = "username"
PASSWORD_INPUT = "password"


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

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the test driver."""
        cls.driver.close()
        super().tearDownClass()

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = create_test_user()
        self.store = Store.objects.create(
            name="Base Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        self.store.save()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        Item.objects.all().delete()
        return super().tearDown()

    def _login_self(self) -> None:
        """Login your own user."""
        url = self.live_server_url
        self.driver.get(url)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("test")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value="submit").click()

    def _create_test_store(self) -> Store:
        """Create test store."""
        store = Store.objects.create(
            name="Test Store", description="", store_type=1, user=self.user
        )
        store.save()
        return store
