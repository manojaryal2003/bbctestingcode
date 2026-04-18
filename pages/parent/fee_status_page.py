from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FeeStatusPage(BasePage):
    """Page object for the Parent Fee Status page (/parent/fee-status)."""

    # Locators
    BILL_LIST    = (By.CSS_SELECTOR, "[class*='bill'], [class*='Bill'], [class*='fee'], [class*='Fee']")
    BILL_ROWS    = (By.CSS_SELECTOR, "[class*='billRow'], [class*='bill-item'], tbody tr")
    STATUS_PAID  = (By.XPATH, "//*[contains(text(),'Paid') or contains(text(),'paid')]")
    STATUS_UNPAID= (By.XPATH, "//*[contains(text(),'Unpaid') or contains(text(),'unpaid') or contains(text(),'Pending')]")
    LOADER       = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/parent/fee-status"

    def open(self):
        """Go to the Fee Status page and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def get_bill_count(self):
        try:
            return len(self.driver.find_elements(*self.BILL_ROWS))
        except Exception:
            return 0

    def is_on_fee_status_page(self):
        return "/parent/fee-status" in self.get_current_url()

    def is_bill_list_visible(self):
        return self.is_element_visible(self.BILL_LIST)

    def is_paid_status_visible(self):
        return self.is_element_visible(self.STATUS_PAID)

    def is_unpaid_status_visible(self):
        return self.is_element_visible(self.STATUS_UNPAID)
