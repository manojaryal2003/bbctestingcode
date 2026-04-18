from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class StudentDashboardPage(BasePage):
    """Page object for the Student Dashboard (/student/dashboard)."""

    # Locators
    NAV_UPLOAD_ACTIVITY = (By.CSS_SELECTOR, "a[href='/student/upload-activity']")
    NAV_SUBMIT_HW       = (By.CSS_SELECTOR, "a[href='/student/submit-homework']")
    NAV_PROGRESS        = (By.CSS_SELECTOR, "a[href='/student/progress']")
    NAV_BADGES          = (By.CSS_SELECTOR, "a[href='/student/badges']")
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/student/dashboard"

    def open(self):
        """Go to the Student Dashboard and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def is_on_student_dashboard(self):
        return "/student/dashboard" in self.get_current_url()

    def is_sidebar_visible(self):
        return self.is_element_visible(self.NAV_SUBMIT_HW)

    def click_submit_homework(self):
        self.click_element(self.NAV_SUBMIT_HW)

    def click_upload_activity(self):
        self.click_element(self.NAV_UPLOAD_ACTIVITY)

    def click_badges(self):
        self.click_element(self.NAV_BADGES)

    def click_progress(self):
        self.click_element(self.NAV_PROGRESS)
