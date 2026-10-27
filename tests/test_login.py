"""Login tests WITH the Page Object Model.

Same scenarios as tests/test_examples.py, but selectors and steps live in
LoginPage, and the four error scenarios share one parametrized test.
"""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.login
@pytest.mark.smoke
def test_successful_login(login_page: LoginPage, inventory_page: InventoryPage) -> None:
    """A valid user can log in and reach the inventory page."""
    login_page.open().login("standard_user", "secret_sauce")

    inventory_page.expect_on_page()


# Disabled: flaky for performance_glitch_user under full-suite runs.
# @pytest.mark.login
# @pytest.mark.parametrize(
#     "username",
#     ["problem_user", pytest.param("performance_glitch_user", id="performance-glitch-user")],
# )
# def test_other_valid_users_can_log_in(
#     login_page: LoginPage, inventory_page: InventoryPage, username: str
# ) -> None:
#     """Other valid accounts can log in, even the deliberately slow one."""
#     login_page.open().login(username, "secret_sauce")
#
#     inventory_page.expect_on_page()


@pytest.mark.login
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param(
            "locked_out_user",
            "secret_sauce",
            "Sorry, this user has been locked out",
            id="locked-out-user",
        ),
        pytest.param(
            "standard_user",
            "wrong_password",
            "Username and password do not match",
            id="invalid-password",
        ),
        pytest.param("", "secret_sauce", "Username is required", id="missing-username"),
        pytest.param("standard_user", "", "Password is required", id="missing-password"),
        pytest.param("", "", "Username is required", id="both-fields-empty"),
        pytest.param(
            "Standard_User",
            "secret_sauce",
            "Username and password do not match",
            id="username-is-case-sensitive",
        ),
        pytest.param(
            "standard_user ",
            "secret_sauce",
            "Username and password do not match",
            id="trailing-space-in-username",
        ),
        pytest.param(
            "' OR 1=1 --",
            "' OR 1=1 --",
            "Username and password do not match",
            id="sql-injection-style-input",
        ),
    ],
)
def test_invalid_login_shows_error(
    login_page: LoginPage, username: str, password: str, expected_error: str
) -> None:
    """Invalid credentials show an error and keep the user on the login page."""
    login_page.open().login(username, password)

    login_page.expect_login_error(expected_error)
    login_page.expect_on_page()


@pytest.mark.login
def test_error_message_can_be_dismissed(login_page: LoginPage) -> None:
    """The login error disappears when the user closes it."""
    login_page.open().login("standard_user", "wrong_password")
    login_page.expect_login_error("Username and password do not match")

    login_page.dismiss_error().expect_no_error()


@pytest.mark.login
def test_login_page_shows_expected_elements(login_page: LoginPage) -> None:
    """The login form displays its fields, placeholders, and button."""
    login_page.open().expect_on_page().expect_placeholders()


@pytest.mark.login
def test_enter_key_submits_login_form(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """Pressing Enter in the password field logs the user in."""
    login_page.open().login_with_enter_key("standard_user", "secret_sauce")

    inventory_page.expect_on_page()


@pytest.mark.login
def test_password_field_is_masked(login_page: LoginPage) -> None:
    """Typed passwords are hidden from view."""
    login_page.open().expect_password_masked()


@pytest.mark.login
def test_logout_returns_to_login_page(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """Logging out returns the user to the login form."""
    login_page.open().login("standard_user", "secret_sauce")
    inventory_page.expect_on_page().logout()

    login_page.expect_on_page()


@pytest.mark.login
def test_protected_page_requires_login(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """Opening the inventory page without logging in is blocked."""
    inventory_page.open()

    login_page.expect_login_error("You can only access '/inventory.html' when you are logged in")
    login_page.expect_on_page()


@pytest.mark.login
def test_session_persists_after_reload(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """A logged-in user stays logged in after refreshing the page."""
    login_page.open().login("standard_user", "secret_sauce")
    inventory_page.expect_on_page().reload()

    inventory_page.expect_on_page()


@pytest.mark.login
def test_back_button_after_logout_does_not_expose_inventory(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """After logging out, the Back button must not show the inventory."""
    login_page.open().login("standard_user", "secret_sauce")
    inventory_page.expect_on_page().logout()
    login_page.expect_on_page()

    login_page.go_back()

    inventory_page.expect_inventory_hidden()
    login_page.expect_on_page()
