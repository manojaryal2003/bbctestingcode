from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ManageUsersPage(BasePage):
    """Page object for the Manage Users page (/admin/manage-users)."""

    # Locators
    TAB_FRANCHISE = (By.XPATH, "//button[contains(text(), 'Franchise')]")
    TAB_MENTOR    = (By.XPATH, "//button[contains(text(), 'Mentor')]")
    TAB_STUDENT   = (By.XPATH, "//button[contains(text(), 'Student')]")
    TAB_PARENT    = (By.XPATH, "//button[contains(text(), 'Parent')]")
    TABLE_ROWS    = (By.CSS_SELECTOR, "tbody tr, [class*='tableRow'], [class*='row']")
    SELECT_ALL_CB = (By.XPATH, "//input[@type='checkbox' and not(@name)]")
    DELETE_BTN    = (By.XPATH, "//button[contains(text(),'Delete')]")
    CONFIRM_BTN   = (By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'Yes')]")
    CANCEL_BTN    = (By.XPATH, "//button[contains(text(),'Cancel') or contains(text(),'No')]")
    TOAST         = (By.CSS_SELECTOR, "[class*='toast'], [class*='Toast']")
    LOADER        = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/admin/manage-users"

    def open(self):
        """Go to the Manage Users page and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def click_franchise_tab(self):
        self.click_element(self.TAB_FRANCHISE)

    def click_mentor_tab(self):
        self.click_element(self.TAB_MENTOR)

    def click_student_tab(self):
        self.click_element(self.TAB_STUDENT)

    def click_parent_tab(self):
        self.click_element(self.TAB_PARENT)

    def get_row_count(self):
        """Return how many user rows are visible in the table."""
        try:
            return len(self.driver.find_elements(*self.TABLE_ROWS))
        except Exception:
            return 0

    def click_select_all(self):
        self.click_element(self.SELECT_ALL_CB)

    def click_delete_selected(self):
        self.click_element(self.DELETE_BTN)

    def confirm_delete(self):
        self.click_element(self.CONFIRM_BTN)

    def cancel_delete(self):
        self.click_element(self.CANCEL_BTN)

    def is_on_manage_users_page(self):
        return "/admin/manage-users" in self.get_current_url()

    def are_tabs_visible(self):
        return self.is_element_visible(self.TAB_FRANCHISE)

    def is_toast_visible(self):
        return self.is_element_visible(self.TOAST)

    def get_toast_text(self):
        return self.get_text(self.TOAST)
