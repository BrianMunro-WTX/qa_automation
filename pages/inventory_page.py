"""Page Object for the inventory page."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object representing the product inventory page."""

    # Selectors
    PRODUCT_TITLE = "[data-test='title']"
    INVENTORY_LIST = "[data-test='inventory-list']"
    SHOPPING_CART_BADGE = "[data-test='shopping-cart-badge']"
    ADD_TO_CART_BUTTON = "button[data-test^='add-to-cart']"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.path = "/inventory.html"

    def open(self) -> "InventoryPage":
        """Navigate directly to the inventory page.

        In a real test you usually reach this page by logging in.
        """
        self.page.goto(self.base_url + self.path)
        return self

    def expect_on_page(self) -> "InventoryPage":
        """Assert that we are on the inventory page."""
        self.expect_text(self.PRODUCT_TITLE, "Products")
        self.expect_visible(self.INVENTORY_LIST)
        return self

    def add_first_product_to_cart(self) -> "InventoryPage":
        """Add the first product in the list to the cart."""
        self.page.locator(self.ADD_TO_CART_BUTTON).first.click()
        return self

    def expect_cart_count(self, count: int) -> None:
        """Assert the shopping cart badge shows the expected count."""
        self.expect_text(self.SHOPPING_CART_BADGE, str(count))
