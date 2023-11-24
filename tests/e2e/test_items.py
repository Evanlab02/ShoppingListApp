"""Contains end-to-end tests for the items views."""

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

REGISTER_URL = "http://localhost:7001/register"

USERNAME_INPUT = "username-input"
PASSWORD_INPUT = "password-input"
CONFIRM_PASSWORD_INPUT = "confirm-password-input"
EMAIL_INPUT = "email-input"
FIRST_NAME_INPUT = "first-name-input"
LAST_NAME_INPUT = "last-name-input"
SUBMIT_REGISTRATION = "submit-registration"

MOCK_USERNAME = "Item Test User"
MOCK_PASSWORD = "TestItem"
MOCK_FIRST_NAME = "Selenium"
MOCK_LAST_NAME = "Item"
MOCK_EMAIL = "selenium@item.com"


class ItemViewTests(TestCase):
    """Contains end-to-end tests for the item views."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test driver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        cls.delay = 3

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the test driver."""
        cls.driver.close()

    def test_01_register(self) -> None:
        """Test that a user can register."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys(MOCK_EMAIL)
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

    def test_02_login(self) -> None:
        """Test that a user can login."""
        self.driver.get("http://localhost:7001/")
        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value="submit-login").click()

    def test_03_store_page_is_empty(self) -> None:
        """Test that the store page is empty."""
        self.driver.get("http://localhost:7001/items/stores")
        self.driver.find_element(value="total-items-sub-value").text == "0"
        self.driver.find_element(value="total-in-stores-sub-value").text == "0"
        self.driver.find_element(value="total-online-stores-sub-value").text == "0"
        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="store-table-row"
        )
        self.assertEqual(len(row_elements), 0)

    def test_04_create_store(self) -> None:
        """Test that a store can be added."""
        self.driver.get("http://localhost:7001/items/stores/create")
        self.driver.find_element(value="store-input").send_keys("Test Item Store")
        select = Select(self.driver.find_element(value="store-type-input"))
        select.select_by_index(2)
        self.driver.find_element(value="submit-create-store").click()

    def test_05_detail_view(self) -> None:
        """Test that a store detail view can be accessed."""
        self.driver.find_element(value="store-name-sub-value").text == "Test Item Store"
        self.driver.find_element(
            value="store-type-sub-value"
        ).text == "Online & In-Store"
        self.driver.find_element(value="number-of-items-sub-value").text == "0"
        self.driver.find_element(value="user-sub-value").text == MOCK_USERNAME
        self.driver.find_element(value="created-on-sub-value")
        self.driver.find_element(value="last-updated-sub-value")

        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="store-item-row"
        )
        self.assertEqual(len(row_elements), 0)

    def test_06_store_page_has_1_row(self) -> None:
        """Test that the store page has 1 row."""
        self.driver.get("http://localhost:7001/items/stores/me")
        self.driver.find_element(value="total-items-sub-value").text == "1"
        self.driver.find_element(value="total-in-stores-sub-value").text == "1"
        self.driver.find_element(value="total-online-stores-sub-value").text == "1"
        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="store-table-row"
        )
        self.assertEqual(len(row_elements), 1)

    def test_07_item_list_view_has_0_rows(self) -> None:
        """Test that the item list view has 0 rows."""
        self.driver.get("http://localhost:7001/items/me")
        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="item-table-row"
        )
        self.assertEqual(len(row_elements), 0)

    def test_08_create_item(self) -> None:
        """Test that an item can be added."""
        self.driver.get("http://localhost:7001/items/create")
        self.driver.find_element(value="item-input").send_keys("Test Item")
        select = Select(self.driver.find_element(value="store-input"))
        select.select_by_value("Test Item Store")
        self.driver.find_element(value="price-input").send_keys("100")
        self.driver.find_element(value="submit-create-item").click()

    def test_09_item_detail_view(self) -> None:
        """Test that an item detail view can be accessed."""
        self.driver.find_element(value="item-name-sub-value").text == "Test Item"
        self.driver.find_element(value="item-store-sub-value").text == "Takealot"
        self.driver.find_element(value="item-price-sub-value").text == "100.00"
        self.driver.find_element(value="user-sub-value").text == MOCK_USERNAME
        self.driver.find_element(value="last-updated-sub-value")
        self.driver.find_element(
            value="item-related-lists"
        ).text == "On 0 shopping lists"

    def test_10_item_list_view_has_1_row(self) -> None:
        """Test that the item list view has 1 row."""
        self.driver.get("http://localhost:7001/items/me")
        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="item-table-row"
        )
        self.assertEqual(len(row_elements), 1)
