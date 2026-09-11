"""Configuration helpers."""

import os

DEFAULT_BASE_URL = "https://www.saucedemo.com"


def get_base_url() -> str:
    """Return the base URL for the application under test.

    Reads from the BASE_URL environment variable or falls back to
    the default Sauce Demo URL.
    """
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")
