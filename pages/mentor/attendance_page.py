from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AttendancePage(BasePage):
    """Page object for the Mentor Attendance page (/mentor/attendance)."""

    # Locators
    TAB_MARK     = (By.XPATH, "//button[contains(text(),'Mark') or contains(text(),'mark')]")
    TAB_REPORT   = (By.XPATH, "//button[contains(text(),'Report') or contains(text(),'report')]")
    DATE_INPUT   = (By.CSS_SELECTOR, "input[type='date']")
    SAVE_BTN     = (By.XPATH, "//button[contains(text(),'Save') or contains(text(),'Submit')]")
    GENERATE_BTN = (By.XPATH, "//button[contains(text(),'Generate') or contains(text(),'View')]")
    REPORT_TABLE = (By.CSS_SELECTOR, "table, [class*='report']")
    SUCCESS_MSG  = (By.CSS_SELECTOR, "[class*='success'], [class*='Success'], [class*='toast']")
    LOADER       = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/mentor/attendance"

    def open(self):
        """Go to the Attendance page and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def click_mark_tab(self):
        self.click_element(self.TAB_MARK)

    def click_report_tab(self):
        self.click_element(self.TAB_REPORT)

    def set_date(self, date_str):
        """Set the attendance date (format: YYYY-MM-DD)."""
        self.enter_text(self.DATE_INPUT, date_str)

    def click_save_attendance(self):
        self.click_element(self.SAVE_BTN)

    def click_generate_report(self):
        self.click_element(self.GENERATE_BTN)

    def is_on_attendance_page(self):
        return "/mentor/attendance" in self.get_current_url()

    def is_mark_tab_visible(self):
        return self.is_element_visible(self.TAB_MARK)

    def is_report_tab_visible(self):
        return self.is_element_visible(self.TAB_REPORT)

    def is_date_input_visible(self):
        return self.is_element_visible(self.DATE_INPUT)

    def is_success_message_visible(self):
        return self.is_element_visible(self.SUCCESS_MSG)
