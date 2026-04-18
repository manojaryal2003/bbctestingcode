import os
import time
import logging

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Load credentials from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

logger = logging.getLogger(__name__)

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def _build_driver():
    """Create and return a Chrome browser instance."""
    headless = os.getenv("HEADLESS", "false").lower() == "true"

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # webdriver-manager sometimes returns a non-.exe path — resolve it
    driver_path = ChromeDriverManager().install()
    if not driver_path.endswith(".exe"):
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")

    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.maximize_window()
    return driver


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    """Return the app's base URL (loaded from .env)."""
    return os.getenv("BASE_URL", "https://bbc.smartitsolutionnepal.com")


@pytest.fixture(scope="function")
def driver():
    """Give each test its own fresh browser. Closes after the test finishes."""
    drv = _build_driver()
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def admin_creds():
    return {"user_id": os.getenv("ADMIN_USER_ID"), "password": os.getenv("ADMIN_PASSWORD")}


@pytest.fixture(scope="session")
def franchise_creds():
    return {"user_id": os.getenv("FRANCHISE_USER_ID"), "password": os.getenv("FRANCHISE_PASSWORD")}


@pytest.fixture(scope="session")
def mentor_creds():
    return {"user_id": os.getenv("MENTOR_USER_ID"), "password": os.getenv("MENTOR_PASSWORD")}


@pytest.fixture(scope="session")
def student_creds():
    return {"user_id": os.getenv("STUDENT_USER_ID"), "password": os.getenv("STUDENT_PASSWORD")}


@pytest.fixture(scope="session")
def parent_creds():
    return {"user_id": os.getenv("PARENT_USER_ID"), "password": os.getenv("PARENT_PASSWORD")}


def _login(driver, base_url, user_id, password):
    """Log in with the given credentials and wait for the dashboard."""
    from pages.login_page import LoginPage
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    login_page = LoginPage(driver, base_url)
    login_page.open_login_page()
    login_page.login(user_id, password)
    WebDriverWait(driver, 15).until(EC.url_changes(f"{base_url}/login"))


@pytest.fixture(scope="function")
def admin_driver(base_url, admin_creds):
    """Browser already logged in as HEAD_ADMIN."""
    drv = _build_driver()
    _login(drv, base_url, admin_creds["user_id"], admin_creds["password"])
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def franchise_driver(base_url, franchise_creds):
    """Browser already logged in as FRANCHISE_ADMIN."""
    drv = _build_driver()
    _login(drv, base_url, franchise_creds["user_id"], franchise_creds["password"])
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def mentor_driver(base_url, mentor_creds):
    """Browser already logged in as MENTOR."""
    drv = _build_driver()
    _login(drv, base_url, mentor_creds["user_id"], mentor_creds["password"])
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def student_driver(base_url, student_creds):
    """Browser already logged in as STUDENT."""
    drv = _build_driver()
    _login(drv, base_url, student_creds["user_id"], student_creds["password"])
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def parent_driver(base_url, parent_creds):
    """Browser already logged in as PARENT."""
    drv = _build_driver()
    _login(drv, base_url, parent_creds["user_id"], parent_creds["password"])
    yield drv
    drv.quit()


# ── Screenshot on failure ──────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot automatically whenever a test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = None
        for fixture_name in ("driver", "admin_driver", "franchise_driver",
                             "mentor_driver", "student_driver", "parent_driver"):
            drv = item.funcargs.get(fixture_name)
            if drv:
                break

        if drv:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_name = item.nodeid.replace("/", "_").replace("::", "__").replace(" ", "-")
            filepath = os.path.join(SCREENSHOT_DIR, f"FAIL__{safe_name}__{timestamp}.png")
            try:
                drv.save_screenshot(filepath)
                if hasattr(report, "extra"):
                    import pytest_html
                    report.extra = getattr(report, "extra", [])
                    report.extra.append(pytest_html.extras.image(filepath))
            except Exception as exc:
                logger.warning("Could not save screenshot: %s", exc)
