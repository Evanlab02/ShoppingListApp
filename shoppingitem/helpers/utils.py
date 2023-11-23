"""Contains utility functions for the shoppingitem app."""


def determine_average_price_of_items(total_price: int, total_items: int) -> float:
    """
    Determine the average price of items.

    Args:
        total_price(int): The total price of all items.
        total_items(int): The total number of items.

    Returns:
        float: The average price of items.
    """
    average_price = float(0)

    if total_items > 0:
        average_price = total_price / total_items
        average_price = round(average_price, 2)
    return average_price
