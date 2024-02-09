"""Contains integration tests for the stores endpoints."""

import requests

from tests.acceptance.base_test_case import BaseTestCase

CREATE_URL = "http://localhost:7001/api/v1/stores/create"
DETAIL_URL = "http://localhost:7001/api/v1/stores/detail"
MAPPING_URL = "http://localhost:7001/api/v1/stores/types/mapping"
AGGREGATION_URL = "http://localhost:7001/api/v1/stores/aggregate"
PERSONAL_STORES_URL = "http://localhost:7001/api/v1/stores/me"
UPDATE_STORE_URL = "http://localhost:7001/api/v1/stores/update"
DELETE_STORE_URL = "http://localhost:7001/api/v1/stores/delete"


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

    def test_3_get_store_detail(self) -> None:
        """Test that a user can get the store detail."""
        response = self.session.get(f"{DETAIL_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Base Test Store")
        self.assertEqual(response.json()["description"], "This is a test store.")
        self.assertEqual(response.json()["store_type"], 3)
        self.assertEqual(response.json()["id"], 1)
        self.assertIsInstance(response.json()["created_at"], str)
        self.assertIsInstance(response.json()["updated_at"], str)
        self.assertEqual(response.json()["user"]["username"], "basetestuser1")

    def test_4_get_store_detail_invalid_id(self) -> None:
        """Test that a user can get the store detail."""
        response = self.session.get(f"{DETAIL_URL}/4000")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Store with id '4000' does not exist.")

    def test_5_get_store_aggregation(self) -> None:
        """Test that a user can get the store aggregation."""
        response = self.session.get(AGGREGATION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["total_stores"], int)
        self.assertIsInstance(response.json()["online_stores"], int)
        self.assertIsInstance(response.json()["in_store_stores"], int)
        self.assertIsInstance(response.json()["combined_stores"], int)
        self.assertIsInstance(response.json()["combined_online_stores"], int)
        self.assertIsInstance(response.json()["combined_in_store_stores"], int)

    def test_6_get_store_aggregation_personal(self) -> None:
        """Test that a user can get the store aggregation."""
        response = self.session.get(f"{AGGREGATION_URL}/me")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["total_stores"], int)
        self.assertIsInstance(response.json()["online_stores"], int)
        self.assertIsInstance(response.json()["in_store_stores"], int)
        self.assertIsInstance(response.json()["combined_stores"], int)
        self.assertIsInstance(response.json()["combined_online_stores"], int)
        self.assertIsInstance(response.json()["combined_in_store_stores"], int)

    def test_7_update_store(self) -> None:
        """Test that a user can update the store."""
        store_response = self.session.get(PERSONAL_STORES_URL)
        store_response_json = store_response.json()

        store_to_update = store_response_json.get("stores")[0]

        for store in store_response_json.get("stores"):
            if store.get("name") == "StoreTester1":
                store_to_update = store
                break

        store_update_response = self.session.put(
            f"{UPDATE_STORE_URL}/{store_to_update.get('id')}?store_type=1"
        )
        self.assertEqual(store_update_response.status_code, 200)

        response_json = store_update_response.json()
        self.assertEqual(response_json.get("id"), store_to_update.get("id"))
        self.assertEqual(response_json.get("name"), store_to_update.get("name"))
        self.assertEqual(response_json.get("store_type"), 1)
        self.assertEqual(response_json.get("description"), store_to_update.get("description"))

    def test_8_delete_store(self) -> None:
        """Test that a use can delete the store."""
        store_response = self.session.get(PERSONAL_STORES_URL)
        store_response_json = store_response.json()

        store_to_delete = store_response_json.get("stores")[0]

        for store in store_response_json.get("stores"):
            if store.get("name") == "StoreTester1":
                store_to_delete = store
                break

        store_delete_response = self.session.delete(
            f"{DELETE_STORE_URL}/{store_to_delete.get('id')}"
        )
        self.assertEqual(store_delete_response.status_code, 200)

        response_json = store_delete_response.json()
        self.assertEqual(response_json.get("message"), "Deleted Store.")
        self.assertEqual(
            response_json.get("detail"), f"Store with ID #{store_to_delete.get('id')} was deleted."
        )
