from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AttendanceReportPage(BasePage):
    """Page object for the Parent Attendance Report page (/parent/attendance-report)."""

    # Locators
    ATTENDANCE_TABLE = (By.CSS_SELECTOR, "table, [class*='attendance'], [class*='Attendance']")
    TABLE_ROWS       = (By.CSS_SELECTOR, "tbody tr, [class*='row']")
    DATE_FROM_INPUT  = (By.CSS_SELECTOR, "input[type='date']:first-of-type")
    DATE_TO_INPUT    = (By.CSS_SELECTOR, "input[type='date']:last-of-type")
    FILTER_BTN       = (By.XPATH, "//button[contains(text(),'Filter') or contains(text(),'Search') or contains(text(),'View')]")
    STATUS_PRESENT   = (By.XPATH, "//*[contains(text(),'Present')]")
    STATUS_ABSENT    = (By.XPATH, "//*[contains(text(),'Absent')]")
    LOADER           = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/parent/attendance-report"

    def open(self):
        """Go to the Attendance Report page and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def get_row_count(self):
        try:
            return len(self.driver.find_elements(*self.TABLE_ROWS))
        except Exception:
            return 0

    def is_on_attendance_report_page(self):
        return "/parent/attendance-report" in self.get_current_url()

    def is_attendance_table_visible(self):
        return self.is_element_visible(self.ATTENDANCE_TABLE)

    def are_present_records_shown(self):
        return self.is_element_visible(self.STATUS_PRESENT)
