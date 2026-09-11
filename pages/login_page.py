"""Page Object for the login page."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object representing https://www.saucedemo.com/."""

    # Selectors
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.path = "/"

    def open(self) -> "LoginPage":
        """Navigate to the login page."""
        self.page.goto(self.base_url + self.path)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Fill in credentials and submit the login form."""
        self.page.locator(self.USERNAME_INPUT).fill(username)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()
        return self

    def expect_login_error(self, message: str) -> None:
        """Assert the error message contains the expected text."""
        self.expect_text(self.ERROR_MESSAGE, message)
