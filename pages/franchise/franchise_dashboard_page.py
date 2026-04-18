from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FranchiseDashboardPage(BasePage):
    """Page object for the Franchise Dashboard (/franchise/dashboard)."""

    # Locators
    STAT_CARDS        = (By.CSS_SELECTOR, "[class*='card'], [class*='Card']")
    NAV_ATTENDANCE    = (By.CSS_SELECTOR, "a[href='/franchise/attendance']")
    NAV_MESSAGES      = (By.CSS_SELECTOR, "a[href='/franchise/messages']")
    NAV_PAYMENT_PROOF = (By.CSS_SELECTOR, "a[href='/franchise/payment-proof']")
    LOADER            = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/franchise/dashboard"

    def open(self):
        """Go to the Franchise Dashboard and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_franchise_dashboard(self):
        return "/franchise/dashboard" in self.get_current_url()

    def are_stat_cards_visible(self):
        return self.is_element_visible(self.STAT_CARDS)

    def get_stat_card_count(self):
        try:
            return len(self.driver.find_elements(*self.STAT_CARDS))
        except Exception:
            return 0

    def is_sidebar_visible(self):
        return self.is_element_visible(self.NAV_ATTENDANCE)

    def click_attendance_monitor(self):
        self.click_element(self.NAV_ATTENDANCE)

    def click_parent_messages(self):
        self.click_element(self.NAV_MESSAGES)

    def click_payment_proofs(self):
        self.click_element(self.NAV_PAYMENT_PROOF)
