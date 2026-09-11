"""pytest fixtures for the test suite."""

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import get_base_url


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the application base URL."""
    return get_base_url()


@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """Provide a ready-to-use LoginPage object."""
    return LoginPage(page, base_url)


@pytest.fixture
def inventory_page(page: Page, base_url: str) -> InventoryPage:
    """Provide a ready-to-use InventoryPage object."""
    return InventoryPage(page, base_url)
