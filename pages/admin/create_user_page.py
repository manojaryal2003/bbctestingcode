"""
Create User Page Object Model.

Route: /admin/create-user
Accessible by: HEAD_ADMIN only

From CreateUser.jsx the page has:
  - userId input (name="userId")
  - password input (name="password")
  - role select dropdown (name="role") — values: FRANCHISE_ADMIN, MENTOR, STUDENT, PARENT
  - Conditional fields based on role:
      MENTOR   → franchiseAdminId (name="franchiseAdminId")
      STUDENT  → assignedFranchise (name="assignedFranchise"), assignedMentor (name="assignedMentor")
      PARENT   → studentId (name="studentId") + package checkboxes
  - phone input (name="phone")  — optional
  - Submit button
  - Success/failure modal
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class CreateUserPage(BasePage):
    """POM for the Create User page (/admin/create-user)."""

    # ── Locators ──────────────────────────────────────────────────────────────
    USER_ID_INPUT       = (By.NAME, "userId")
    PASSWORD_INPUT      = (By.NAME, "password")
    ROLE_SELECT         = (By.NAME, "role")
    PHONE_INPUT         = (By.NAME, "phone")

    # Conditional role fields
    FRANCHISE_ADMIN_ID  = (By.NAME, "franchiseAdminId")
    ASSIGNED_FRANCHISE  = (By.NAME, "assignedFranchise")
    ASSIGNED_MENTOR     = (By.NAME, "assignedMentor")
    STUDENT_ID_INPUT    = (By.NAME, "studentId")

    # Submit
    SUBMIT_BUTTON       = (By.CSS_SELECTOR, "button[type='submit']")

    # Result modal — shown on success or failure
    MODAL               = (By.CSS_SELECTOR, "[class*='modal'], [class*='Modal']")
    MODAL_TITLE         = (By.CSS_SELECTOR, "[class*='modal'] [class*='title'], [class*='Modal'] h2, [class*='Modal'] h3")
    MODAL_MESSAGE       = (By.CSS_SELECTOR, "[class*='modal'] [class*='message'], [class*='Modal'] p")
    MODAL_CLOSE_BTN     = (By.CSS_SELECTOR, "[class*='modal'] button, [class*='Modal'] button")

    # Inline field errors
    USERID_ERROR        = (By.XPATH, "//input[@name='userId']/following-sibling::*[contains(@class,'error') or contains(@class,'Error')]")
    PASSWORD_ERROR      = (By.XPATH, "//input[@name='password']/following-sibling::*[contains(@class,'error') or contains(@class,'Error')]")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/admin/create-user"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self):
        """Navigate directly to the Create User page."""
        super().open(self.url)
        self.wait_for_element(self.USER_ID_INPUT)

    # ── Field interactions ────────────────────────────────────────────────────

    def enter_user_id(self, user_id: str):
        """Type into the User ID field."""
        self.enter_text(self.USER_ID_INPUT, user_id)

    def enter_password(self, password: str):
        """Type into the Password field."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def select_role(self, role_value: str):
        """
        Select a role from the dropdown.

        Args:
            role_value: one of 'FRANCHISE_ADMIN', 'MENTOR', 'STUDENT', 'PARENT'
        """
        element = self.wait_for_element(self.ROLE_SELECT)
        Select(element).select_by_value(role_value)

    def enter_phone(self, phone: str):
        """Type into the optional Phone field."""
        self.enter_text(self.PHONE_INPUT, phone)

    def enter_franchise_admin_id(self, fid: str):
        """Fill the franchiseAdminId field (required for MENTOR role)."""
        self.enter_text(self.FRANCHISE_ADMIN_ID, fid)

    def enter_assigned_franchise(self, franchise_id: str):
        """Fill the assignedFranchise field (required for STUDENT role)."""
        self.enter_text(self.ASSIGNED_FRANCHISE, franchise_id)

    def enter_assigned_mentor(self, mentor_id: str):
        """Fill the assignedMentor field (required for STUDENT role)."""
        self.enter_text(self.ASSIGNED_MENTOR, mentor_id)

    def enter_student_id(self, student_id: str):
        """Fill the studentId field (required for PARENT role)."""
        self.enter_text(self.STUDENT_ID_INPUT, student_id)

    def click_submit(self):
        """Click the Create User submit button."""
        self.click_element(self.SUBMIT_BUTTON)

    # ── Composite flows ───────────────────────────────────────────────────────

    def create_franchise_admin(self, user_id: str, password: str, phone: str = ""):
        """Fill and submit the form for a Franchise Admin user."""
        self.enter_user_id(user_id)
        self.enter_password(password)
        self.select_role("FRANCHISE_ADMIN")
        if phone:
            self.enter_phone(phone)
        self.click_submit()

    def create_mentor(self, user_id: str, password: str, franchise_admin_id: str):
        """Fill and submit the form for a Mentor user."""
        self.enter_user_id(user_id)
        self.enter_password(password)
        self.select_role("MENTOR")
        self.enter_franchise_admin_id(franchise_admin_id)
        self.click_submit()

    def create_student(self, user_id: str, password: str,
                       assigned_franchise: str, assigned_mentor: str):
        """Fill and submit the form for a Student user."""
        self.enter_user_id(user_id)
        self.enter_password(password)
        self.select_role("STUDENT")
        self.enter_assigned_franchise(assigned_franchise)
        self.enter_assigned_mentor(assigned_mentor)
        self.click_submit()

    # ── Assertions ────────────────────────────────────────────────────────────

    def is_modal_visible(self) -> bool:
        """Return True if the result modal is displayed."""
        return self.is_element_visible(self.MODAL)

    def get_modal_title(self) -> str:
        """Return the modal heading text."""
        return self.get_text(self.MODAL_TITLE)

    def close_modal(self):
        """Dismiss the result modal by clicking its button."""
        self.click_element(self.MODAL_CLOSE_BTN)

    def is_on_create_user_page(self) -> bool:
        """Return True if current URL is the Create User page."""
        return "/admin/create-user" in self.get_current_url()

    def is_userid_error_visible(self) -> bool:
        """Return True if the User ID validation error is shown."""
        return self.is_element_visible(self.USERID_ERROR)

    def is_password_error_visible(self) -> bool:
        """Return True if the Password validation error is shown."""
        return self.is_element_visible(self.PASSWORD_ERROR)
