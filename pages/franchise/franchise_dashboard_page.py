"""
Franchise Dashboard Page Object Model.

Route: /franchise/dashboard
Accessible by: FRANCHISE_ADMIN only

From FranchiseDashboard.jsx — shows 3 stat cards:
  Total Students, Total Mentors, Attendance Rate (today %)

Sidebar confirmed from Sidebar.jsx FRANCHISE_ADMIN section:
  Dashboard, Attendance Monitor, Parent Messages, View Activity,
  Evaluation Report, Homework Report, Payment Proofs, Financial Reports
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FranchiseDashboardPage(BasePage):
    """POM for the Franchise Admin Dashboard page (/franchise/dashboard)."""

    # ── Stat cards ────────────────────────────────────────────────────────────
    STAT_CARDS          = (By.CSS_SELECTOR, "[class*='card'], [class*='Card']")

    # ── Sidebar links (confirmed from Sidebar.jsx) ────────────────────────────
    NAV_ATTENDANCE      = (By.CSS_SELECTOR, "a[href='/franchise/attendance']")
    NAV_MESSAGES        = (By.CSS_SELECTOR, "a[href='/franchise/messages']")
    NAV_VIEW_ACTIVITY   = (By.CSS_SELECTOR, "a[href='/franchise/view-activity']")
    NAV_EVAL_REPORT     = (By.CSS_SELECTOR, "a[href='/franchise/evaluation-report']")
    NAV_HW_REPORT       = (By.CSS_SELECTOR, "a[href='/franchise/homework-report']")
    NAV_PAYMENT_PROOF   = (By.CSS_SELECTOR, "a[href='/franchise/payment-proof']")
    NAV_FIN_REPORTS     = (By.CSS_SELECTOR, "a[href='/franchise/reports']")

    # Loader
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/franchise/dashboard"

    def open(self):
        """Navigate directly to the Franchise Dashboard."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_franchise_dashboard(self) -> bool:
        """Return True if current URL is the Franchise Dashboard."""
        return "/franchise/dashboard" in self.get_current_url()

    def are_stat_cards_visible(self) -> bool:
        """Return True if at least one stat card is visible."""
        return self.is_element_visible(self.STAT_CARDS)

    def get_stat_card_count(self) -> int:
        """Return the number of stat cards on the dashboard."""
        try:
            return len(self.driver.find_elements(*self.STAT_CARDS))
        except Exception:
            return 0

    def is_sidebar_visible(self) -> bool:
        """Return True if the Attendance Monitor sidebar link is visible."""
        return self.is_element_visible(self.NAV_ATTENDANCE)

    def click_attendance_monitor(self):
        """Click the Attendance Monitor sidebar link."""
        self.click_element(self.NAV_ATTENDANCE)

    def click_parent_messages(self):
        """Click the Parent Messages sidebar link."""
        self.click_element(self.NAV_MESSAGES)

    def click_payment_proofs(self):
        """Click the Payment Proofs sidebar link."""
        self.click_element(self.NAV_PAYMENT_PROOF)
