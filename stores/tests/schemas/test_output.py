"""Contains tests for the output schemas of the stores app."""


from stores.schemas.output import StoreAggregationSchema, StorePaginationSchema


def test_store_aggregation_default_values() -> None:
    """Test the default values of the store aggregation schema."""
    schema = StoreAggregationSchema()
    assert schema.total_stores == 0
    assert schema.online_stores == 0
    assert schema.in_store_stores == 0
    assert schema.combined_stores == 0
    assert schema.combined_online_stores == 0
    assert schema.combined_in_store_stores == 0


def test_store_aggregation_keys() -> None:
    """Test the keys of the store aggregation schema."""
    schema = StoreAggregationSchema()
    assert schema.dict().keys() == {
        "total_stores",
        "online_stores",
        "in_store_stores",
        "combined_stores",
        "combined_online_stores",
        "combined_in_store_stores",
    }


def test_store_pagination_default_values() -> None:
    """Test the default values of the store pagination schema."""
    schema = StorePaginationSchema()
    assert schema.stores == []
    assert schema.total == 0
    assert schema.page_number == 1
    assert schema.total_pages == 1
    assert schema.has_previous is False
    assert schema.previous_page is None
    assert schema.has_next is False
    assert schema.next_page is None


def test_store_pagination_keys() -> None:
    """Test the keys of the store pagination schema."""
    schema = StorePaginationSchema()
    assert schema.dict().keys() == {
        "stores",
        "total",
        "page_number",
        "total_pages",
        "has_previous",
        "previous_page",
        "has_next",
        "next_page",
    }
