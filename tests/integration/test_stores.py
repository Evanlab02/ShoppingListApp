"""Contains integration tests for the stores endpoints."""

import requests

from tests.integration.base_test_case import BaseTestCase

CREATE_URL = "http://localhost:7001/api/v1/stores/create"
MAPPING_URL = "http://localhost:7001/api/v1/stores/types/mapping"


class TestStoreEndpoints(BaseTestCase):
    """Contains tests for the store endpoints."""

    session: requests.Session

    @classmethod
    def setUpClass(cls) -> None:
        """Create a requests session."""
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the requests session."""
        cls.session.close()

    def test_1_create_store(self) -> None:
        """Test that a user can create a store."""
        self._login()
        payload = {
            "name": "StoreTester1",
            "description": "StoreTester1",
            "store_type": 3,
        }
        response = self.session.post(CREATE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "StoreTester1")
        self.assertEqual(response.json()["description"], "StoreTester1")
        self.assertEqual(response.json()["store_type"], 3)
        self.assertIsInstance(response.json()["id"], int)
        self.assertIsInstance(response.json()["created_at"], str)
        self.assertIsInstance(response.json()["updated_at"], str)

    def test_2_get_store_type_mapping(self) -> None:
        """Test that a user can get the store type mapping."""
        response = self.session.get(MAPPING_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()["1"], "Online")
        self.assertEqual(response.json()["2"], "In-Store")
        self.assertEqual(response.json()["3"], "Both")
