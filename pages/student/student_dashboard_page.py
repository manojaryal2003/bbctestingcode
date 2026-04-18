"""
Student Dashboard Page Object Model.

Route: /student/dashboard
Accessible by: STUDENT only

From StudentDashboard.jsx and Sidebar.jsx (STUDENT section):
  Sidebar links: Dashboard, Upload Activity, Activities (view),
                 Submit Homework, My Tracking, My Progress, Badges
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class StudentDashboardPage(BasePage):
    """POM for the Student Dashboard page (/student/dashboard)."""

    # ── Sidebar nav locators ──────────────────────────────────────────────────
    NAV_UPLOAD_ACTIVITY = (By.CSS_SELECTOR, "a[href='/student/upload-activity']")
    NAV_VIEW_ACTIVITY   = (By.CSS_SELECTOR, "a[href='/student/view-activity']")
    NAV_SUBMIT_HW       = (By.CSS_SELECTOR, "a[href='/student/submit-homework']")
    NAV_TRACKING        = (By.CSS_SELECTOR, "a[href='/student/tracking']")
    NAV_PROGRESS        = (By.CSS_SELECTOR, "a[href='/student/progress']")
    NAV_BADGES          = (By.CSS_SELECTOR, "a[href='/student/badges']")

    # Dashboard content area
    DASHBOARD_CONTENT   = (By.CSS_SELECTOR, "main, [class*='dashboard'], [class*='Dashboard']")

    # Loader
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/student/dashboard"

    def open(self):
        """Navigate directly to the Student Dashboard."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_student_dashboard(self) -> bool:
        """Return True if current URL is the Student Dashboard."""
        return "/student/dashboard" in self.get_current_url()

    def is_sidebar_visible(self) -> bool:
        """Return True if the Submit Homework sidebar link is visible."""
        return self.is_element_visible(self.NAV_SUBMIT_HW)

    def click_submit_homework(self):
        """Click the Submit Homework sidebar link."""
        self.click_element(self.NAV_SUBMIT_HW)

    def click_upload_activity(self):
        """Click the Upload Activity sidebar link."""
        self.click_element(self.NAV_UPLOAD_ACTIVITY)

    def click_badges(self):
        """Click the Badges sidebar link."""
        self.click_element(self.NAV_BADGES)

    def click_progress(self):
        """Click the My Progress sidebar link."""
        self.click_element(self.NAV_PROGRESS)
