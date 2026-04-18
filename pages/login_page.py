from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page (/login)."""

    # Locators — these tell Selenium where to find each element
    USER_ID_INPUT  = (By.NAME, "userId")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")
    GENERAL_ERROR  = (By.CSS_SELECTOR, "[class*='errorAlert']")
    USERID_ERROR   = (By.XPATH, "//input[@name='userId']/following-sibling::*[contains(@class,'error') or contains(@class,'Error')]")
    PASSWORD_ERROR = (By.XPATH, "//input[@name='password']/following-sibling::*[contains(@class,'error') or contains(@class,'Error')]")
    SIDEBAR_ROLE   = (By.CSS_SELECTOR, "[class*='roleLabel']")

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url
        self.login_url = f"{base_url}/login"

    def open_login_page(self):
        """Go to the login page."""
        self.open(self.login_url)
        self.wait_for_element(self.USER_ID_INPUT)

    def enter_user_id(self, user_id):
        self.enter_text(self.USER_ID_INPUT, user_id)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_sign_in(self):
        self.click_element(self.SUBMIT_BUTTON)

    def login(self, user_id, password):
        """Fill both fields and click Sign In."""
        self.enter_user_id(user_id)
        self.enter_password(password)
        self.click_sign_in()

    def submit_empty_form(self):
        """Click Sign In without entering anything (tests validation)."""
        self.click_sign_in()

    def wait_for_dashboard_redirect(self, timeout=15):
        """Wait until browser leaves /login (redirected to a dashboard)."""
        self.wait_for_url_contains("/dashboard", timeout=timeout)

    def is_on_login_page(self):
        return "/login" in self.get_current_url()

    def is_general_error_visible(self):
        return self.is_element_visible(self.GENERAL_ERROR)

    def is_userid_error_visible(self):
        return self.is_element_visible(self.USERID_ERROR)

    def is_password_error_visible(self):
        return self.is_element_visible(self.PASSWORD_ERROR)

    def is_sign_in_button_visible(self):
        return self.is_element_visible(self.SUBMIT_BUTTON)

    def get_general_error_message(self):
        return self.get_text(self.GENERAL_ERROR)

    def get_logged_in_role_label(self):
        """Return the role label shown in the sidebar after login."""
        return self.get_text(self.SIDEBAR_ROLE)

    def get_page_heading(self):
        """Return the heading text on the login card."""
        return self.get_text((By.CSS_SELECTOR, "[class*='title']"))
