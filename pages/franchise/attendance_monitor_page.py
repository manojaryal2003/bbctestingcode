"""
Franchise Attendance Monitor Page Object Model.

Route: /franchise/attendance
Accessible by: FRANCHISE_ADMIN only

From AttendanceMonitor.jsx — shows the franchise's student attendance records.
Franchise admin can view attendance by date, filter by mentor, see summaries.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AttendanceMonitorPage(BasePage):
    """POM for the Franchise Attendance Monitor page (/franchise/attendance)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    PAGE_HEADING        = (By.CSS_SELECTOR, "h1, h2, [class*='heading'], [class*='title']")

    # Date filter
    DATE_INPUT          = (By.CSS_SELECTOR, "input[type='date']")

    # Mentor filter dropdown (if present)
    MENTOR_SELECT       = (By.CSS_SELECTOR, "select[class*='mentor'], select")

    # Attendance records
    ATTENDANCE_TABLE    = (By.CSS_SELECTOR, "table, [class*='attendance'], [class*='Attendance']")
    TABLE_ROWS          = (By.CSS_SELECTOR, "tbody tr, [class*='row']")

    # Summary stats (present/absent counts)
    PRESENT_COUNT       = (By.XPATH, "//*[contains(text(),'Present')]")
    ABSENT_COUNT        = (By.XPATH, "//*[contains(text(),'Absent')]")

    # Filter / View button
    FILTER_BTN          = (By.XPATH, "//button[contains(text(),'Filter') or contains(text(),'View') or contains(text(),'Search')]")

    # Loader
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    # Empty state
    EMPTY_STATE         = (By.XPATH, "//*[contains(text(),'No attendance') or contains(text(),'No records') or contains(text(),'no data')]")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/franchise/attendance"

    def open(self):
        """Navigate to the Franchise Attendance Monitor page."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def get_row_count(self) -> int:
        """Return the number of attendance rows visible."""
        try:
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            return len(rows)
        except Exception:
            return 0

    def is_on_attendance_monitor_page(self) -> bool:
        """Return True if current URL is the Attendance Monitor page."""
        return "/franchise/attendance" in self.get_current_url()

    def is_attendance_table_visible(self) -> bool:
        """Return True if the attendance table or list is visible."""
        return self.is_element_visible(self.ATTENDANCE_TABLE)

    def is_date_input_visible(self) -> bool:
        """Return True if the date filter input is visible."""
        return self.is_element_visible(self.DATE_INPUT)
