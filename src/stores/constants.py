"""Contains the constants for the stores app."""

import logging

log = logging.getLogger(__name__)
log.info("Stores app constants loading...")

STORE_TYPE_CHOICES = ((1, "Online"), (2, "In-Store"), (3, "Both"))

STORE_TYPE_MAPPING = {index[0]: index[1] for index in STORE_TYPE_CHOICES}

log.info("Stores app constants loaded.")
