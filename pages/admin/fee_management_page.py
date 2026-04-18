from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FeeManagementPage(BasePage):
    """Page object for the Fee Packages page (/admin/fee-management)."""

    # Locators
    ADD_PACKAGE_BTN    = (By.XPATH, "//button[contains(text(),'Add') or contains(text(),'Package')]")
    MODAL              = (By.CSS_SELECTOR, "[class*='modal'], [class*='Modal']")
    MODAL_NAME_INPUT   = (By.XPATH, "//input[@placeholder[contains(.,'name') or contains(.,'Name')] or @id='name']")
    MODAL_AMOUNT_INPUT = (By.XPATH, "//input[@placeholder[contains(.,'amount') or contains(.,'Amount')] or @id='amount' or @type='number']")
    MODAL_DESC_INPUT   = (By.XPATH, "//textarea | //input[@placeholder[contains(.,'description') or contains(.,'Description')]]")
    MODAL_SAVE_BTN     = (By.XPATH, "//button[contains(text(),'Save') or contains(text(),'Create') or contains(text(),'Update')]")
    MODAL_CANCEL_BTN   = (By.XPATH, "//button[contains(text(),'Cancel') or contains(text(),'Close')]")
    PACKAGE_ROWS       = (By.CSS_SELECTOR, "tbody tr, [class*='packageRow'], [class*='row']")
    TOAST              = (By.CSS_SELECTOR, "[class*='toast'], [class*='Toast']")
    LOADER             = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/admin/fee-management"

    def open(self):
        """Go to the Fee Packages page and wait for it to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    def click_add_package(self):
        """Click Add Package button to open the modal."""
        self.click_element(self.ADD_PACKAGE_BTN)
        self.wait_for_element(self.MODAL)

    def fill_package_form(self, name, amount, description=""):
        self.enter_text(self.MODAL_NAME_INPUT, name)
        self.enter_text(self.MODAL_AMOUNT_INPUT, amount)
        if description:
            self.enter_text(self.MODAL_DESC_INPUT, description)

    def click_save(self):
        self.click_element(self.MODAL_SAVE_BTN)

    def click_cancel(self):
        self.click_element(self.MODAL_CANCEL_BTN)

    def get_package_count(self):
        try:
            return len(self.driver.find_elements(*self.PACKAGE_ROWS))
        except Exception:
            return 0

    def is_on_fee_management_page(self):
        return "/admin/fee-management" in self.get_current_url()

    def is_modal_visible(self):
        return self.is_element_visible(self.MODAL)

    def is_add_button_visible(self):
        return self.is_element_visible(self.ADD_PACKAGE_BTN)

    def is_toast_visible(self):
        return self.is_element_visible(self.TOAST)

    def get_toast_text(self):
        return self.get_text(self.TOAST)
