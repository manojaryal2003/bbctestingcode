import os
import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")


class BasePage:
    """Base class that all page objects inherit from."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    def wait_for_element(self, locator, timeout=None):
        """Wait until an element is visible on the page."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait until an element can be clicked."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_url_contains(self, partial_url, timeout=None):
        """Wait until the browser URL contains the given text."""
        t = timeout or self.timeout
        WebDriverWait(self.driver, t).until(EC.url_contains(partial_url))

    def wait_for_page_load(self, timeout=None):
        """Wait until the page is fully loaded."""
        t = timeout or self.timeout
        WebDriverWait(self.driver, t).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait until an element is no longer visible."""
        t = timeout or self.timeout
        WebDriverWait(self.driver, t).until(
            EC.invisibility_of_element_located(locator)
        )

    def click_element(self, locator):
        """Click an element after waiting for it to be clickable."""
        element = self.wait_for_element_clickable(locator)
        element.click()

    def enter_text(self, locator, text):
        """Clear a field and type text into it."""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Return the visible text of an element."""
        return self.wait_for_element(locator).text.strip()

    def is_element_visible(self, locator, timeout=5):
        """Return True if the element is visible, False otherwise."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def open(self, url):
        """Navigate to a URL and wait for the page to load."""
        self.driver.get(url)
        self.wait_for_page_load()

    def get_current_url(self):
        """Return the current browser URL."""
        return self.driver.current_url

    def get_page_title(self):
        """Return the browser tab title."""
        return self.driver.title

    def take_screenshot(self, name):
        """Save a screenshot to the screenshots folder."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name.replace(' ', '_')}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        return filepath

    def is_text_present(self, text):
        """Return True if the text appears anywhere on the page."""
        return text.lower() in self.driver.page_source.lower()

    def get_element_attribute(self, locator, attribute):
        """Return the value of an attribute on an element."""
        return self.wait_for_element(locator).get_attribute(attribute)
