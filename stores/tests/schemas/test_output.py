"""Contains tests for the output schemas of the stores app."""


from stores.schemas.output import StoreAggregationSchema


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
