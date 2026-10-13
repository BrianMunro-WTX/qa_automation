# Basic pytest-playwright Test Examples

Simple, self-contained test scripts for learning pytest-playwright basics.
Copy any example into a file in `tests/` (e.g., `tests/test_example.py`) and run it.

These examples use the demo site [https://www.saucedemo.com](https://www.saucedemo.com),
which requires no account setup and is built for test automation practice.

**Run commands:**

```bash
pytest tests/test_example.py            # run headless
pytest tests/test_example.py --headed   # watch the browser
pytest -k test_navigation --headed      # run a single test
```

---

## 1. Basic Navigation & Page Info

```python
from playwright.sync_api import Page


def test_navigation(page: Page):
    page.goto("https://www.saucedemo.com")

    # Read page properties
    print(page.title())   # "Swag Labs"
    print(page.url)       # current URL

    # Browser history navigation
    page.reload()         # reload current page
    # page.go_back()      # back in history
    # page.go_forward()   # forward in history

    assert "Swag Labs" in page.title()
```

---

## 2. Finding Elements with Locators

```python
from playwright.sync_api import Page


def test_locators(page: Page):
    page.goto("https://www.saucedemo.com")

    # By placeholder text (best for inputs without labels)
    username = page.get_by_placeholder("Username")
    password = page.get_by_placeholder("Password")

    # By test id (data-test attribute on saucedemo)
    username_by_id = page.get_by_test_id("username")

    # By role (buttons, headings, links, etc.)
    login_button = page.get_by_role("button", name="Login")

    # Fallback: CSS selector
    css_input = page.locator("#user-name")

    # All these locate elements — nothing happens until an action/assertion
    assert username is not None
    assert css_input.count() == 1
```

---

## 3. Filling Inputs and Clicking

```python
from playwright.sync_api import Page


def test_fill_and_click(page: Page):
    page.goto("https://www.saucedemo.com")

    # fill() clears the field first, then types
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    # Click the login button
    page.get_by_role("button", name="Login").click()

    # After successful login we land on the inventory page
    assert "inventory" in page.url
```

---

## 4. Keyboard Actions

```python
from playwright.sync_api import Page


def test_keyboard(page: Page):
    page.goto("https://www.saucedemo.com")

    username = page.get_by_placeholder("Username")
    username.fill("standard_user")

    # Tab moves focus to the password field
    page.keyboard.press("Tab")
    page.keyboard.type("secret_sauce")

    # Press Enter instead of clicking the button
    page.keyboard.press("Enter")

    assert "inventory" in page.url
```

---

## 5. Basic Assertions with `expect`

```python
from playwright.sync_api import Page, expect


def test_basic_assertions(page: Page):
    page.goto("https://www.saucedemo.com")

    # Page-level assertions (auto-retry until timeout)
    expect(page).to_have_title("Swag Labs")
    expect(page).to_have_url("https://www.saucedemo.com/")

    # Element state assertions
    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_enabled()
```

---

## 6. Text Content Assertions

```python
from playwright.sync_api import Page, expect


def test_text_assertions(page: Page):
    page.goto("https://www.saucedemo.com")

    # Exact text match
    expect(page.locator(".login_logo")).to_have_text("Swag Labs")

    # Partial text match
    expect(page.locator(".login_logo")).to_contain_text("Swag")

    # Input value assertion
    page.get_by_placeholder("Username").fill("standard_user")
    expect(page.get_by_placeholder("Username")).to_have_value("standard_user")
```

---

## 7. Waiting for Elements and URLs

```python
from playwright.sync_api import Page, expect


def test_waiting(page: Page):
    page.goto("https://www.saucedemo.com")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # Explicitly wait for a URL change
    page.wait_for_url("**/inventory.html")

    # Explicitly wait for an element to appear
    page.locator(".inventory_list").wait_for(state="visible")

    # Note: expect() already auto-waits, so this usually suffices:
    expect(page.locator(".inventory_list")).to_be_visible()
```

---

## 8. Handling Login Errors

```python
from playwright.sync_api import Page, expect


def test_invalid_login_shows_error(page: Page):
    page.goto("https://www.saucedemo.com")

    page.get_by_placeholder("Username").fill("wrong_user")
    page.get_by_placeholder("Password").fill("wrong_pass")
    page.get_by_role("button", name="Login").click()

    # The error message appears — web-first assertion waits for it
    error = page.get_by_test_id("error")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")

    # Still on the login page
    expect(page).to_have_url("https://www.saucedemo.com/")
```

---

## 9. Filtering Locators

```python
from playwright.sync_api import Page, expect


def test_filtering_locators(page: Page):
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # Filter a list to the item containing specific text
    backpack = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")

    # Chain locators: find a button inside the filtered item
    backpack.get_by_role("button", name="Add to cart").click()

    # The cart badge now shows 1 item
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
```

---

## 10. Working with Multiple Elements

```python
from playwright.sync_api import Page, expect


def test_multiple_elements(page: Page):
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    products = page.locator(".inventory_item")

    # Count how many elements matched
    expect(products).to_have_count(6)

    # Pick individual elements from the list
    first_product = products.first
    last_product = products.last
    third_product = products.nth(2)   # zero-based index

    expect(first_product).to_be_visible()
    print(first_product.inner_text())
```

---

## 11. Dropdowns (select_option)

```python
from playwright.sync_api import Page, expect


def test_dropdown(page: Page):
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    sort_dropdown = page.get_by_test_id("product-sort-container")

    # Select by the option's value attribute
    sort_dropdown.select_option(value="lohi")   # Price: low to high

    # Verify the selected value
    expect(sort_dropdown).to_have_value("lohi")

    # Select by the visible label instead
    sort_dropdown.select_option(label="Name (Z to A)")
```

---

## 12. Checkboxes and Radio Buttons

```python
from playwright.sync_api import Page, expect


def test_checkboxes(page: Page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")

    checkboxes = page.get_by_role("checkbox")

    # check() / uncheck() handle the click for you
    checkboxes.first.check()
    checkboxes.nth(1).uncheck()

    # Assert their state
    expect(checkboxes.first).to_be_checked()
    expect(checkboxes.nth(1)).not_to_be_checked()
```

---

## 13. Hover and Links

```python
from playwright.sync_api import Page, expect


def test_hover_and_links(page: Page):
    page.goto("https://the-internet.herokuapp.com/hovers")

    avatar = page.locator(".figure").first

    # Hover reveals hidden content
    avatar.hover()
    expect(avatar.get_by_text("name: user1")).to_be_visible()

    # Click the link that appeared
    avatar.get_by_role("link", name="View profile").click()
    expect(page).to_have_url("https://the-internet.herokuapp.com/users/1")
```

---

## 14. Taking Screenshots

```python
from playwright.sync_api import Page, expect


def test_screenshots(page: Page):
    page.goto("https://www.saucedemo.com")

    # Screenshot the full page
    page.screenshot(path="login_page.png", full_page=True)

    # Screenshot a single element
    page.locator(".login_logo").screenshot(path="logo.png")

    expect(page.get_by_role("button", name="Login")).to_be_visible()
```

---

## 15. Using Pytest Fixtures (setup/teardown)

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def logged_in_page(page: Page):
    """A fixture that logs in before the test runs."""
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    yield page   # test runs here; code after yield is teardown


def test_inventory_visible(logged_in_page: Page):
    expect(logged_in_page.locator(".inventory_list")).to_be_visible()


def test_cart_starts_empty(logged_in_page: Page):
    expect(logged_in_page.locator(".shopping_cart_badge")).not_to_be_visible()
```

---

## Tips for Learners

- **`page` is a built-in fixture** from `pytest-playwright` — no browser setup code needed.
- **Never use `time.sleep()`** — Playwright auto-waits for elements and assertions retry automatically.
- **Use `playwright codegen https://www.saucedemo.com`** to record your clicks and generate starter code.
- **Use `page.pause()`** inside a test with `pytest --headed` to open the Playwright Inspector and debug interactively.
