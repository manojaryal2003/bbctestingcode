"""
test_login.py — Authentication / Login regression tests.

Feature: Login page at /login
Source: Frontend/src/pages/auth/Login/Login.jsx
        Backend/controllers/authController.js
        Backend/models/User.js

Test Cases:
  TC-AUTH-001  Valid Admin login redirects to admin dashboard
  TC-AUTH-002  Valid Franchise login redirects to franchise dashboard
  TC-AUTH-003  Valid Mentor login redirects to mentor dashboard
  TC-AUTH-004  Valid Student login redirects to student dashboard
  TC-AUTH-005  Valid Parent login redirects to parent dashboard
  TC-AUTH-006  Empty form submission shows validation errors
  TC-AUTH-007  Empty User ID field shows User ID required error
  TC-AUTH-008  Empty Password field shows Password required error
  TC-AUTH-009  Wrong password shows 'Invalid credentials' error
  TC-AUTH-010  Non-existent user ID shows 'Invalid credentials' error
  TC-AUTH-011  Login page heading is 'School Management System'
  TC-AUTH-012  Sign In button is visible on login page
  TC-AUTH-013  Successful login navbar shows correct role label
  TC-AUTH-014  Logout returns user to login page
"""

import pytest
from pages.login_page import LoginPage


@pytest.mark.auth
@pytest.mark.smoke
class TestLogin:
    """Regression tests for the /login authentication page."""

    # ── TC-AUTH-001 ────────────────────────────────────────────────────────────
    def test_admin_login_redirects_to_admin_dashboard(self, driver, base_url, admin_creds):
        """
        Purpose: Verify HEAD_ADMIN login redirects to /admin/dashboard.
        Steps:
            1. Open /login
            2. Enter admin user_id and password from .env
            3. Click Sign In
            4. Wait for redirect
        Expected: URL contains '/admin/dashboard' or '/dashboard'
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.login(admin_creds["user_id"], admin_creds["password"])
        login_page.wait_for_dashboard_redirect(timeout=15)

        current_url = login_page.get_current_url()
        assert "/dashboard" in current_url or "/admin" in current_url, (
            f"Expected admin dashboard URL, got: {current_url}"
        )

    # ── TC-AUTH-002 ────────────────────────────────────────────────────────────
    def test_franchise_login_redirects_to_franchise_dashboard(
            self, driver, base_url, franchise_creds):
        """
        Purpose: Verify FRANCHISE_ADMIN login redirects to /franchise/dashboard.
        Steps:
            1. Open /login
            2. Enter franchise user_id and password from .env
            3. Click Sign In
        Expected: URL contains '/franchise/dashboard' or '/dashboard'
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.login(franchise_creds["user_id"], franchise_creds["password"])
        login_page.wait_for_dashboard_redirect(timeout=15)

        current_url = login_page.get_current_url()
        assert "/dashboard" in current_url or "/franchise" in current_url, (
            f"Expected franchise dashboard URL, got: {current_url}"
        )

    # ── TC-AUTH-003 ────────────────────────────────────────────────────────────
    def test_mentor_login_redirects_to_mentor_dashboard(
            self, driver, base_url, mentor_creds):
        """
        Purpose: Verify MENTOR login redirects to /mentor/dashboard.
        Steps:
            1. Open /login
            2. Enter mentor user_id and password from .env
            3. Click Sign In
        Expected: URL contains '/mentor/dashboard' or '/dashboard'
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.login(mentor_creds["user_id"], mentor_creds["password"])
        login_page.wait_for_dashboard_redirect(timeout=15)

        current_url = login_page.get_current_url()
        assert "/dashboard" in current_url or "/mentor" in current_url, (
            f"Expected mentor dashboard URL, got: {current_url}"
        )

    # ── TC-AUTH-004 ────────────────────────────────────────────────────────────
    def test_student_login_redirects_to_student_dashboard(
            self, driver, base_url, student_creds):
        """
        Purpose: Verify STUDENT login redirects to /student/dashboard.
        Steps:
            1. Open /login
            2. Enter student user_id and password from .env
            3. Click Sign In
        Expected: URL contains '/student/dashboard' or '/dashboard'
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.login(student_creds["user_id"], student_creds["password"])
        login_page.wait_for_dashboard_redirect(timeout=15)

        current_url = login_page.get_current_url()
        assert "/dashboard" in current_url or "/student" in current_url, (
            f"Expected student dashboard URL, got: {current_url}"
        )

    # ── TC-AUTH-005 ────────────────────────────────────────────────────────────
    def test_parent_login_redirects_to_parent_dashboard(
            self, driver, base_url, parent_creds):
        """
        Purpose: Verify PARENT login redirects to /parent/dashboard.
        Steps:
            1. Open /login
            2. Enter parent user_id and password from .env
            3. Click Sign In
        Expected: URL contains '/parent/dashboard' or '/dashboard'
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.login(parent_creds["user_id"], parent_creds["password"])
        login_page.wait_for_dashboard_redirect(timeout=15)

        current_url = login_page.get_current_url()
        assert "/dashboard" in current_url or "/parent" in current_url, (
            f"Expected parent dashboard URL, got: {current_url}"
        )

    # ── TC-AUTH-006 ────────────────────────────────────────────────────────────
    def test_empty_form_shows_validation_errors(self, driver, base_url):
        """
        Purpose: Submitting with both fields empty shows validation errors.
        Steps:
            1. Open /login
            2. Click Sign In without entering any data
        Expected: At least one field validation error is visible
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.submit_empty_form()

        userid_err  = login_page.is_userid_error_visible()
        pass_err    = login_page.is_password_error_visible()
        assert userid_err or pass_err, (
            "Expected at least one field validation error after empty form submission"
        )

    # ── TC-AUTH-007 ────────────────────────────────────────────────────────────
    def test_empty_userid_shows_error(self, driver, base_url):
        """
        Purpose: Leaving User ID blank and submitting shows 'User ID is required'.
        Steps:
            1. Open /login
            2. Enter only a password, leave User ID blank
            3. Click Sign In
        Expected: User ID validation error is visible
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.enter_password("somepassword")
        login_page.click_sign_in()

        assert login_page.is_userid_error_visible(), (
            "Expected User ID validation error to be visible"
        )

    # ── TC-AUTH-008 ────────────────────────────────────────────────────────────
    def test_empty_password_shows_error(self, driver, base_url):
        """
        Purpose: Leaving Password blank and submitting shows 'Password is required'.
        Steps:
            1. Open /login
            2. Enter only a User ID, leave Password blank
            3. Click Sign In
        Expected: Password validation error is visible
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.enter_user_id("someuser")
        login_page.click_sign_in()

        assert login_page.is_password_error_visible(), (
            "Expected Password validation error to be visible"
        )

    # ── TC-AUTH-009 ────────────────────────────────────────────────────────────
    def test_wrong_password_shows_invalid_credentials(
            self, driver, base_url, admin_creds):
        """
        Purpose: Entering correct User ID but wrong password shows error.
        Steps:
            1. Open /login
            2. Enter valid admin User ID
            3. Enter an incorrect password
            4. Click Sign In
        Expected: 'Invalid credentials' error alert is visible; still on /login
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.login(admin_creds["user_id"], "WRONG_PASSWORD_12345!")

        assert login_page.is_general_error_visible(), (
            "Expected general error alert for wrong password"
        )
        assert login_page.is_on_login_page(), (
            "Expected browser to remain on /login after failed login"
        )

    # ── TC-AUTH-010 ────────────────────────────────────────────────────────────
    def test_nonexistent_user_shows_invalid_credentials(self, driver, base_url):
        """
        Purpose: Using a user ID that does not exist shows 'Invalid credentials'.
        Steps:
            1. Open /login
            2. Enter a user ID that cannot exist in the system
            3. Enter any password
            4. Click Sign In
        Expected: Error alert is visible; browser stays on /login
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.login("NONEXISTENT_USER_XYZ_99999", "somepassword")

        assert login_page.is_general_error_visible(), (
            "Expected error alert for non-existent user"
        )
        assert login_page.is_on_login_page(), (
            "Expected browser to remain on /login"
        )

    # ── TC-AUTH-011 ────────────────────────────────────────────────────────────
    def test_login_page_heading(self, driver, base_url):
        """
        Purpose: Verify the login card displays 'School Management System'.
        Steps:
            1. Open /login
        Expected: Heading text contains 'School Management System'
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()

        heading = login_page.get_page_heading()
        assert "School Management System" in heading or "school" in heading.lower(), (
            f"Expected 'School Management System' in heading, got: '{heading}'"
        )

    # ── TC-AUTH-012 ────────────────────────────────────────────────────────────
    def test_sign_in_button_is_visible(self, driver, base_url):
        """
        Purpose: Verify the Sign In submit button is present on load.
        Steps:
            1. Open /login
        Expected: Sign In button is visible
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()

        assert login_page.is_sign_in_button_visible(), (
            "Expected Sign In button to be visible on login page"
        )

    # ── TC-AUTH-013 ────────────────────────────────────────────────────────────
    def test_admin_navbar_shows_head_admin_role(
            self, driver, base_url, admin_creds):
        """
        Purpose: After admin login, navbar/sidebar shows 'Head Admin' role label.
        Steps:
            1. Open /login and log in as HEAD_ADMIN
            2. Wait for dashboard
            3. Read the role label from sidebar
        Expected: Role label contains 'Admin' or 'HEAD_ADMIN'
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        login_page.login(admin_creds["user_id"], admin_creds["password"])
        login_page.wait_for_dashboard_redirect(timeout=15)

        role_label = login_page.get_logged_in_role_label()
        assert "admin" in role_label.lower() or "Admin" in role_label, (
            f"Expected admin role label in sidebar, got: '{role_label}'"
        )

    # ── TC-AUTH-014 ────────────────────────────────────────────────────────────
    def test_logout_returns_to_login_page(self, admin_driver, base_url):
        """
        Purpose: Clicking Logout redirects back to the /login page.
        Steps:
            1. Start with an already-logged-in admin session (admin_driver fixture)
            2. Click the Logout button in the navbar
        Expected: Browser URL contains '/login'
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Logout button — from Navbar.jsx (LogOut icon button, aria label or text)
        logout_btn_locator = (By.XPATH,
            "//button[contains(@aria-label,'logout') or contains(@aria-label,'Logout') "
            "or contains(@title,'Logout') or contains(@title,'logout') "
            "or .//*[name()='svg' and contains(@class,'log')]]"
        )

        try:
            btn = WebDriverWait(admin_driver, 10).until(
                EC.element_to_be_clickable(logout_btn_locator)
            )
            btn.click()
        except Exception:
            # Fallback: look for any element with logout text
            fallback = (By.XPATH, "//*[contains(text(),'Logout') or contains(text(),'Sign Out')]")
            WebDriverWait(admin_driver, 5).until(
                EC.element_to_be_clickable(fallback)
            ).click()

        WebDriverWait(admin_driver, 10).until(EC.url_contains("/login"))
        assert "/login" in admin_driver.current_url, (
            f"Expected /login after logout, got: {admin_driver.current_url}"
        )
