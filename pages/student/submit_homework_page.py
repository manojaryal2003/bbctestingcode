from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SubmitHomeworkPage(BasePage):
    """Page object for the Student Submit Homework page (/student/submit-homework)."""

    # Locators
    HW_LIST_ITEMS = (By.CSS_SELECTOR, "[class*='homework'], [class*='Homework']")
    FIRST_HW_ITEM = (By.CSS_SELECTOR, "[class*='homework']:first-of-type, [class*='Homework']:first-of-type")
    MODAL         = (By.CSS_SELECTOR, "[class*='modal'], [class*='Modal']")
    FILE_INPUT    = (By.CSS_SELECTOR, "input[type='file']")
    SUBMIT_BTN    = (By.CSS_SELECTOR, "button[type='submit']")
    CLOSE_BTN     = (By.XPATH, "//button[contains(text(),'Close') or contains(text(),'Cancel') or contains(@aria-label,'close')]")
    ERROR_MSG     = (By.CSS_SELECTOR, "[class*='error'], [class*='Error']")
    LOADER        = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/student/submit-homework"

    def open(self):
        """Go to the Submit Homework page and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def click_first_homework(self):
        """Click the first homework item to open the submission modal."""
        self.click_element(self.FIRST_HW_ITEM)
        self.wait_for_element(self.MODAL)

    def close_modal(self):
        self.click_element(self.CLOSE_BTN)

    def click_submit(self):
        self.click_element(self.SUBMIT_BTN)

    def is_on_submit_homework_page(self):
        return "/student/submit-homework" in self.get_current_url()

    def is_homework_list_visible(self):
        return self.is_element_visible(self.HW_LIST_ITEMS)

    def is_modal_visible(self):
        return self.is_element_visible(self.MODAL)

    def is_file_input_visible(self):
        return self.is_element_visible(self.FILE_INPUT)

    def is_error_visible(self):
        return self.is_element_visible(self.ERROR_MSG)

    def get_error_text(self):
        return self.get_text(self.ERROR_MSG)
