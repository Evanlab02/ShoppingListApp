"""Contains end-to-end tests for the stores views."""

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

MOCK_USERNAME = "Store Test User"
MOCK_PASSWORD = "TestStore"
MOCK_FIRST_NAME = "Selenium"
MOCK_LAST_NAME = "Store"
MOCK_EMAIL = "selenium@store.com"


class StoreViewTests(TestCase):
    """Contains end-to-end tests for the store views."""

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
        self.driver.get("http://localhost:7001/items/stores/me")
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
        self.driver.find_element(value="store-input").send_keys("Takealot")
        select = Select(self.driver.find_element(value="store-type-input"))
        select.select_by_index(0)
        self.driver.find_element(value="submit-create-store").click()

    def test_05_detail_view(self) -> None:
        """Test that a store detail view can be accessed."""
        self.driver.find_element(value="store-name-sub-value").text == "Takealot"
        self.driver.find_element(value="store-type-sub-value").text == "Online"
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
        self.driver.find_element(value="total-in-stores-sub-value").text == "0"
        self.driver.find_element(value="total-online-stores-sub-value").text == "1"
        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="store-table-row"
        )
        self.assertEqual(len(row_elements), 1)

    def test_07_create_second_store(self) -> None:
        """Test that a second store can be added."""
        self.driver.get("http://localhost:7001/items/stores/create")
        self.driver.find_element(value="store-input").send_keys("Pick n Pay")
        select = Select(self.driver.find_element(value="store-type-input"))
        select.select_by_index(1)
        self.driver.find_element(value="submit-create-store").click()

    def test_08_second_store_detail_view(self) -> None:
        """Test that a second store detail view can be accessed."""
        self.driver.find_element(value="store-name-sub-value").text == "Pick n Pay"
        self.driver.find_element(value="store-type-sub-value").text == "In-store"
        self.driver.find_element(value="number-of-items-sub-value").text == "0"
        self.driver.find_element(value="user-sub-value").text == MOCK_USERNAME
        self.driver.find_element(value="created-on-sub-value")
        self.driver.find_element(value="last-updated-sub-value")

        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="store-item-row"
        )
        self.assertEqual(len(row_elements), 0)

    def test_09_store_page_has_2_rows(self) -> None:
        """Test that the store page has 2 rows."""
        self.driver.get("http://localhost:7001/items/stores/me")
        self.driver.find_element(value="total-items-sub-value").text == "2"
        self.driver.find_element(value="total-in-stores-sub-value").text == "1"
        self.driver.find_element(value="total-online-stores-sub-value").text == "1"
        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="store-table-row"
        )
        self.assertEqual(len(row_elements), 2)

    def test_10_create_third_store(self) -> None:
        """Test that a third store can be added."""
        self.driver.get("http://localhost:7001/items/stores/create")
        self.driver.find_element(value="store-input").send_keys("Checkers")
        select = Select(self.driver.find_element(value="store-type-input"))
        select.select_by_index(2)
        self.driver.find_element(value="submit-create-store").click()

    def test_11_third_store_detail_view(self) -> None:
        """Test that a third store detail view can be accessed."""
        self.driver.find_element(value="store-name-sub-value").text == "Checkers"
        self.driver.find_element(
            value="store-type-sub-value"
        ).text == "Online & In-store"
        self.driver.find_element(value="number-of-items-sub-value").text == "0"
        self.driver.find_element(value="user-sub-value").text == MOCK_USERNAME
        self.driver.find_element(value="created-on-sub-value")
        self.driver.find_element(value="last-updated-sub-value")

        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="store-item-row"
        )
        self.assertEqual(len(row_elements), 0)

    def test_12_store_page_has_3_rows(self) -> None:
        """Test that the store page has 3 rows."""
        self.driver.get("http://localhost:7001/items/stores/me")
        self.driver.find_element(value="total-items-sub-value").text == "3"
        self.driver.find_element(value="total-in-stores-sub-value").text == "2"
        self.driver.find_element(value="total-online-stores-sub-value").text == "2"
        row_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value="store-table-row"
        )
        self.assertEqual(len(row_elements), 3)
