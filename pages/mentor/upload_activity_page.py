from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class UploadActivityPage(BasePage):
    """Page object for the Mentor Upload Activity page (/mentor/upload-activity)."""

    # Locators
    TITLE_INPUT          = (By.NAME, "title")
    DESCRIPTION_INPUT    = (By.NAME, "description")
    FILE_CATEGORY_SELECT = (By.NAME, "fileCategory")
    FILE_INPUT           = (By.CSS_SELECTOR, "input[type='file']")
    CB_PARENTS           = (By.NAME, "visibleToParents")
    CB_ADMINS            = (By.NAME, "visibleToAdmins")
    CB_STUDENTS          = (By.NAME, "visibleToStudents")
    SUBMIT_BTN           = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG            = (By.CSS_SELECTOR, "[class*='error'], [class*='Error']")
    SUCCESS_MSG          = (By.CSS_SELECTOR, "[class*='success'], [class*='toast'], [class*='Toast']")
    LOADER               = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/mentor/upload-activity"

    def open(self):
        """Go to the Upload Activity page."""
        super().open(self.url)
        self.wait_for_element(self.TITLE_INPUT)

    def enter_title(self, title):
        self.enter_text(self.TITLE_INPUT, title)

    def enter_description(self, description):
        self.enter_text(self.DESCRIPTION_INPUT, description)

    def click_submit(self):
        self.click_element(self.SUBMIT_BTN)

    def is_on_upload_activity_page(self):
        return "/mentor/upload-activity" in self.get_current_url()

    def is_form_visible(self):
        return self.is_element_visible(self.TITLE_INPUT)

    def is_file_input_present(self):
        return self.is_element_visible(self.FILE_INPUT)

    def is_error_visible(self):
        return self.is_element_visible(self.ERROR_MSG)

    def get_error_text(self):
        return self.get_text(self.ERROR_MSG)

    def is_success_visible(self):
        return self.is_element_visible(self.SUCCESS_MSG)
