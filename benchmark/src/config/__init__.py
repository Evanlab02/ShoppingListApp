"""Contains the config and config loaders for the benchmarking tool."""

import logging

from config.loaders import load_login_config

log = logging.getLogger(__name__)
log.info("Loading configs...")
USER_LOGIN = load_login_config()
log.info("Configs loaded successfully.")


__all__ = ["USER_LOGIN"]
