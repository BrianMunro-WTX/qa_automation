"""Page Object for the login page."""

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object representing https://www.saucedemo.com/."""

    # Selectors
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_DISMISS_BUTTON = "[data-test='error-button']"

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

    def login_with_enter_key(self, username: str, password: str) -> "LoginPage":
        """Fill in credentials and submit the form by pressing Enter."""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.page.locator(self.PASSWORD_INPUT).press("Enter")
        return self

    def expect_placeholders(self) -> "LoginPage":
        """Assert the input fields show helpful placeholder text."""
        expect(self.page.locator(self.USERNAME_INPUT)).to_have_attribute(
            "placeholder", "Username"
        )
        expect(self.page.locator(self.PASSWORD_INPUT)).to_have_attribute(
            "placeholder", "Password"
        )
        return self

    def expect_password_masked(self) -> "LoginPage":
        """Assert typed passwords are hidden from view."""
        expect(self.page.locator(self.PASSWORD_INPUT)).to_have_attribute(
            "type", "password"
        )
        return self

    def expect_on_page(self) -> "LoginPage":
        """Assert that the login form is displayed."""
        self.expect_visible(self.USERNAME_INPUT)
        self.expect_visible(self.PASSWORD_INPUT)
        self.expect_visible(self.LOGIN_BUTTON)
        return self

    def expect_login_error(self, message: str) -> None:
        """Assert the error message contains the expected text."""
        self.expect_text(self.ERROR_MESSAGE, message)

    def dismiss_error(self) -> "LoginPage":
        """Close the login error message."""
        self.click(self.ERROR_DISMISS_BUTTON)
        return self

    def expect_no_error(self) -> None:
        """Assert that no login error message is displayed."""
        expect(self.page.locator(self.ERROR_MESSAGE)).to_have_count(0)
