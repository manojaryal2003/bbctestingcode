from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MentorDashboardPage(BasePage):
    """Page object for the Mentor Dashboard (/mentor/dashboard)."""

    # Locators
    NAV_ATTENDANCE      = (By.CSS_SELECTOR, "a[href='/mentor/attendance']")
    NAV_UPLOAD_ACTIVITY = (By.CSS_SELECTOR, "a[href='/mentor/upload-activity']")
    NAV_HOMEWORK_MGMT   = (By.CSS_SELECTOR, "a[href='/mentor/homework-management']")
    NAV_EVALUATION      = (By.CSS_SELECTOR, "a[href='/mentor/evaluation']")
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/mentor/dashboard"

    def open(self):
        """Go to the Mentor Dashboard and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_mentor_dashboard(self):
        return "/mentor/dashboard" in self.get_current_url()

    def is_sidebar_visible(self):
        return self.is_element_visible(self.NAV_ATTENDANCE)

    def click_attendance(self):
        self.click_element(self.NAV_ATTENDANCE)

    def click_upload_activity(self):
        self.click_element(self.NAV_UPLOAD_ACTIVITY)

    def click_homework_management(self):
        self.click_element(self.NAV_HOMEWORK_MGMT)

    def click_evaluation(self):
        self.click_element(self.NAV_EVALUATION)
