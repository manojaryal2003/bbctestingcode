"""
Fee Management (Fee Packages) Page Object Model.

Route: /admin/fee-management
Accessible by: HEAD_ADMIN only

From FeeManagement.jsx:
  - Package list table (name, amount, description)
  - "+ Add Package" button
  - Edit (pencil) and Delete (trash) per row
  - Add/Edit modal with fields: name, amount, description
  - Toast notifications for success/error
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FeeManagementPage(BasePage):
    """POM for the Fee Packages page (/admin/fee-management)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Add package button — confirmed from FeeManagement.jsx (Plus icon + text)
    ADD_PACKAGE_BTN     = (By.XPATH, "//button[contains(text(),'Add') or contains(text(),'Package')]")

    # Modal form fields (name="name", name="amount", name="description" not confirmed
    # in JSX — fall back to CSS placeholder / label-based locators)
    MODAL               = (By.CSS_SELECTOR, "[class*='modal'], [class*='Modal']")
    MODAL_NAME_INPUT    = (By.XPATH, "//input[@placeholder[contains(.,'name') or contains(.,'Name')] or @id='name']")
    MODAL_AMOUNT_INPUT  = (By.XPATH, "//input[@placeholder[contains(.,'amount') or contains(.,'Amount')] or @id='amount' or @type='number']")
    MODAL_DESC_INPUT    = (By.XPATH, "//textarea | //input[@placeholder[contains(.,'description') or contains(.,'Description')]]")
    MODAL_SAVE_BTN      = (By.XPATH, "//button[contains(text(),'Save') or contains(text(),'Create') or contains(text(),'Update')]")
    MODAL_CANCEL_BTN    = (By.XPATH, "//button[contains(text(),'Cancel') or contains(text(),'Close')]")

    # Package list rows
    PACKAGE_ROWS        = (By.CSS_SELECTOR, "tbody tr, [class*='packageRow'], [class*='row']")

    # Edit and delete icons per row
    EDIT_BTNS           = (By.CSS_SELECTOR, "button[class*='edit'], button svg[class*='Edit'], button[title*='edit' i]")
    DELETE_BTNS         = (By.CSS_SELECTOR, "button[class*='delete'], button svg[class*='Trash'], button[title*='delete' i]")

    # Toast notification
    TOAST               = (By.CSS_SELECTOR, "[class*='toast'], [class*='Toast']")

    # Loading spinner
    LOADER              = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/admin/fee-management"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self):
        """Navigate to the Fee Packages page and wait for content to load."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    # ── Actions ───────────────────────────────────────────────────────────────

    def click_add_package(self):
        """Click the Add Package button to open the creation modal."""
        self.click_element(self.ADD_PACKAGE_BTN)
        self.wait_for_element(self.MODAL)

    def fill_package_form(self, name: str, amount: str, description: str = ""):
        """
        Fill in the package Add/Edit modal fields.

        Args:
            name:        Package name
            amount:      Numeric fee amount (as string)
            description: Optional description text
        """
        self.enter_text(self.MODAL_NAME_INPUT, name)
        self.enter_text(self.MODAL_AMOUNT_INPUT, amount)
        if description:
            self.enter_text(self.MODAL_DESC_INPUT, description)

    def click_save(self):
        """Click Save in the modal."""
        self.click_element(self.MODAL_SAVE_BTN)

    def click_cancel(self):
        """Click Cancel/Close in the modal."""
        self.click_element(self.MODAL_CANCEL_BTN)

    def create_package(self, name: str, amount: str, description: str = ""):
        """Open modal, fill form, and save a new fee package."""
        self.click_add_package()
        self.fill_package_form(name, amount, description)
        self.click_save()

    def get_package_count(self) -> int:
        """Return the number of package rows in the list."""
        try:
            rows = self.driver.find_elements(*self.PACKAGE_ROWS)
            return len(rows)
        except Exception:
            return 0

    # ── Assertions ────────────────────────────────────────────────────────────

    def is_on_fee_management_page(self) -> bool:
        """Return True if current URL is the Fee Management page."""
        return "/admin/fee-management" in self.get_current_url()

    def is_modal_visible(self) -> bool:
        """Return True if the Add/Edit modal is open."""
        return self.is_element_visible(self.MODAL)

    def is_toast_visible(self) -> bool:
        """Return True if a toast notification is displayed."""
        return self.is_element_visible(self.TOAST)

    def get_toast_text(self) -> str:
        """Return the text content of the toast notification."""
        return self.get_text(self.TOAST)

    def is_add_button_visible(self) -> bool:
        """Return True if the Add Package button is visible."""
        return self.is_element_visible(self.ADD_PACKAGE_BTN)
