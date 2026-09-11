# Project Structure Explained

This document explains how the repository is organized and why.

## Folder layout

```
qa_automation/
├── .github/workflows/     # Continuous integration configuration
├── docs/                  # Documentation for learners
├── pages/                 # Page Object Models (POM)
├── tests/                 # pytest test cases and fixtures
├── utils/                 # Shared helpers and configuration
├── .gitignore             # Files and folders ignored by git
├── pytest.ini             # pytest settings
└── README.md              # Project overview
```

## `pages/` — Page Object Models

Each file represents one page of the application under test.

- `base_page.py` contains methods shared by all pages (e.g., `goto`, `fill`, `click`).
- `login_page.py` contains selectors and actions specific to the login page.
- `inventory_page.py` contains selectors and actions specific to the inventory page.

By keeping locators in one place, tests stay clean and UI changes only require updates in one location.

## `tests/` — Test cases

- `conftest.py` defines pytest fixtures, such as ready-to-use page objects.
- `test_login.py` and `test_inventory.py` contain the actual test cases.
- `requirements.txt` lists the Python dependencies.

## `utils/` — Shared helpers

- `config.py` reads environment variables and provides default values.

## `pytest.ini`

Centralizes pytest options so every run uses the same defaults:

- Verbose output (`-v`)
- Default browser (`chromium`)
- Base URL for the demo site
- Tracing and screenshots on failure

## Why Page Object Model?

Without POM, tests mix selectors with assertions:

```python
def test_login(page):
    page.goto("https://www.saucedemo.com")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    assert page.locator("[data-test='title']").text_content() == "Products"
```

With POM, the test reads like a user story:

```python
def test_successful_login(login_page, inventory_page):
    login_page.open().login("standard_user", "secret_sauce")
    inventory_page.expect_on_page()
```

Selectors and low-level interactions live in the page objects, making tests easier to maintain.
