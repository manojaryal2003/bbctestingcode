"""
Parent Fee Status Page Object Model.

Route: /parent/fee-status
Accessible by: PARENT only

From FeeStatusDisplay.jsx — shows the child's fee bills and payment status.
Lists bills with amount, status (paid/unpaid), and due dates.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FeeStatusPage(BasePage):
    """POM for the Parent Fee Status page (/parent/fee-status)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Page heading
    PAGE_HEADING    = (By.CSS_SELECTOR, "h1, h2, [class*='heading'], [class*='title']")

    # Bill list container
    BILL_LIST       = (By.CSS_SELECTOR, "[class*='bill'], [class*='Bill'], [class*='fee'], [class*='Fee']")
    BILL_ROWS       = (By.CSS_SELECTOR, "[class*='billRow'], [class*='bill-item'], tbody tr")

    # Payment status badges
    STATUS_PAID     = (By.XPATH, "//*[contains(text(),'Paid') or contains(text(),'paid')]")
    STATUS_UNPAID   = (By.XPATH, "//*[contains(text(),'Unpaid') or contains(text(),'unpaid') or contains(text(),'Pending')]")

    # Summary / totals section
    TOTAL_SECTION   = (By.CSS_SELECTOR, "[class*='total'], [class*='summary'], [class*='Summary']")

    # Loader
    LOADER          = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    # Empty state
    EMPTY_MSG       = (By.XPATH, "//*[contains(text(),'No bills') or contains(text(),'No fee') or contains(text(),'no record')]")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/parent/fee-status"

    def open(self):
        """Navigate to the Parent Fee Status page."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def get_bill_count(self) -> int:
        """Return the number of fee bill rows displayed."""
        try:
            rows = self.driver.find_elements(*self.BILL_ROWS)
            return len(rows)
        except Exception:
            return 0

    def is_on_fee_status_page(self) -> bool:
        """Return True if current URL is the Fee Status page."""
        return "/parent/fee-status" in self.get_current_url()

    def is_bill_list_visible(self) -> bool:
        """Return True if the bill list container is visible."""
        return self.is_element_visible(self.BILL_LIST)

    def is_paid_status_visible(self) -> bool:
        """Return True if at least one 'Paid' status is shown."""
        return self.is_element_visible(self.STATUS_PAID)

    def is_unpaid_status_visible(self) -> bool:
        """Return True if at least one 'Unpaid/Pending' status is shown."""
        return self.is_element_visible(self.STATUS_UNPAID)
