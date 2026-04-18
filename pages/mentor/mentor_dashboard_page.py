"""
Mentor Dashboard Page Object Model.

Route: /mentor/dashboard
Accessible by: MENTOR only

From MentorDashboard.jsx the page shows the mentor's class overview.
Sidebar confirmed from Sidebar.jsx for MENTOR role:
  - Dashboard, Attendance, Upload Activity, View Activity,
    Homework Management, Student Evaluation
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MentorDashboardPage(BasePage):
    """POM for the Mentor Dashboard page (/mentor/dashboard)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Sidebar nav links (confirmed from Sidebar.jsx MENTOR section)
    NAV_ATTENDANCE      = (By.CSS_SELECTOR, "a[href='/mentor/attendance']")
    NAV_UPLOAD_ACTIVITY = (By.CSS_SELECTOR, "a[href='/mentor/upload-activity']")
    NAV_VIEW_ACTIVITY   = (By.CSS_SELECTOR, "a[href='/mentor/view-activity']")
    NAV_HOMEWORK_MGMT   = (By.CSS_SELECTOR, "a[href='/mentor/homework-management']")
    NAV_EVALUATION      = (By.CSS_SELECTOR, "a[href='/mentor/evaluation']")

    # Dashboard content — stat cards or welcome text
    DASHBOARD_CONTENT   = (By.CSS_SELECTOR, "[class*='dashboard'], [class*='Dashboard'], main")

    # Loading state
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/mentor/dashboard"

    def open(self):
        """Navigate directly to the Mentor Dashboard."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_mentor_dashboard(self) -> bool:
        """Return True if the current URL is the Mentor Dashboard."""
        return "/mentor/dashboard" in self.get_current_url()

    def is_sidebar_visible(self) -> bool:
        """Return True if the Attendance sidebar link is visible."""
        return self.is_element_visible(self.NAV_ATTENDANCE)

    def click_attendance(self):
        """Click the Attendance sidebar link."""
        self.click_element(self.NAV_ATTENDANCE)

    def click_upload_activity(self):
        """Click the Upload Activity sidebar link."""
        self.click_element(self.NAV_UPLOAD_ACTIVITY)

    def click_homework_management(self):
        """Click the Homework Management sidebar link."""
        self.click_element(self.NAV_HOMEWORK_MGMT)

    def click_evaluation(self):
        """Click the Student Evaluation sidebar link."""
        self.click_element(self.NAV_EVALUATION)
