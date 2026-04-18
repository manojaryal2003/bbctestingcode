from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomeworkManagementPage(BasePage):
    """Page object for Mentor Homework Management and Send Homework pages."""

    # Locators
    TITLE_INPUT    = (By.NAME, "title")
    DESC_INPUT     = (By.NAME, "description")
    DUE_DATE_INPUT = (By.NAME, "dueDate")
    FILE_INPUT     = (By.CSS_SELECTOR, "input[type='file']")
    SUBMIT_BTN     = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG      = (By.CSS_SELECTOR, "[class*='error'], [class*='Error']")
    SUCCESS_ALERT  = (By.CSS_SELECTOR, "[class*='success'], [class*='toast'], [class*='Toast']")
    LOADER         = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.send_hw_url = f"{base_url}/mentor/send-homework"
        self.hw_mgmt_url = f"{base_url}/mentor/homework-management"

    def open_send_homework(self):
        """Go to the Send Homework page."""
        super().open(self.send_hw_url)
        self.wait_for_element(self.TITLE_INPUT)

    def open_homework_management(self):
        """Go to the Homework Management page."""
        super().open(self.hw_mgmt_url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def enter_title(self, title):
        self.enter_text(self.TITLE_INPUT, title)

    def enter_description(self, description):
        self.enter_text(self.DESC_INPUT, description)

    def enter_due_date(self, date_str):
        """Enter a due date (format: YYYY-MM-DD)."""
        self.enter_text(self.DUE_DATE_INPUT, date_str)

    def click_submit(self):
        self.click_element(self.SUBMIT_BTN)

    def send_homework(self, title, description, due_date=""):
        """Fill in the form and submit homework."""
        self.enter_title(title)
        self.enter_description(description)
        if due_date:
            self.enter_due_date(due_date)
        self.click_submit()

    def is_form_visible(self):
        return self.is_element_visible(self.TITLE_INPUT)

    def is_error_visible(self):
        return self.is_element_visible(self.ERROR_MSG)

    def get_error_text(self):
        return self.get_text(self.ERROR_MSG)

    def is_on_send_homework_page(self):
        return "/mentor/send-homework" in self.get_current_url()

    def is_on_homework_management_page(self):
        return "/mentor/homework-management" in self.get_current_url()
