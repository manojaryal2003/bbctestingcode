from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AttendanceMonitorPage(BasePage):
    """Page object for the Franchise Attendance Monitor page (/franchise/attendance)."""

    # Locators
    DATE_INPUT       = (By.CSS_SELECTOR, "input[type='date']")
    ATTENDANCE_TABLE = (By.CSS_SELECTOR, "table, [class*='attendance'], [class*='Attendance']")
    TABLE_ROWS       = (By.CSS_SELECTOR, "tbody tr, [class*='row']")
    FILTER_BTN       = (By.XPATH, "//button[contains(text(),'Filter') or contains(text(),'View') or contains(text(),'Search')]")
    LOADER           = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/franchise/attendance"

    def open(self):
        """Go to the Attendance Monitor page and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def get_row_count(self):
        try:
            return len(self.driver.find_elements(*self.TABLE_ROWS))
        except Exception:
            return 0

    def is_on_attendance_monitor_page(self):
        return "/franchise/attendance" in self.get_current_url()

    def is_attendance_table_visible(self):
        return self.is_element_visible(self.ATTENDANCE_TABLE)

    def is_date_input_visible(self):
        return self.is_element_visible(self.DATE_INPUT)
