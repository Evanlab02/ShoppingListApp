"""Stress testing the Django application."""

from threading import Thread

import requests


def stress_test_items_page() -> None:
    """Stress test the items page."""
    for _ in range(1000):
        response = requests.get("http://192.168.0.2:8000/items/")
        if response.status_code != 200:
            print("X", end="")
        else:
            print(".", end="")

    print("\nDone")


def stress_test_stores_page() -> None:
    """Stress test the stores page."""
    for _ in range(1000):
        response = requests.get("http://192.168.0.2:8000/stores/")
        if response.status_code != 200:
            print("X", end="")
        else:
            print(".", end="")

    print("\nDone")


def single_test() -> None:
    """Single test for the items page."""
    response = requests.get("http://192.168.0.2:8000/items/")
    print(response.status_code)
    print(response.content)


t1 = Thread(target=stress_test_items_page)
t2 = Thread(target=stress_test_items_page)
t3 = Thread(target=stress_test_items_page)
t4 = Thread(target=stress_test_items_page)

t5 = Thread(target=stress_test_stores_page)
t6 = Thread(target=stress_test_stores_page)
t7 = Thread(target=stress_test_stores_page)
t8 = Thread(target=stress_test_stores_page)

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
