"""
Parent Dashboard Page Object Model.

Route: /parent/dashboard
Accessible by: PARENT only

From ParentDashboard.jsx — shows 8 navigation tiles:
  Attendance, Homework, Fee Status, Activities,
  Messages, Progress, View Files, Tracking

Plus a 7-day attendance strip and quick stats.
Sidebar confirmed from Sidebar.jsx PARENT section.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ParentDashboardPage(BasePage):
    """POM for the Parent Dashboard page (/parent/dashboard)."""

    # ── Nav tiles (confirmed from ParentDashboard.jsx NAV_TILES) ─────────────
    TILE_ATTENDANCE = (By.CSS_SELECTOR, "a[href='/parent/attendance-report'], [data-path='/parent/attendance-report']")
    TILE_HOMEWORK   = (By.CSS_SELECTOR, "a[href='/parent/homework'], [data-path='/parent/homework']")
    TILE_FEE_STATUS = (By.CSS_SELECTOR, "a[href='/parent/fee-status'], [data-path='/parent/fee-status']")
    TILE_MESSAGES   = (By.CSS_SELECTOR, "a[href='/parent/messages'], [data-path='/parent/messages']")
    TILE_PROGRESS   = (By.CSS_SELECTOR, "a[href='/parent/progress-report'], [data-path='/parent/progress-report']")

    # Sidebar links (confirmed from Sidebar.jsx PARENT section)
    NAV_HOMEWORK        = (By.CSS_SELECTOR, "a[href='/parent/homework']")
    NAV_ATTENDANCE      = (By.CSS_SELECTOR, "a[href='/parent/attendance-report']")
    NAV_VIEW_ACTIVITY   = (By.CSS_SELECTOR, "a[href='/parent/view-activity']")
    NAV_PROGRESS_REPORT = (By.CSS_SELECTOR, "a[href='/parent/progress-report']")
    NAV_MESSAGES        = (By.CSS_SELECTOR, "a[href='/parent/messages']")
    NAV_FEE_STATUS      = (By.CSS_SELECTOR, "a[href='/parent/fee-status']")

    # 7-day attendance strip and today status
    ATTENDANCE_STRIP    = (By.CSS_SELECTOR, "[class*='attendance'], [class*='Attendance']")

    # Dashboard content
    DASHBOARD_CONTENT   = (By.CSS_SELECTOR, "main, [class*='dashboard'], [class*='Dashboard']")

    # Loader
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/parent/dashboard"

    def open(self):
        """Navigate directly to the Parent Dashboard."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_parent_dashboard(self) -> bool:
        """Return True if current URL is the Parent Dashboard."""
        return "/parent/dashboard" in self.get_current_url()

    def is_sidebar_visible(self) -> bool:
        """Return True if the sidebar Fee Status link is visible."""
        return self.is_element_visible(self.NAV_FEE_STATUS)

    def click_attendance_from_sidebar(self):
        """Click the Attendance sidebar link."""
        self.click_element(self.NAV_ATTENDANCE)

    def click_fee_status_from_sidebar(self):
        """Click the Fee Status sidebar link."""
        self.click_element(self.NAV_FEE_STATUS)

    def click_homework_from_sidebar(self):
        """Click the Homework sidebar link."""
        self.click_element(self.NAV_HOMEWORK)

    def click_progress_report(self):
        """Click the Progress Report sidebar link."""
        self.click_element(self.NAV_PROGRESS_REPORT)

    def is_dashboard_content_visible(self) -> bool:
        """Return True if any nav tile or main content area is rendered."""
        return self.is_element_visible(self.DASHBOARD_CONTENT)
