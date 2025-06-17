"""Contains the repositories for the stores app."""

import logging

from stores.database.interfaces.i_store_repo import IStoreRepo
from stores.database.store_repo import StoreRepo

log = logging.getLogger(__name__)

__all__ = ["IStoreRepo", "StoreRepo"]
