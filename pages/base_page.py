"""Base Page Object with shared helpers."""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all Page Objects.

    Provides common actions every page can reuse, such as navigating,
    reading the page title, and waiting for elements.
    """

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = "") -> "BasePage":
        """Open a page at the given path relative to the base URL."""
        self.page.goto(f"{self.base_url}/{path}".rstrip("/"))
        return self

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def wait_for_load(self) -> "BasePage":
        """Wait until the network is idle."""
        self.page.wait_for_load_state("networkidle")
        return self

    def fill(self, locator: str, value: str) -> "BasePage":
        """Fill an input field identified by a locator string."""
        self.page.locator(locator).fill(value)
        return self

    def click(self, locator: str) -> "BasePage":
        """Click an element identified by a locator string."""
        self.page.locator(locator).click()
        return self

    def expect_text(self, locator: str, text: str) -> None:
        """Assert that an element contains the expected text."""
        expect(self.page.locator(locator)).to_contain_text(text)

    def expect_visible(self, locator: str) -> None:
        """Assert that an element is visible."""
        expect(self.page.locator(locator)).to_be_visible()
