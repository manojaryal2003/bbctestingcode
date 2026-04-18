"""
Base Page — Page Object Model foundation class.

Every page object inherits from BasePage. It provides:
  - A consistent driver reference
  - Explicit wait helpers (NO time.sleep anywhere)
  - Multi-selector fallback strategy (NAME → ID → CSS → XPATH)
  - Screenshot capture on demand (called automatically on failure via conftest)
  - Reusable interaction methods used by all child page objects
"""

import os
import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)

logger = logging.getLogger(__name__)

# Folder where failure screenshots are saved (created if absent)
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")


class BasePage:
    """
    Foundation class for all Page Objects.

    Args:
        driver: Selenium WebDriver instance (passed from conftest fixture)
        timeout: Default explicit-wait timeout in seconds (overridable per call)
    """

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _find_element(self, locator: tuple):
        """
        Attempt to locate an element using the supplied (By, value) locator tuple.
        Raises NoSuchElementException if the element cannot be found.
        """
        return self.driver.find_element(*locator)

    def _find_with_fallback(self, name: str = None, id_: str = None,
                            css: str = None, xpath: str = None):
        """
        Multi-selector fallback strategy.
        Tries NAME → ID → CSS_SELECTOR → XPATH in order.
        Returns the first element that is successfully located.

        At least one selector must be provided.
        Raises NoSuchElementException if all selectors fail.
        """
        strategies = []
        if name:
            strategies.append((By.NAME, name))
        if id_:
            strategies.append((By.ID, id_))
        if css:
            strategies.append((By.CSS_SELECTOR, css))
        if xpath:
            strategies.append((By.XPATH, xpath))

        last_exc = None
        for locator in strategies:
            try:
                return self.driver.find_element(*locator)
            except NoSuchElementException as exc:
                last_exc = exc
                continue

        raise NoSuchElementException(
            f"Element not found with any selector — name={name}, id={id_}, "
            f"css={css}, xpath={xpath}"
        ) from last_exc

    # ── Public API (required by task spec) ───────────────────────────────────

    def wait_for_element(self, locator: tuple, timeout: int = None):
        """
        Wait until element identified by `locator` is visible in the DOM.

        Args:
            locator: (By.X, "value") tuple
            timeout: seconds to wait (defaults to self.timeout)

        Returns:
            WebElement once visible

        Raises:
            TimeoutException if element does not appear within timeout
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug("Element visible: %s", locator)
            return element
        except TimeoutException:
            logger.error("Timeout waiting for element: %s (after %ss)", locator, wait_time)
            raise

    def wait_for_element_clickable(self, locator: tuple, timeout: int = None):
        """Wait until element is present AND clickable."""
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_url_contains(self, partial_url: str, timeout: int = None):
        """Wait until the browser URL contains `partial_url`."""
        wait_time = timeout or self.timeout
        WebDriverWait(self.driver, wait_time).until(
            EC.url_contains(partial_url)
        )

    def wait_for_page_load(self, timeout: int = None):
        """Wait until document.readyState is 'complete'."""
        wait_time = timeout or self.timeout
        WebDriverWait(self.driver, wait_time).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def click_element(self, locator: tuple):
        """
        Wait for `locator` to be clickable, then click it.

        Args:
            locator: (By.X, "value") tuple
        """
        element = self.wait_for_element_clickable(locator)
        element.click()
        logger.debug("Clicked element: %s", locator)

    def enter_text(self, locator: tuple, text: str):
        """
        Wait for `locator` to be visible, clear any existing value, then type `text`.

        Args:
            locator: (By.X, "value") tuple
            text:    string to type into the element
        """
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
        logger.debug("Entered text into %s: '%s'", locator, text)

    def get_text(self, locator: tuple) -> str:
        """
        Wait for `locator` to be visible and return its visible text.

        Returns:
            Stripped text content of the element
        """
        element = self.wait_for_element(locator)
        return element.text.strip()

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Non-raising visibility check.

        Returns:
            True if the element is visible within `timeout` seconds, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def take_screenshot(self, name: str):
        """
        Capture a PNG screenshot and save it to the screenshots/ folder.

        Args:
            name: filename base (without extension). Timestamp is appended
                  to avoid collisions across test runs.

        Returns:
            Full path of the saved screenshot file
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_name = name.replace(" ", "_").replace("/", "-")
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        logger.info("Screenshot saved: %s", filepath)
        return filepath

    # ── Navigation helpers ────────────────────────────────────────────────────

    def open(self, url: str):
        """Navigate to `url` and wait for the page to fully load."""
        self.driver.get(url)
        self.wait_for_page_load()
        logger.debug("Navigated to: %s", url)

    def get_current_url(self) -> str:
        """Return the browser's current URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Return the browser tab title."""
        return self.driver.title

    def refresh(self):
        """Reload the current page."""
        self.driver.refresh()
        self.wait_for_page_load()

    # ── Utility helpers ───────────────────────────────────────────────────────

    def is_text_present(self, text: str) -> bool:
        """Return True if `text` appears anywhere in the page source."""
        return text.lower() in self.driver.page_source.lower()

    def scroll_to_element(self, locator: tuple):
        """Scroll the element into view using JavaScript."""
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_element_attribute(self, locator: tuple, attribute: str) -> str:
        """Return the value of `attribute` on the element at `locator`."""
        element = self.wait_for_element(locator)
        return element.get_attribute(attribute)

    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = None):
        """Wait until the element at `locator` is no longer visible."""
        wait_time = timeout or self.timeout
        WebDriverWait(self.driver, wait_time).until(
            EC.invisibility_of_element_located(locator)
        )
