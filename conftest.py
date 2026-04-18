"""
conftest.py — pytest configuration and shared fixtures.

Responsibilities:
  1. Load all credentials from .env via python-dotenv (NEVER hardcoded)
  2. Set up Chrome WebDriver with webdriver-manager (visible browser, headless=False)
  3. Provide a base `driver` fixture (function scope — fresh browser per test)
  4. Provide per-role credential fixtures: admin_creds, franchise_creds,
     mentor_creds, student_creds, parent_creds
  5. Provide pre-logged-in driver fixtures for each role:
     admin_driver, franchise_driver, mentor_driver, student_driver, parent_driver
  6. Auto-capture screenshots on EVERY test failure and attach to HTML report
  7. Expose BASE_URL as a pytest fixture
"""

import os
import time
import logging

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ── Load .env file ─────────────────────────────────────────────────────────────
# Resolves to testing/.env (same directory as this conftest.py)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

logger = logging.getLogger(__name__)

# ── Screenshot directory ───────────────────────────────────────────────────────
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ==============================================================================
# Helper: build a configured Chrome WebDriver
# ==============================================================================

def _build_driver() -> webdriver.Chrome:
    """
    Create and return a configured Chrome WebDriver instance.

    - headless controlled by HEADLESS env var (default False = visible)
    - window maximised for consistent element visibility
    - webdriver-manager auto-downloads the matching ChromeDriver
    """
    headless = os.getenv("HEADLESS", "false").lower() == "true"

    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")   # Chrome 112+ headless mode

    # Stability flags
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")

    # Suppress "Chrome is being controlled by automated test software" banner
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # webdriver-manager 4.x bug: .install() may return a license/notice file
    # instead of chromedriver.exe — resolve to the actual executable.
    driver_path = ChromeDriverManager().install()
    if not driver_path.endswith(".exe"):
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    return driver


# ==============================================================================
# Core fixtures
# ==============================================================================

@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Return the live application base URL loaded from .env.

    Scope: session — shared across all tests (URL never changes mid-run).
    """
    url = os.getenv("BASE_URL", "https://bbc.smartitsolutionnepal.com")
    logger.info("BASE_URL = %s", url)
    return url


@pytest.fixture(scope="function")
def driver():
    """
    Provide a fresh Chrome WebDriver for each test function.

    Scope: function — each test gets its own browser instance, ensuring
    full test independence (no shared state / cookies between tests).

    Teardown: driver.quit() is called after every test, even on failure.
    """
    drv = _build_driver()
    logger.info("Browser opened for test")
    yield drv
    logger.info("Browser closed after test")
    drv.quit()


# ==============================================================================
# Credential fixtures — loaded from .env, never hardcoded
# ==============================================================================

@pytest.fixture(scope="session")
def admin_creds() -> dict:
    """
    Return HEAD_ADMIN credentials as a dict.

    Keys: user_id, password
    Source: ADMIN_USER_ID and ADMIN_PASSWORD in .env
    """
    return {
        "user_id": os.getenv("ADMIN_USER_ID"),
        "password": os.getenv("ADMIN_PASSWORD"),
    }


@pytest.fixture(scope="session")
def franchise_creds() -> dict:
    """
    Return FRANCHISE_ADMIN credentials as a dict.

    Keys: user_id, password
    Source: FRANCHISE_USER_ID and FRANCHISE_PASSWORD in .env
    """
    return {
        "user_id": os.getenv("FRANCHISE_USER_ID"),
        "password": os.getenv("FRANCHISE_PASSWORD"),
    }


@pytest.fixture(scope="session")
def mentor_creds() -> dict:
    """
    Return MENTOR credentials as a dict.

    Keys: user_id, password
    Source: MENTOR_USER_ID and MENTOR_PASSWORD in .env
    """
    return {
        "user_id": os.getenv("MENTOR_USER_ID"),
        "password": os.getenv("MENTOR_PASSWORD"),
    }


@pytest.fixture(scope="session")
def student_creds() -> dict:
    """
    Return STUDENT credentials as a dict.

    Keys: user_id, password
    Source: STUDENT_USER_ID and STUDENT_PASSWORD in .env
    """
    return {
        "user_id": os.getenv("STUDENT_USER_ID"),
        "password": os.getenv("STUDENT_PASSWORD"),
    }


@pytest.fixture(scope="session")
def parent_creds() -> dict:
    """
    Return PARENT credentials as a dict.

    Keys: user_id, password
    Source: PARENT_USER_ID and PARENT_PASSWORD in .env
    """
    return {
        "user_id": os.getenv("PARENT_USER_ID"),
        "password": os.getenv("PARENT_PASSWORD"),
    }


# ==============================================================================
# Pre-logged-in driver fixtures (one per role)
# ==============================================================================

def _login(driver, base_url: str, user_id: str, password: str):
    """
    Shared login helper used by all role-specific driver fixtures.

    Navigates to /login, fills credentials, submits, and waits for
    the dashboard URL to appear in the address bar.
    """
    from pages.login_page import LoginPage

    login_page = LoginPage(driver, base_url)
    login_page.open_login_page()
    login_page.login(user_id, password)

    # Wait up to 15 s for redirect away from /login
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    WebDriverWait(driver, 15).until(EC.url_changes(f"{base_url}/login"))
    logger.info("Login successful — redirected to: %s", driver.current_url)


@pytest.fixture(scope="function")
def admin_driver(base_url, admin_creds):
    """
    Provide a Chrome WebDriver already logged in as HEAD_ADMIN.

    Scope: function — fresh browser + fresh login for each test.
    """
    drv = _build_driver()
    _login(drv, base_url, admin_creds["user_id"], admin_creds["password"])
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def franchise_driver(base_url, franchise_creds):
    """
    Provide a Chrome WebDriver already logged in as FRANCHISE_ADMIN.

    Scope: function — fresh browser + fresh login for each test.
    """
    drv = _build_driver()
    _login(drv, base_url, franchise_creds["user_id"], franchise_creds["password"])
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def mentor_driver(base_url, mentor_creds):
    """
    Provide a Chrome WebDriver already logged in as MENTOR.

    Scope: function — fresh browser + fresh login for each test.
    """
    drv = _build_driver()
    _login(drv, base_url, mentor_creds["user_id"], mentor_creds["password"])
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def student_driver(base_url, student_creds):
    """
    Provide a Chrome WebDriver already logged in as STUDENT.

    Scope: function — fresh browser + fresh login for each test.
    """
    drv = _build_driver()
    _login(drv, base_url, student_creds["user_id"], student_creds["password"])
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def parent_driver(base_url, parent_creds):
    """
    Provide a Chrome WebDriver already logged in as PARENT.

    Scope: function — fresh browser + fresh login for each test.
    """
    drv = _build_driver()
    _login(drv, base_url, parent_creds["user_id"], parent_creds["password"])
    yield drv
    drv.quit()


# ==============================================================================
# Screenshot-on-failure hook
# ==============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    After every test phase (setup / call / teardown):
      - If the test FAILED, capture a screenshot and embed it in the HTML report.

    The screenshot filename encodes the test node ID and a timestamp so
    multiple failures never overwrite each other.
    """
    outcome = yield
    report = outcome.get_result()

    # Only act on the 'call' phase (actual test body) and only on failure
    if report.when == "call" and report.failed:
        # Try to get the driver from the test's fixtures
        drv = None
        for fixture_name in ("driver", "admin_driver", "franchise_driver",
                             "mentor_driver", "student_driver", "parent_driver"):
            drv = item.funcargs.get(fixture_name)
            if drv is not None:
                break

        if drv is not None:
            timestamp   = time.strftime("%Y%m%d_%H%M%S")
            # Sanitise the node id to make it safe as a filename
            safe_name   = item.nodeid.replace("/", "_").replace("::", "__").replace(" ", "-")
            filename    = f"FAIL__{safe_name}__{timestamp}.png"
            filepath    = os.path.join(SCREENSHOT_DIR, filename)

            try:
                drv.save_screenshot(filepath)
                logger.info("Failure screenshot saved: %s", filepath)

                # Embed screenshot in pytest-html report
                if hasattr(report, "extra"):
                    import pytest_html
                    report.extra = getattr(report, "extra", [])
                    report.extra.append(pytest_html.extras.image(filepath))
            except Exception as exc:
                logger.warning("Could not capture failure screenshot: %s", exc)
