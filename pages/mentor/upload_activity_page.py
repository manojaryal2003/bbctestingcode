"""
Mentor Upload Activity Page Object Model.

Route: /mentor/upload-activity
Accessible by: MENTOR only

From UploadActivity.jsx the form has:
  - title input (name="title")
  - description textarea (name="description")
  - fileCategory select (name="fileCategory", default "ACTIVITY")
  - visibility checkboxes:
      visibleToParents  (name="visibleToParents",  default checked)
      visibleToAdmins   (name="visibleToAdmins",   default unchecked)
      visibleToFranchise(name="visibleToFranchise",default unchecked)
      visibleToStudents (name="visibleToStudents",  default checked)
  - file input (type="file")
  - Submit button

Below the form: list of previously uploaded activities.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class UploadActivityPage(BasePage):
    """POM for the Mentor Upload Activity page (/mentor/upload-activity)."""

    # ── Form locators ─────────────────────────────────────────────────────────
    TITLE_INPUT         = (By.NAME, "title")
    DESCRIPTION_INPUT   = (By.NAME, "description")
    FILE_CATEGORY_SELECT= (By.NAME, "fileCategory")
    FILE_INPUT          = (By.CSS_SELECTOR, "input[type='file']")

    # Visibility checkboxes
    CB_PARENTS          = (By.NAME, "visibleToParents")
    CB_ADMINS           = (By.NAME, "visibleToAdmins")
    CB_FRANCHISE        = (By.NAME, "visibleToFranchise")
    CB_STUDENTS         = (By.NAME, "visibleToStudents")

    # Submit
    SUBMIT_BTN          = (By.CSS_SELECTOR, "button[type='submit']")

    # Uploaded activity list items
    ACTIVITY_LIST_ITEMS = (By.CSS_SELECTOR, "[class*='activity'], [class*='Activity']")

    # Error / success feedback
    ERROR_MSG           = (By.CSS_SELECTOR, "[class*='error'], [class*='Error']")
    SUCCESS_MSG         = (By.CSS_SELECTOR, "[class*='success'], [class*='toast'], [class*='Toast']")

    # Loader
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/mentor/upload-activity"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self):
        """Navigate to the Upload Activity page."""
        super().open(self.url)
        self.wait_for_element(self.TITLE_INPUT)

    # ── Actions ───────────────────────────────────────────────────────────────

    def enter_title(self, title: str):
        """Type into the Title field."""
        self.enter_text(self.TITLE_INPUT, title)

    def enter_description(self, description: str):
        """Type into the Description field."""
        self.enter_text(self.DESCRIPTION_INPUT, description)

    def click_submit(self):
        """Click the Upload/Submit button."""
        self.click_element(self.SUBMIT_BTN)

    def submit_without_file(self, title: str, description: str):
        """Fill title + description then submit without attaching a file."""
        self.enter_title(title)
        self.enter_description(description)
        self.click_submit()

    # ── Assertions ────────────────────────────────────────────────────────────

    def is_on_upload_activity_page(self) -> bool:
        """Return True if current URL is the Upload Activity page."""
        return "/mentor/upload-activity" in self.get_current_url()

    def is_form_visible(self) -> bool:
        """Return True if the title input is rendered."""
        return self.is_element_visible(self.TITLE_INPUT)

    def is_error_visible(self) -> bool:
        """Return True if an error message is displayed."""
        return self.is_element_visible(self.ERROR_MSG)

    def get_error_text(self) -> str:
        """Return the error message text."""
        return self.get_text(self.ERROR_MSG)

    def is_success_visible(self) -> bool:
        """Return True if a success message is displayed."""
        return self.is_element_visible(self.SUCCESS_MSG)

    def is_file_input_present(self) -> bool:
        """Return True if the file upload input is present."""
        return self.is_element_visible(self.FILE_INPUT)
