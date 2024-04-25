"""Contains API stress testing functions."""

import os
from threading import Thread

import requests

COUNTER = 100
AUTH_HEADER = {"X-API-Key": os.getenv("API_KEY", "")}
HEADER = AUTH_HEADER


def create_session_auth() -> requests.Session:
    """Create a session with authentication."""
    session = requests.Session()
    session.headers.update(HEADER)
    session.post(
        "http://192.168.0.2:8000/api/v1/auth/login",
        json={"username": os.getenv("USERNAME", ""), "password": os.getenv("PASSWORD", "")},
    )
    return session


def stress_test_stores_api() -> None:
    """Stress test the stores API."""
    session = create_session_auth()
    for _ in range(COUNTER):
        response = session.get("http://192.168.0.2:8000/api/v1/stores", headers=HEADER)
        if response.status_code == 200:
            print(".", end="")
        else:
            print("X", end="")
    print("\nDone")


def stress_test_stores_aggregation_api() -> None:
    """Stress test the stores aggregation API."""
    session = create_session_auth()
    for _ in range(COUNTER):
        response = session.get("http://192.168.0.2:8000/api/v1/stores/aggregate", headers=HEADER)
        if response.status_code == 200:
            print(".", end="")
        else:
            print("X", end="")

    print("\nDone")


def stress_test_items_api() -> None:
    """Stress test the items API."""
    session = create_session_auth()
    for _ in range(COUNTER):
        response = session.get("http://192.168.0.2:8000/api/v1/items", headers=HEADER)
        if response.status_code == 200:
            print(".", end="")
        else:
            print("X", end="")

    print("\nDone")


def stress_test_items_aggregation_api() -> None:
    """Stress test the items aggregation API."""
    session = create_session_auth()
    for _ in range(COUNTER):
        response = session.get("http://192.168.0.2:8000/api/v1/items/aggregate", headers=HEADER)
        if response.status_code == 200:
            print(".", end="")
        else:
            print("X", end="")

    print("\nDone")


t1 = Thread(target=stress_test_stores_api)
t2 = Thread(target=stress_test_stores_aggregation_api)
t3 = Thread(target=stress_test_items_api)
t4 = Thread(target=stress_test_items_aggregation_api)
t5 = Thread(target=stress_test_stores_api)
t6 = Thread(target=stress_test_stores_aggregation_api)
t7 = Thread(target=stress_test_items_api)
t8 = Thread(target=stress_test_items_aggregation_api)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
