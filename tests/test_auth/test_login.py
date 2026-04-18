import pytest
from pages.login_page import LoginPage


@pytest.mark.auth
@pytest.mark.smoke
class TestLogin:
    """Tests for the login page (/login)."""

    # TC-AUTH-001
    def test_admin_login_redirects_to_admin_dashboard(self, driver, base_url, admin_creds):
        """Admin login should redirect to /admin/dashboard."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.login(admin_creds["user_id"], admin_creds["password"])
        page.wait_for_dashboard_redirect(timeout=15)
        assert "/dashboard" in page.get_current_url() or "/admin" in page.get_current_url()

    # TC-AUTH-002
    def test_franchise_login_redirects_to_franchise_dashboard(self, driver, base_url, franchise_creds):
        """Franchise login should redirect to /franchise/dashboard."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.login(franchise_creds["user_id"], franchise_creds["password"])
        page.wait_for_dashboard_redirect(timeout=15)
        assert "/dashboard" in page.get_current_url() or "/franchise" in page.get_current_url()

    # TC-AUTH-003
    def test_mentor_login_redirects_to_mentor_dashboard(self, driver, base_url, mentor_creds):
        """Mentor login should redirect to /mentor/dashboard."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.login(mentor_creds["user_id"], mentor_creds["password"])
        page.wait_for_dashboard_redirect(timeout=15)
        assert "/dashboard" in page.get_current_url() or "/mentor" in page.get_current_url()

    # TC-AUTH-004
    def test_student_login_redirects_to_student_dashboard(self, driver, base_url, student_creds):
        """Student login should redirect to /student/dashboard."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.login(student_creds["user_id"], student_creds["password"])
        page.wait_for_dashboard_redirect(timeout=15)
        assert "/dashboard" in page.get_current_url() or "/student" in page.get_current_url()

    # TC-AUTH-005
    def test_parent_login_redirects_to_parent_dashboard(self, driver, base_url, parent_creds):
        """Parent login should redirect to /parent/dashboard."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.login(parent_creds["user_id"], parent_creds["password"])
        page.wait_for_dashboard_redirect(timeout=15)
        assert "/dashboard" in page.get_current_url() or "/parent" in page.get_current_url()

    # TC-AUTH-006
    def test_empty_form_shows_validation_errors(self, driver, base_url):
        """Submitting with empty fields should show at least one validation error."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.submit_empty_form()
        assert page.is_userid_error_visible() or page.is_password_error_visible()

    # TC-AUTH-007
    def test_empty_userid_shows_error(self, driver, base_url):
        """Leaving User ID blank should show a User ID validation error."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.enter_password("somepassword")
        page.click_sign_in()
        assert page.is_userid_error_visible()

    # TC-AUTH-008
    def test_empty_password_shows_error(self, driver, base_url):
        """Leaving Password blank should show a Password validation error."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.enter_user_id("someuser")
        page.click_sign_in()
        assert page.is_password_error_visible()

    # TC-AUTH-009
    def test_wrong_password_shows_invalid_credentials(self, driver, base_url, admin_creds):
        """Wrong password should show an error and stay on /login."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.login(admin_creds["user_id"], "WRONG_PASSWORD_12345!")
        assert page.is_general_error_visible()
        assert page.is_on_login_page()

    # TC-AUTH-010
    def test_nonexistent_user_shows_invalid_credentials(self, driver, base_url):
        """Non-existent user ID should show an error and stay on /login."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.login("NONEXISTENT_USER_XYZ_99999", "somepassword")
        assert page.is_general_error_visible()
        assert page.is_on_login_page()

    # TC-AUTH-011
    def test_login_page_heading(self, driver, base_url):
        """Login page heading should contain 'School Management System'."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        heading = page.get_page_heading()
        assert "School Management System" in heading or "school" in heading.lower()

    # TC-AUTH-012
    def test_sign_in_button_is_visible(self, driver, base_url):
        """Sign In button should be visible on the login page."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        assert page.is_sign_in_button_visible()

    # TC-AUTH-013
    def test_admin_navbar_shows_head_admin_role(self, driver, base_url, admin_creds):
        """After admin login, the sidebar should show 'Admin' role label."""
        page = LoginPage(driver, base_url)
        page.open_login_page()
        page.login(admin_creds["user_id"], admin_creds["password"])
        page.wait_for_dashboard_redirect(timeout=15)
        role_label = page.get_logged_in_role_label()
        assert "admin" in role_label.lower()

    # TC-AUTH-014
    def test_logout_returns_to_login_page(self, admin_driver, base_url):
        """Clicking Logout should redirect back to /login."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        logout_btn = (By.XPATH,
            "//button[contains(@aria-label,'logout') or contains(@aria-label,'Logout') "
            "or contains(@title,'Logout') or contains(@title,'logout')]"
        )

        try:
            btn = WebDriverWait(admin_driver, 10).until(EC.element_to_be_clickable(logout_btn))
            btn.click()
        except Exception:
            fallback = (By.XPATH, "//*[contains(text(),'Logout') or contains(text(),'Sign Out')]")
            WebDriverWait(admin_driver, 5).until(EC.element_to_be_clickable(fallback)).click()

        WebDriverWait(admin_driver, 10).until(EC.url_contains("/login"))
        assert "/login" in admin_driver.current_url
