from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ParentDashboardPage(BasePage):
    """Page object for the Parent Dashboard (/parent/dashboard)."""

    # Locators
    NAV_ATTENDANCE      = (By.CSS_SELECTOR, "a[href='/parent/attendance-report']")
    NAV_FEE_STATUS      = (By.CSS_SELECTOR, "a[href='/parent/fee-status']")
    NAV_HOMEWORK        = (By.CSS_SELECTOR, "a[href='/parent/homework']")
    NAV_PROGRESS_REPORT = (By.CSS_SELECTOR, "a[href='/parent/progress-report']")
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/parent/dashboard"

    def open(self):
        """Go to the Parent Dashboard and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_parent_dashboard(self):
        return "/parent/dashboard" in self.get_current_url()

    def is_sidebar_visible(self):
        return self.is_element_visible(self.NAV_FEE_STATUS)

    def click_attendance_from_sidebar(self):
        self.click_element(self.NAV_ATTENDANCE)

    def click_fee_status_from_sidebar(self):
        self.click_element(self.NAV_FEE_STATUS)

    def click_homework_from_sidebar(self):
        self.click_element(self.NAV_HOMEWORK)

    def click_progress_report(self):
        self.click_element(self.NAV_PROGRESS_REPORT)
