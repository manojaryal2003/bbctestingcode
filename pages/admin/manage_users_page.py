"""
Manage Users Page Object Model.

Route: /admin/manage-users
Accessible by: HEAD_ADMIN only

From ManageUsers.jsx:
  - Role filter tabs: FRANCHISE_ADMIN, MENTOR, STUDENT, PARENT
  - User table with checkboxes, userId, role columns
  - "Delete Selected" button
  - "Reset Password" action per user row
  - Confirmation modal for bulk delete
  - Toast notification on success/failure
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ManageUsersPage(BasePage):
    """POM for the Manage Users page (/admin/manage-users)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Role filter tabs (each tab is a button containing the role label text)
    TAB_FRANCHISE   = (By.XPATH, "//button[contains(text(), 'Franchise')]")
    TAB_MENTOR      = (By.XPATH, "//button[contains(text(), 'Mentor')]")
    TAB_STUDENT     = (By.XPATH, "//button[contains(text(), 'Student')]")
    TAB_PARENT      = (By.XPATH, "//button[contains(text(), 'Parent')]")

    # User table rows
    TABLE_ROWS      = (By.CSS_SELECTOR, "tbody tr, [class*='tableRow'], [class*='row']")

    # Select-all checkbox
    SELECT_ALL_CB   = (By.XPATH, "//input[@type='checkbox' and not(@name)]")

    # Delete selected button
    DELETE_BTN      = (By.XPATH, "//button[contains(text(),'Delete')]")

    # Confirmation modal buttons
    CONFIRM_BTN     = (By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'Yes')]")
    CANCEL_BTN      = (By.XPATH, "//button[contains(text(),'Cancel') or contains(text(),'No')]")

    # Toast notification
    TOAST           = (By.CSS_SELECTOR, "[class*='toast'], [class*='Toast']")

    # Reset password modal input
    RESET_PW_INPUT  = (By.CSS_SELECTOR, "input[type='password'], input[placeholder*='password' i], input[placeholder*='Password']")
    RESET_PW_BTN    = (By.XPATH, "//button[contains(text(),'Reset') or contains(text(),'Save')]")

    # Loading state
    LOADER          = (By.CSS_SELECTOR, "[class*='loader'], [class*='Loader']")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/admin/manage-users"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self):
        """Navigate directly to Manage Users and wait for content."""
        super().open(self.url)
        self.wait_for_element_to_disappear(self.LOADER, timeout=15)

    # ── Tab interactions ──────────────────────────────────────────────────────

    def click_franchise_tab(self):
        """Switch to the Franchise Admin tab."""
        self.click_element(self.TAB_FRANCHISE)

    def click_mentor_tab(self):
        """Switch to the Mentor tab."""
        self.click_element(self.TAB_MENTOR)

    def click_student_tab(self):
        """Switch to the Student tab."""
        self.click_element(self.TAB_STUDENT)

    def click_parent_tab(self):
        """Switch to the Parent tab."""
        self.click_element(self.TAB_PARENT)

    # ── Table helpers ─────────────────────────────────────────────────────────

    def get_row_count(self) -> int:
        """Return the number of user rows currently visible in the table."""
        try:
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            return len(rows)
        except Exception:
            return 0

    def click_select_all(self):
        """Toggle the select-all checkbox."""
        self.click_element(self.SELECT_ALL_CB)

    def click_delete_selected(self):
        """Click the Delete Selected button."""
        self.click_element(self.DELETE_BTN)

    def confirm_delete(self):
        """Click Confirm in the deletion confirmation modal."""
        self.click_element(self.CONFIRM_BTN)

    def cancel_delete(self):
        """Click Cancel in the deletion confirmation modal."""
        self.click_element(self.CANCEL_BTN)

    # ── Assertions ────────────────────────────────────────────────────────────

    def is_on_manage_users_page(self) -> bool:
        """Return True if current URL is the Manage Users page."""
        return "/admin/manage-users" in self.get_current_url()

    def is_toast_visible(self) -> bool:
        """Return True if a toast notification is displayed."""
        return self.is_element_visible(self.TOAST)

    def get_toast_text(self) -> str:
        """Return the text content of the toast notification."""
        return self.get_text(self.TOAST)

    def are_tabs_visible(self) -> bool:
        """Return True if the role filter tabs are rendered."""
        return self.is_element_visible(self.TAB_FRANCHISE)
