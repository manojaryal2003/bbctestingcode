from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class CreateUserPage(BasePage):
    """Page object for the Create User page (/admin/create-user)."""

    # Locators
    USER_ID_INPUT      = (By.NAME, "userId")
    PASSWORD_INPUT     = (By.NAME, "password")
    ROLE_SELECT        = (By.NAME, "role")
    PHONE_INPUT        = (By.NAME, "phone")
    FRANCHISE_ADMIN_ID = (By.NAME, "franchiseAdminId")
    ASSIGNED_FRANCHISE = (By.NAME, "assignedFranchise")
    ASSIGNED_MENTOR    = (By.NAME, "assignedMentor")
    STUDENT_ID_INPUT   = (By.NAME, "studentId")
    SUBMIT_BUTTON      = (By.CSS_SELECTOR, "button[type='submit']")
    MODAL              = (By.CSS_SELECTOR, "[class*='modal'], [class*='Modal']")
    MODAL_TITLE        = (By.CSS_SELECTOR, "[class*='modal'] h2, [class*='Modal'] h2, [class*='Modal'] h3")
    MODAL_CLOSE_BTN    = (By.CSS_SELECTOR, "[class*='modal'] button, [class*='Modal'] button")
    USERID_ERROR       = (By.XPATH, "//input[@name='userId']/following-sibling::*[contains(@class,'error') or contains(@class,'Error')]")
    PASSWORD_ERROR     = (By.XPATH, "//input[@name='password']/following-sibling::*[contains(@class,'error') or contains(@class,'Error')]")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.url = f"{base_url}/admin/create-user"

    def open(self):
        """Go to the Create User page."""
        super().open(self.url)
        self.wait_for_element(self.USER_ID_INPUT)

    def enter_user_id(self, user_id):
        self.enter_text(self.USER_ID_INPUT, user_id)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def select_role(self, role_value):
        """Select a role. Options: FRANCHISE_ADMIN, MENTOR, STUDENT, PARENT"""
        element = self.wait_for_element(self.ROLE_SELECT)
        Select(element).select_by_value(role_value)

    def enter_phone(self, phone):
        self.enter_text(self.PHONE_INPUT, phone)

    def enter_franchise_admin_id(self, fid):
        self.enter_text(self.FRANCHISE_ADMIN_ID, fid)

    def enter_assigned_franchise(self, franchise_id):
        self.enter_text(self.ASSIGNED_FRANCHISE, franchise_id)

    def enter_assigned_mentor(self, mentor_id):
        self.enter_text(self.ASSIGNED_MENTOR, mentor_id)

    def enter_student_id(self, student_id):
        self.enter_text(self.STUDENT_ID_INPUT, student_id)

    def click_submit(self):
        self.click_element(self.SUBMIT_BUTTON)

    def is_on_create_user_page(self):
        return "/admin/create-user" in self.get_current_url()

    def is_modal_visible(self):
        return self.is_element_visible(self.MODAL)

    def get_modal_title(self):
        return self.get_text(self.MODAL_TITLE)

    def close_modal(self):
        self.click_element(self.MODAL_CLOSE_BTN)

    def is_userid_error_visible(self):
        return self.is_element_visible(self.USERID_ERROR)

    def is_password_error_visible(self):
        return self.is_element_visible(self.PASSWORD_ERROR)
