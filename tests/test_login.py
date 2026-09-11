"""Tests for the login flow."""

import pytest

from pages.login_page import LoginPage


@pytest.mark.login
@pytest.mark.smoke
class TestLogin:
    """Login-related tests using the Page Object Model."""

    def test_successful_login(self, login_page: LoginPage, inventory_page):
        """A valid user can log in and reach the inventory page."""
        login_page.open().login("standard_user", "secret_sauce")
        inventory_page.expect_on_page()

    def test_locked_out_user_sees_error(self, login_page: LoginPage):
        """A locked-out user sees an appropriate error message."""
        login_page.open().login("locked_out_user", "secret_sauce")
        login_page.expect_login_error("Epic sadface")

    def test_invalid_password_shows_error(self, login_page: LoginPage):
        """An invalid password shows an error message."""
        login_page.open().login("standard_user", "wrong_password")
        login_page.expect_login_error("Username and password do not match")
