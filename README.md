# QA Automation with Python, pytest & Playwright

A teaching repository for test automation using the **Page Object Model (POM)** pattern with **Python**, **pytest**, and **Playwright**.

## What you will learn

- How to structure a Python test automation project.
- How to write pytest test cases.
- How to use Playwright for browser automation.
- How to apply the Page Object Model pattern to keep tests maintainable.
- How to run tests locally and in CI.

## Tech stack

- Python 3.12+
- pytest
- pytest-playwright
- Playwright

## Project structure

```
qa_automation/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI workflow
├── docs/
│   └── structure.md         # Project structure explained
├── pages/
│   ├── __init__.py
│   ├── base_page.py         # Shared page actions and helpers
│   ├── login_page.py        # Page Object for the login page
│   └── inventory_page.py    # Page Object for the inventory page
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   ├── requirements.txt     # Python dependencies
│   ├── test_login.py        # Login tests
│   └── test_inventory.py    # Inventory tests
├── utils/
│   ├── __init__.py
│   └── config.py            # Configuration helpers
├── .gitignore
├── pytest.ini               # pytest configuration
└── README.md
```

## Getting started

### 1. Clone the repository

```bash
git clone <repo-url>
cd qa_automation
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r tests/requirements.txt
playwright install
```

### 4. Run the tests

```bash
pytest
```

Run with a visible browser (headed mode):

```bash
pytest --headed --slowmo 500
```

Run a specific test file:

```bash
pytest tests/test_login.py
```

Run with the HTML report:

```bash
pytest --html=report.html --self-contained-html
```

> Note: `pytest-html` is optional. Install it with `pip install pytest-html` if you want HTML reports.

## Configuration

Default settings live in `utils/config.py`. You can override the base URL with an environment variable:

```bash
BASE_URL=https://www.saucedemo.com pytest
```

## Page Object Model (POM)

The POM pattern separates page-specific selectors and actions from test logic.

- `pages/base_page.py` — common methods every page can reuse.
- `pages/login_page.py` — encapsulates the login page.
- `pages/inventory_page.py` — encapsulates the inventory page.
- `tests/conftest.py` — pytest fixtures that provide ready-to-use page objects.

This makes tests easier to read, maintain, and update when the UI changes.

## Demo site

Tests use the public demo site [https://www.saucedemo.com](https://www.saucedemo.com).

## Useful links

- [pytest documentation](https://docs.pytest.org/)
- [Playwright for Python](https://playwright.dev/python/)
- [pytest-playwright](https://github.com/microsoft/playwright-pytest)
