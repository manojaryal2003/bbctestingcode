"""
Admin Dashboard Page Object Model.

Route: /admin/dashboard
Accessible by: HEAD_ADMIN only

From AdminDashboard.jsx the page shows 4 statistic cards:
  - Total Users
  - Franchises
  - Mentors
  - Students
Plus the sidebar navigation with all admin menu items.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdminDashboardPage(BasePage):
    """POM for the Admin Dashboard page (/admin/dashboard)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Stat cards — identified by their heading text inside each card
    STAT_CARDS          = (By.CSS_SELECTOR, "[class*='card'], [class*='Card']")

    # Sidebar nav links — confirmed from Sidebar.jsx
    NAV_CREATE_USER     = (By.CSS_SELECTOR, "a[href='/admin/create-user']")
    NAV_MANAGE_USERS    = (By.CSS_SELECTOR, "a[href='/admin/manage-users']")
    NAV_STUDENT_DB      = (By.CSS_SELECTOR, "a[href='/admin/student-database']")
    NAV_MANAGE_COURSES  = (By.CSS_SELECTOR, "a[href='/admin/manage-courses']")
    NAV_UPLOAD_WS       = (By.CSS_SELECTOR, "a[href='/admin/upload-worksheet']")
    NAV_VIEW_ACTIVITY   = (By.CSS_SELECTOR, "a[href='/admin/view-activity']")
    NAV_HW_REPORT       = (By.CSS_SELECTOR, "a[href='/admin/homework-report']")
    NAV_STUDENT_PROG    = (By.CSS_SELECTOR, "a[href='/admin/student-progress']")
    NAV_FEE_PACKAGES    = (By.CSS_SELECTOR, "a[href='/admin/fee-management']")
    NAV_BILL_GEN        = (By.CSS_SELECTOR, "a[href='/admin/bill-generation']")
    NAV_FEE_VERIF       = (By.CSS_SELECTOR, "a[href='/admin/fee-verification']")
    NAV_REPORTS         = (By.CSS_SELECTOR, "a[href='/admin/reports']")

    # Dashboard route
    DASHBOARD_URL_FRAGMENT = "/admin/dashboard"

    # Loading state — spinner shown while data loads
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/admin/dashboard"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self):
        """Navigate directly to the admin dashboard."""
        super().open(self.url)
        self.wait_for_dashboard_to_load()

    def wait_for_dashboard_to_load(self):
        """Wait until the loading spinner disappears and stat cards appear."""
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    # ── Stat card helpers ─────────────────────────────────────────────────────

    def get_all_stat_cards(self):
        """Return a list of all visible stat card WebElements."""
        self.wait_for_element(self.STAT_CARDS)
        return self.driver.find_elements(*self.STAT_CARDS)

    def get_stat_card_count(self) -> int:
        """Return the number of stat cards displayed on the dashboard."""
        return len(self.get_all_stat_cards())

    # ── Sidebar navigation helpers ────────────────────────────────────────────

    def click_create_user(self):
        """Click the 'Create User' sidebar link."""
        self.click_element(self.NAV_CREATE_USER)

    def click_manage_users(self):
        """Click the 'Manage Users' sidebar link."""
        self.click_element(self.NAV_MANAGE_USERS)

    def click_student_database(self):
        """Click the 'Student Database' sidebar link."""
        self.click_element(self.NAV_STUDENT_DB)

    def click_fee_packages(self):
        """Click the 'Fee Packages' sidebar link."""
        self.click_element(self.NAV_FEE_PACKAGES)

    def click_bill_generation(self):
        """Click the 'Bill Generation' sidebar link."""
        self.click_element(self.NAV_BILL_GEN)

    def click_reports(self):
        """Click the 'Reports' sidebar link."""
        self.click_element(self.NAV_REPORTS)

    # ── Assertions ────────────────────────────────────────────────────────────

    def is_on_admin_dashboard(self) -> bool:
        """Return True if current URL contains /admin/dashboard."""
        return self.DASHBOARD_URL_FRAGMENT in self.get_current_url()

    def are_stat_cards_visible(self) -> bool:
        """Return True if at least one stat card is visible."""
        return self.is_element_visible(self.STAT_CARDS)

    def is_sidebar_nav_visible(self) -> bool:
        """Return True if the Create User sidebar link is visible."""
        return self.is_element_visible(self.NAV_CREATE_USER)
