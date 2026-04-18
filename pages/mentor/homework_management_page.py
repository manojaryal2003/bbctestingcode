"""
Mentor Homework Management Page Object Model.

Route: /mentor/homework-management  (maps to HomeworkManagement.jsx)
Also covers: /mentor/send-homework  (maps to SendHomework.jsx)
Accessible by: MENTOR only

From SendHomework.jsx the send-homework form has:
  - title input (name="title")
  - description textarea (name="description")
  - dueDate input (name="dueDate", type="date" or "datetime-local")
  - file input (type="file") — optional
  - Submit button

Below form: list of previously sent homework items.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomeworkManagementPage(BasePage):
    """POM for the Mentor Homework Management / Send Homework pages."""

    # ── Send Homework form locators ───────────────────────────────────────────
    TITLE_INPUT     = (By.NAME, "title")
    DESC_INPUT      = (By.NAME, "description")
    DUE_DATE_INPUT  = (By.NAME, "dueDate")
    FILE_INPUT      = (By.CSS_SELECTOR, "input[type='file']")
    SUBMIT_BTN      = (By.CSS_SELECTOR, "button[type='submit']")

    # Homework list
    HW_LIST_ITEMS   = (By.CSS_SELECTOR, "[class*='homework'], [class*='Homework']")

    # Feedback
    ERROR_MSG       = (By.CSS_SELECTOR, "[class*='error'], [class*='Error']")
    SUCCESS_ALERT   = (By.CSS_SELECTOR, "[class*='success'], [class*='toast'], [class*='Toast']")

    # Loader
    LOADER          = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.send_hw_url = f"{base_url}/mentor/send-homework"
        self.hw_mgmt_url = f"{base_url}/mentor/homework-management"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open_send_homework(self):
        """Navigate to the Send Homework page."""
        super().open(self.send_hw_url)
        self.wait_for_element(self.TITLE_INPUT)

    def open_homework_management(self):
        """Navigate to the Homework Management page."""
        super().open(self.hw_mgmt_url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    # ── Form actions ──────────────────────────────────────────────────────────

    def enter_title(self, title: str):
        """Enter the homework title."""
        self.enter_text(self.TITLE_INPUT, title)

    def enter_description(self, description: str):
        """Enter the homework description."""
        self.enter_text(self.DESC_INPUT, description)

    def enter_due_date(self, date_str: str):
        """
        Enter the due date.

        Args:
            date_str: date in YYYY-MM-DD format
        """
        self.enter_text(self.DUE_DATE_INPUT, date_str)

    def click_submit(self):
        """Click the Send Homework submit button."""
        self.click_element(self.SUBMIT_BTN)

    def send_homework(self, title: str, description: str, due_date: str = ""):
        """
        Complete full Send Homework flow.

        Steps:
            1. Enter title
            2. Enter description
            3. Optionally enter due date
            4. Click submit
        """
        self.enter_title(title)
        self.enter_description(description)
        if due_date:
            self.enter_due_date(due_date)
        self.click_submit()

    # ── Assertions ────────────────────────────────────────────────────────────

    def is_form_visible(self) -> bool:
        """Return True if the send homework form title input is visible."""
        return self.is_element_visible(self.TITLE_INPUT)

    def is_error_visible(self) -> bool:
        """Return True if an error message is shown."""
        return self.is_element_visible(self.ERROR_MSG)

    def get_error_text(self) -> str:
        """Return the error message text."""
        return self.get_text(self.ERROR_MSG)

    def is_on_send_homework_page(self) -> bool:
        """Return True if current URL is the Send Homework page."""
        return "/mentor/send-homework" in self.get_current_url()

    def is_on_homework_management_page(self) -> bool:
        """Return True if current URL is the Homework Management page."""
        return "/mentor/homework-management" in self.get_current_url()
