"""
Student Upload Activity Page Object Model.

Route: /student/upload-activity
Accessible by: STUDENT only

From student/UploadActivity.jsx — students upload their own activity files.
Form fields confirmed (structurally similar to mentor upload):
  - title input
  - description textarea
  - file input (type="file")
  - Submit button
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class StudentUploadActivityPage(BasePage):
    """POM for the Student Upload Activity page (/student/upload-activity)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    TITLE_INPUT     = (By.NAME, "title")
    DESC_INPUT      = (By.NAME, "description")
    FILE_INPUT      = (By.CSS_SELECTOR, "input[type='file']")
    SUBMIT_BTN      = (By.CSS_SELECTOR, "button[type='submit']")

    # Feedback
    ERROR_MSG       = (By.CSS_SELECTOR, "[class*='error'], [class*='Error']")
    SUCCESS_MSG     = (By.CSS_SELECTOR, "[class*='success'], [class*='toast'], [class*='Toast']")

    # Activity list
    ACTIVITY_LIST   = (By.CSS_SELECTOR, "[class*='activity'], [class*='Activity']")

    # Loader
    LOADER          = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/student/upload-activity"

    def open(self):
        """Navigate to the Student Upload Activity page."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def enter_title(self, title: str):
        """Type into the Title field."""
        self.enter_text(self.TITLE_INPUT, title)

    def enter_description(self, desc: str):
        """Type into the Description field."""
        self.enter_text(self.DESC_INPUT, desc)

    def click_submit(self):
        """Click the submit button."""
        self.click_element(self.SUBMIT_BTN)

    def is_on_upload_activity_page(self) -> bool:
        """Return True if current URL is the Student Upload Activity page."""
        return "/student/upload-activity" in self.get_current_url()

    def is_form_visible(self) -> bool:
        """Return True if the title input is rendered."""
        return self.is_element_visible(self.TITLE_INPUT)

    def is_error_visible(self) -> bool:
        """Return True if an error message is shown."""
        return self.is_element_visible(self.ERROR_MSG)

    def get_error_text(self) -> str:
        """Return error message text."""
        return self.get_text(self.ERROR_MSG)
