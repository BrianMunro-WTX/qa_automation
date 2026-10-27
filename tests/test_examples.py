"""Login tests WITHOUT the Page Object Model.

Every test repeats the same URL, selectors, and steps. Compare with
tests/test_login.py, which covers the same scenarios using LoginPage.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.login
@pytest.mark.smoke
def test_successful_login(page: Page, base_url: str) -> None:
    """A valid user can log in and reach the inventory page."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='title']")).to_contain_text("Products")
    expect(page.locator("[data-test='inventory-list']")).to_be_visible()


@pytest.mark.login
def test_locked_out_user_sees_error(page: Page, base_url: str) -> None:
    """A locked-out user sees an error and stays on the login page."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("locked_out_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Sorry, this user has been locked out"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_invalid_password_shows_error(page: Page, base_url: str) -> None:
    """A wrong password shows an error and stays on the login page."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("wrong_password")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Username and password do not match"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_missing_username_shows_error(page: Page, base_url: str) -> None:
    """Submitting without a username shows a validation error."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Username is required"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_missing_password_shows_error(page: Page, base_url: str) -> None:
    """Submitting without a password shows a validation error."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Password is required"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_error_message_can_be_dismissed(page: Page, base_url: str) -> None:
    """The login error disappears when the user closes it."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("wrong_password")
    page.locator("[data-test='login-button']").click()
    expect(page.locator("[data-test='error']")).to_be_visible()

    page.locator("[data-test='error-button']").click()

    expect(page.locator("[data-test='error']")).to_have_count(0)


@pytest.mark.login
def test_login_page_shows_expected_elements(page: Page, base_url: str) -> None:
    """The login form displays its fields, placeholders, and button."""
    page.goto(base_url)

    expect(page.locator("[data-test='username']")).to_be_visible()
    expect(page.locator("[data-test='password']")).to_be_visible()
    expect(page.locator("[data-test='login-button']")).to_be_visible()
    expect(page.locator("[data-test='username']")).to_have_attribute(
        "placeholder", "Username"
    )
    expect(page.locator("[data-test='password']")).to_have_attribute(
        "placeholder", "Password"
    )


@pytest.mark.login
def test_both_fields_empty_shows_error(page: Page, base_url: str) -> None:
    """Submitting an empty form shows the username-required error."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("")
    page.locator("[data-test='password']").fill("")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Username is required"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_username_is_case_sensitive(page: Page, base_url: str) -> None:
    """A username with the wrong capitalization is rejected."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("Standard_User")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Username and password do not match"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_username_with_trailing_space_is_rejected(page: Page, base_url: str) -> None:
    """Extra whitespace around the username is not trimmed."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user ")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Username and password do not match"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_sql_injection_style_input_is_rejected(page: Page, base_url: str) -> None:
    """Special characters are treated as plain text, not as a bypass."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("' OR 1=1 --")
    page.locator("[data-test='password']").fill("' OR 1=1 --")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Username and password do not match"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_enter_key_submits_login_form(page: Page, base_url: str) -> None:
    """Pressing Enter in the password field logs the user in."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='password']").press("Enter")

    expect(page.locator("[data-test='title']")).to_contain_text("Products")
    expect(page.locator("[data-test='inventory-list']")).to_be_visible()


@pytest.mark.login
def test_password_field_is_masked(page: Page, base_url: str) -> None:
    """Typed passwords are hidden from view."""
    page.goto(base_url)

    expect(page.locator("[data-test='password']")).to_have_attribute(
        "type", "password"
    )


@pytest.mark.login
def test_problem_user_can_log_in(page: Page, base_url: str) -> None:
    """The problem_user account can log in."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("problem_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='title']")).to_contain_text("Products")
    expect(page.locator("[data-test='inventory-list']")).to_be_visible()


@pytest.mark.login
def test_performance_glitch_user_can_log_in(page: Page, base_url: str) -> None:
    """The slow performance_glitch_user account can still log in."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("performance_glitch_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    expect(page.locator("[data-test='title']")).to_contain_text(
        "Products", timeout=15_000
    )
    expect(page.locator("[data-test='inventory-list']")).to_be_visible()


@pytest.mark.login
def test_logout_returns_to_login_page(page: Page, base_url: str) -> None:
    """Logging out returns the user to the login form."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page.locator("[data-test='title']")).to_contain_text("Products")

    page.locator("#react-burger-menu-btn").click()
    page.locator("[data-test='logout-sidebar-link']").click()

    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_protected_page_requires_login(page: Page, base_url: str) -> None:
    """Opening the inventory page without logging in is blocked."""
    page.goto(f"{base_url}/inventory.html")

    expect(page.locator("[data-test='error']")).to_contain_text(
        "You can only access '/inventory.html' when you are logged in"
    )
    expect(page.locator("[data-test='login-button']")).to_be_visible()


@pytest.mark.login
def test_session_persists_after_reload(page: Page, base_url: str) -> None:
    """A logged-in user stays logged in after refreshing the page."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page.locator("[data-test='title']")).to_contain_text("Products")

    page.reload()

    expect(page.locator("[data-test='title']")).to_contain_text("Products")
    expect(page.locator("[data-test='inventory-list']")).to_be_visible()


@pytest.mark.login
def test_back_button_after_logout_does_not_expose_inventory(
    page: Page, base_url: str
) -> None:
    """After logging out, the Back button must not show the inventory."""
    page.goto(base_url)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page.locator("[data-test='title']")).to_contain_text("Products")
    page.locator("#react-burger-menu-btn").click()
    page.locator("[data-test='logout-sidebar-link']").click()
    expect(page.locator("[data-test='login-button']")).to_be_visible()

    page.go_back()

    expect(page.locator("[data-test='inventory-list']")).to_have_count(0)
    expect(page.locator("[data-test='login-button']")).to_be_visible()