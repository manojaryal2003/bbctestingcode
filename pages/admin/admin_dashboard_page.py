from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdminDashboardPage(BasePage):
    """Page object for the Admin Dashboard (/admin/dashboard)."""

    # Locators
    STAT_CARDS       = (By.CSS_SELECTOR, "[class*='card'], [class*='Card']")
    NAV_CREATE_USER  = (By.CSS_SELECTOR, "a[href='/admin/create-user']")
    NAV_MANAGE_USERS = (By.CSS_SELECTOR, "a[href='/admin/manage-users']")
    NAV_FEE_PACKAGES = (By.CSS_SELECTOR, "a[href='/admin/fee-management']")
    NAV_REPORTS      = (By.CSS_SELECTOR, "a[href='/admin/reports']")
    LOADER           = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/admin/dashboard"

    def open(self):
        """Go to the admin dashboard and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_admin_dashboard(self):
        return "/admin/dashboard" in self.get_current_url()

    def are_stat_cards_visible(self):
        return self.is_element_visible(self.STAT_CARDS)

    def get_stat_card_count(self):
        return len(self.driver.find_elements(*self.STAT_CARDS))

    def is_sidebar_nav_visible(self):
        return self.is_element_visible(self.NAV_CREATE_USER)

    def click_create_user(self):
        self.click_element(self.NAV_CREATE_USER)

    def click_manage_users(self):
        self.click_element(self.NAV_MANAGE_USERS)

    def click_fee_packages(self):
        self.click_element(self.NAV_FEE_PACKAGES)

    def click_reports(self):
        self.click_element(self.NAV_REPORTS)
