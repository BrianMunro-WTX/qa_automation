"""Tests for the inventory page."""

import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.inventory
class TestInventory:
    """Inventory-page tests using the Page Object Model."""

    @pytest.fixture(autouse=True)
    def login(self, login_page: LoginPage, inventory_page: InventoryPage):
        """Log in before every inventory test."""
        login_page.open().login("standard_user", "secret_sauce")
        inventory_page.expect_on_page()

    def test_inventory_page_loads(self, inventory_page: InventoryPage):
        """The inventory page loads with products visible."""
        inventory_page.expect_on_page()

    def test_add_first_product_to_cart(self, inventory_page: InventoryPage):
        """Adding a product to the cart updates the cart badge."""
        inventory_page.add_first_product_to_cart()
        inventory_page.expect_cart_count(1)
