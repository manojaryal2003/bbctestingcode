"""
Parent Attendance Report Page Object Model.

Route: /parent/attendance-report
Accessible by: PARENT only

From AttendanceReport.jsx — shows child's attendance records.
Includes a date-range or monthly filter and a table/list of attendance records.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AttendanceReportPage(BasePage):
    """POM for the Parent Attendance Report page (/parent/attendance-report)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Page heading
    PAGE_HEADING        = (By.CSS_SELECTOR, "h1, h2, [class*='heading'], [class*='title']")

    # Attendance records table or list
    ATTENDANCE_TABLE    = (By.CSS_SELECTOR, "table, [class*='attendance'], [class*='Attendance']")
    TABLE_ROWS          = (By.CSS_SELECTOR, "tbody tr, [class*='row']")

    # Filter inputs (if present)
    DATE_FROM_INPUT     = (By.CSS_SELECTOR, "input[type='date']:first-of-type")
    DATE_TO_INPUT       = (By.CSS_SELECTOR, "input[type='date']:last-of-type")
    FILTER_BTN          = (By.XPATH, "//button[contains(text(),'Filter') or contains(text(),'Search') or contains(text(),'View')]")

    # Present / Absent / Late status indicators
    STATUS_PRESENT      = (By.XPATH, "//*[contains(text(),'Present')]")
    STATUS_ABSENT       = (By.XPATH, "//*[contains(text(),'Absent')]")

    # Loader
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    # Empty state message (when no records found)
    EMPTY_STATE         = (By.XPATH, "//*[contains(text(),'No attendance') or contains(text(),'no record')]")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/parent/attendance-report"

    def open(self):
        """Navigate to the Parent Attendance Report page."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def get_row_count(self) -> int:
        """Return the number of attendance record rows displayed."""
        try:
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            return len(rows)
        except Exception:
            return 0

    def is_on_attendance_report_page(self) -> bool:
        """Return True if current URL is the Attendance Report page."""
        return "/parent/attendance-report" in self.get_current_url()

    def is_attendance_table_visible(self) -> bool:
        """Return True if the attendance table/list container is visible."""
        return self.is_element_visible(self.ATTENDANCE_TABLE)

    def are_present_records_shown(self) -> bool:
        """Return True if at least one 'Present' status indicator is visible."""
        return self.is_element_visible(self.STATUS_PRESENT)
