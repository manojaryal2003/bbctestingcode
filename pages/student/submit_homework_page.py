"""
Student Submit Homework Page Object Model.

Route: /student/submit-homework
Accessible by: STUDENT only

From SubmitHomework.jsx:
  - List of pending homework assignments (clickable to open submission modal)
  - Submission modal contains:
      - file input (type="file") — REQUIRED
      - submissionText textarea (name or placeholder-based)
      - Submit button
      - Close/Cancel button
  - Error shown if:
      - no homework selected
      - already submitted
      - no file attached
  - Alert on success
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SubmitHomeworkPage(BasePage):
    """POM for the Student Submit Homework page (/student/submit-homework)."""

    # ── Homework list ─────────────────────────────────────────────────────────
    HW_LIST_ITEMS   = (By.CSS_SELECTOR, "[class*='homework'], [class*='Homework']")
    # First homework item in the list (click to open submission modal)
    FIRST_HW_ITEM   = (By.CSS_SELECTOR, "[class*='homework']:first-of-type, [class*='Homework']:first-of-type")

    # ── Submission modal ──────────────────────────────────────────────────────
    MODAL               = (By.CSS_SELECTOR, "[class*='modal'], [class*='Modal']")
    FILE_INPUT          = (By.CSS_SELECTOR, "input[type='file']")
    SUBMISSION_TEXT     = (By.CSS_SELECTOR, "textarea, input[placeholder*='text' i], input[placeholder*='comment' i]")
    SUBMIT_BTN          = (By.CSS_SELECTOR, "button[type='submit']")
    CLOSE_BTN           = (By.XPATH, "//button[contains(text(),'Close') or contains(text(),'Cancel') or contains(@aria-label,'close')]")

    # Error / Success
    ERROR_MSG       = (By.CSS_SELECTOR, "[class*='error'], [class*='Error']")

    # Loader
    LOADER          = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/student/submit-homework"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self):
        """Navigate to the Submit Homework page."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    # ── Actions ───────────────────────────────────────────────────────────────

    def click_first_homework(self):
        """Click the first homework item in the list to open the submission modal."""
        self.click_element(self.FIRST_HW_ITEM)
        self.wait_for_element(self.MODAL)

    def close_modal(self):
        """Close the submission modal."""
        self.click_element(self.CLOSE_BTN)

    def click_submit(self):
        """Click the Submit button inside the modal (without attaching file)."""
        self.click_element(self.SUBMIT_BTN)

    # ── Assertions ────────────────────────────────────────────────────────────

    def is_on_submit_homework_page(self) -> bool:
        """Return True if current URL is the Submit Homework page."""
        return "/student/submit-homework" in self.get_current_url()

    def is_homework_list_visible(self) -> bool:
        """Return True if any homework item is displayed."""
        return self.is_element_visible(self.HW_LIST_ITEMS)

    def is_modal_visible(self) -> bool:
        """Return True if the submission modal is open."""
        return self.is_element_visible(self.MODAL)

    def is_error_visible(self) -> bool:
        """Return True if an error message is displayed."""
        return self.is_element_visible(self.ERROR_MSG)

    def get_error_text(self) -> str:
        """Return the error message text."""
        return self.get_text(self.ERROR_MSG)

    def is_file_input_visible(self) -> bool:
        """Return True if the file input is visible inside the modal."""
        return self.is_element_visible(self.FILE_INPUT)
