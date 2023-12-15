"""Contains the constants for the stores app."""

STORE_TYPE_CHOICES = ((1, "Online"), (2, "In-Store"), (3, "Both"))

STORE_TYPE_MAPPING = {index[0]: index[1] for index in STORE_TYPE_CHOICES}
