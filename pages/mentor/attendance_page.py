"""
Mentor Attendance Page Object Model.

Route: /mentor/attendance
Accessible by: MENTOR only

From Attendance.jsx the page has TWO tabs:
  Tab 1 — "Mark Attendance":
    - Date picker (input type="date", default today)
    - Student list with Present/Absent toggle per student
    - "Save Attendance" button

  Tab 2 — "Attendance Report":
    - Report type radio: 'all' | 'individual'
    - If individual: student selector dropdown
    - Report mode radio: 'monthly' | 'date'
    - Month/Year selectors OR specific date picker
    - "Generate Report" button
    - Report table rendered below
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class AttendancePage(BasePage):
    """POM for the Mentor Attendance page (/mentor/attendance)."""

    # ── Tab locators ──────────────────────────────────────────────────────────
    TAB_MARK        = (By.XPATH, "//button[contains(text(),'Mark') or contains(text(),'mark')]")
    TAB_REPORT      = (By.XPATH, "//button[contains(text(),'Report') or contains(text(),'report')]")

    # ── Mark Attendance tab ───────────────────────────────────────────────────
    DATE_INPUT      = (By.CSS_SELECTOR, "input[type='date']")
    STUDENT_LIST    = (By.CSS_SELECTOR, "[class*='student'], [class*='Student']")
    SAVE_BTN        = (By.XPATH, "//button[contains(text(),'Save') or contains(text(),'Submit')]")

    # Present/Absent toggle buttons inside student rows
    PRESENT_BTNS    = (By.XPATH, "//button[contains(text(),'Present')]")
    ABSENT_BTNS     = (By.XPATH, "//button[contains(text(),'Absent')]")

    # ── Report tab ────────────────────────────────────────────────────────────
    RADIO_ALL       = (By.CSS_SELECTOR, "input[value='all']")
    RADIO_INDIV     = (By.CSS_SELECTOR, "input[value='individual']")
    STUDENT_SELECT  = (By.CSS_SELECTOR, "select[class*='student'], select")
    RADIO_MONTHLY   = (By.CSS_SELECTOR, "input[value='monthly']")
    RADIO_DATE      = (By.CSS_SELECTOR, "input[value='date']")
    MONTH_SELECT    = (By.CSS_SELECTOR, "select[class*='month']")
    YEAR_SELECT     = (By.CSS_SELECTOR, "select[class*='year']")
    GENERATE_BTN    = (By.XPATH, "//button[contains(text(),'Generate') or contains(text(),'View')]")

    # Report table
    REPORT_TABLE    = (By.CSS_SELECTOR, "table, [class*='report']")

    # Notifications
    SUCCESS_MSG     = (By.CSS_SELECTOR, "[class*='success'], [class*='Success'], [class*='toast']")
    ERROR_MSG       = (By.CSS_SELECTOR, "[class*='error'], [class*='Error']")

    # Loader
    LOADER          = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/mentor/attendance"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self):
        """Navigate to the Mentor Attendance page."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    # ── Tab navigation ────────────────────────────────────────────────────────

    def click_mark_tab(self):
        """Switch to the Mark Attendance tab."""
        self.click_element(self.TAB_MARK)

    def click_report_tab(self):
        """Switch to the Attendance Report tab."""
        self.click_element(self.TAB_REPORT)

    # ── Mark Attendance actions ───────────────────────────────────────────────

    def set_date(self, date_str: str):
        """
        Set the attendance date.

        Args:
            date_str: date in YYYY-MM-DD format
        """
        self.enter_text(self.DATE_INPUT, date_str)

    def click_save_attendance(self):
        """Click the Save Attendance button."""
        self.click_element(self.SAVE_BTN)

    # ── Report tab actions ────────────────────────────────────────────────────

    def select_all_students_report(self):
        """Select the 'all students' radio button."""
        self.click_element(self.RADIO_ALL)

    def select_individual_report(self):
        """Select the 'individual' radio button."""
        self.click_element(self.RADIO_INDIV)

    def select_monthly_mode(self):
        """Select the monthly report mode."""
        self.click_element(self.RADIO_MONTHLY)

    def click_generate_report(self):
        """Click the Generate Report button."""
        self.click_element(self.GENERATE_BTN)

    # ── Assertions ────────────────────────────────────────────────────────────

    def is_on_attendance_page(self) -> bool:
        """Return True if current URL is the Attendance page."""
        return "/mentor/attendance" in self.get_current_url()

    def is_mark_tab_visible(self) -> bool:
        """Return True if the Mark Attendance tab button is visible."""
        return self.is_element_visible(self.TAB_MARK)

    def is_report_tab_visible(self) -> bool:
        """Return True if the Attendance Report tab button is visible."""
        return self.is_element_visible(self.TAB_REPORT)

    def is_success_message_visible(self) -> bool:
        """Return True if a success/toast message is displayed."""
        return self.is_element_visible(self.SUCCESS_MSG)

    def is_date_input_visible(self) -> bool:
        """Return True if the date picker is visible on the Mark tab."""
        return self.is_element_visible(self.DATE_INPUT)
