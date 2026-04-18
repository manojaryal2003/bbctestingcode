"""
Login Page Object Model.

Represents the login page at /login.
Fields confirmed from source: Login.jsx
  - userId input  (name="userId")
  - password input (name="password")
  - Submit button  (type="submit", text "Sign In")
  - Error alert div (.errorAlert class for general errors)
  - Field-level validation error spans
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """POM for the /login page of BBC School Management System."""

    # ── Locators (NAME first per spec, then fallbacks) ────────────────────────
    USER_ID_INPUT   = (By.NAME, "userId")
    PASSWORD_INPUT  = (By.NAME, "password")

    # Submit button — no name attr, use CSS on type
    SUBMIT_BUTTON   = (By.CSS_SELECTOR, "button[type='submit']")

    # General error alert (wrong credentials, locked account, etc.)
    GENERAL_ERROR   = (By.CSS_SELECTOR, "[class*='errorAlert']")

    # Field validation errors rendered as text under inputs
    USERID_ERROR    = (By.XPATH, "//input[@name='userId']/following-sibling::*[contains(@class,'error') or contains(@class,'Error')]")
    PASSWORD_ERROR  = (By.XPATH, "//input[@name='password']/following-sibling::*[contains(@class,'error') or contains(@class,'Error')]")

    # After login — sidebar role badge confirms which dashboard loaded
    SIDEBAR_ROLE    = (By.CSS_SELECTOR, "[class*='roleLabel']")

    # Loading spinner that appears while login request is in flight
    LOADING_BUTTON  = (By.XPATH, "//button[@type='submit' and @disabled]")

    def __init__(self, driver, base_url: str, timeout: int = 10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.login_url = f"{base_url}/login"

    # ── Navigation ────────────────────────────────────────────────────────────

    def open_login_page(self):
        """Navigate to /login and wait for the page to be ready."""
        self.open(self.login_url)
        self.wait_for_element(self.USER_ID_INPUT)

    # ── Actions ───────────────────────────────────────────────────────────────

    def enter_user_id(self, user_id: str):
        """Type `user_id` into the User ID field."""
        self.enter_text(self.USER_ID_INPUT, user_id)

    def enter_password(self, password: str):
        """Type `password` into the Password field."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_sign_in(self):
        """Click the Sign In button."""
        self.click_element(self.SUBMIT_BUTTON)

    def login(self, user_id: str, password: str):
        """
        Full login flow: fill both fields then submit.

        Steps:
            1. Enter user_id in the User ID field
            2. Enter password in the Password field
            3. Click the Sign In button

        Does NOT assert success — callers decide what to verify next.
        """
        self.enter_user_id(user_id)
        self.enter_password(password)
        self.click_sign_in()

    def submit_empty_form(self):
        """Click Sign In without entering any credentials (tests validation)."""
        self.click_sign_in()

    # ── Assertions / Getters ──────────────────────────────────────────────────

    def get_general_error_message(self) -> str:
        """Return the text of the general error alert (wrong creds, locked, etc.)."""
        return self.get_text(self.GENERAL_ERROR)

    def is_general_error_visible(self) -> bool:
        """Return True if a general error alert is displayed."""
        return self.is_element_visible(self.GENERAL_ERROR)

    def is_userid_error_visible(self) -> bool:
        """Return True if the User ID field shows a validation error."""
        return self.is_element_visible(self.USERID_ERROR)

    def is_password_error_visible(self) -> bool:
        """Return True if the Password field shows a validation error."""
        return self.is_element_visible(self.PASSWORD_ERROR)

    def is_on_login_page(self) -> bool:
        """Return True if the browser is currently on the /login route."""
        return "/login" in self.get_current_url()

    def wait_for_dashboard_redirect(self, timeout: int = 15):
        """
        After a successful login, wait until the browser navigates away from /login.
        The app redirects each role to its own dashboard route.
        """
        self.wait_for_url_contains("/dashboard", timeout=timeout)

    def get_logged_in_role_label(self) -> str:
        """
        After login, return the role label shown in the sidebar.
        e.g. 'Head Admin', 'Mentor', 'Student', etc.
        """
        return self.get_text(self.SIDEBAR_ROLE)

    def is_sign_in_button_visible(self) -> bool:
        """Return True if the Sign In button is present on the page."""
        return self.is_element_visible(self.SUBMIT_BUTTON)

    def get_page_heading(self) -> str:
        """Return the main heading text on the login card ('School Management System')."""
        heading_locator = (By.CSS_SELECTOR, "[class*='title']")
        return self.get_text(heading_locator)
