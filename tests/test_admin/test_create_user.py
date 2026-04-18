"""
test_create_user.py — Create User form regression tests.

Feature: Create User page at /admin/create-user
Source:  Frontend/src/pages/admin/CreateUser/CreateUser.jsx

Test Cases:
  TC-CU-001  Create User page loads for admin
  TC-CU-002  Form is visible with required fields
  TC-CU-003  Submit with empty User ID shows validation error
  TC-CU-004  Submit with empty Password shows validation error
  TC-CU-005  Submit with password shorter than 6 chars shows validation error
  TC-CU-006  Role dropdown contains all expected role options
  TC-CU-007  Selecting MENTOR role shows franchiseAdminId field
  TC-CU-008  Selecting STUDENT role shows assignedFranchise and assignedMentor fields
  TC-CU-009  Selecting PARENT role shows studentId field
  TC-CU-010  Submitting MENTOR form without franchiseAdminId shows validation error
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.admin.create_user_page import CreateUserPage


@pytest.mark.admin
@pytest.mark.regression
class TestCreateUser:
    """Regression tests for the Create User page."""

    # ── TC-CU-001 ──────────────────────────────────────────────────────────────
    def test_create_user_page_loads(self, admin_driver, base_url):
        """
        Purpose: Create User page loads successfully for HEAD_ADMIN.
        Steps:
            1. Navigate to /admin/create-user using admin_driver
        Expected: URL contains /admin/create-user; User ID field is visible.
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        assert page.is_on_create_user_page(), (
            f"Expected /admin/create-user URL, got: {page.get_current_url()}"
        )

    # ── TC-CU-002 ──────────────────────────────────────────────────────────────
    def test_create_user_form_fields_visible(self, admin_driver, base_url):
        """
        Purpose: All required form fields are visible on page load.
        Steps:
            1. Open /admin/create-user
        Expected: User ID input, Password input, Role select, and Submit button are visible.
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()

        assert page.is_element_visible(page.USER_ID_INPUT),    "User ID input not visible"
        assert page.is_element_visible(page.PASSWORD_INPUT),   "Password input not visible"
        assert page.is_element_visible(page.ROLE_SELECT),      "Role select not visible"
        assert page.is_element_visible(page.SUBMIT_BUTTON),    "Submit button not visible"

    # ── TC-CU-003 ──────────────────────────────────────────────────────────────
    def test_empty_userid_shows_validation_error(self, admin_driver, base_url):
        """
        Purpose: Submitting without a User ID shows a validation error.
        Steps:
            1. Open /admin/create-user
            2. Enter only a password
            3. Click Submit
        Expected: User ID validation error is shown.
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.enter_password("validpass123")
        page.click_submit()

        assert page.is_userid_error_visible(), (
            "Expected User ID validation error when User ID is empty"
        )

    # ── TC-CU-004 ──────────────────────────────────────────────────────────────
    def test_empty_password_shows_validation_error(self, admin_driver, base_url):
        """
        Purpose: Submitting without a Password shows a validation error.
        Steps:
            1. Open /admin/create-user
            2. Enter only a User ID
            3. Click Submit
        Expected: Password validation error is shown.
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.enter_user_id("testuser999")
        page.click_submit()

        assert page.is_password_error_visible(), (
            "Expected Password validation error when Password is empty"
        )

    # ── TC-CU-005 ──────────────────────────────────────────────────────────────
    def test_short_password_shows_validation_error(self, admin_driver, base_url):
        """
        Purpose: Password shorter than 6 characters shows a validation error.
        Steps:
            1. Open /admin/create-user
            2. Enter User ID and a 3-character password
            3. Click Submit
        Expected: Password validation error is shown ('at least 6 characters').
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.enter_user_id("testuser999")
        page.enter_password("abc")
        page.click_submit()

        assert page.is_password_error_visible(), (
            "Expected Password validation error for password shorter than 6 characters"
        )

    # ── TC-CU-006 ──────────────────────────────────────────────────────────────
    def test_role_dropdown_has_all_options(self, admin_driver, base_url):
        """
        Purpose: Role dropdown contains all 4 creatable roles.
        Steps:
            1. Open /admin/create-user
            2. Read options from the Role select element
        Expected: Options include FRANCHISE_ADMIN, MENTOR, STUDENT, PARENT.
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()

        select_el = admin_driver.find_element(*page.ROLE_SELECT)
        select = Select(select_el)
        option_values = [o.get_attribute("value") for o in select.options]

        assert "FRANCHISE_ADMIN" in option_values, "FRANCHISE_ADMIN option missing"
        assert "MENTOR"          in option_values, "MENTOR option missing"
        assert "STUDENT"         in option_values, "STUDENT option missing"
        assert "PARENT"          in option_values, "PARENT option missing"

    # ── TC-CU-007 ──────────────────────────────────────────────────────────────
    def test_mentor_role_shows_franchise_admin_field(self, admin_driver, base_url):
        """
        Purpose: Selecting MENTOR role reveals the franchiseAdminId input.
        Steps:
            1. Open /admin/create-user
            2. Select MENTOR from the Role dropdown
        Expected: franchiseAdminId input field becomes visible.
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.select_role("MENTOR")

        assert page.is_element_visible(page.FRANCHISE_ADMIN_ID), (
            "Expected franchiseAdminId field to appear when MENTOR role is selected"
        )

    # ── TC-CU-008 ──────────────────────────────────────────────────────────────
    def test_student_role_shows_franchise_and_mentor_fields(self, admin_driver, base_url):
        """
        Purpose: Selecting STUDENT role reveals assignedFranchise and assignedMentor fields.
        Steps:
            1. Open /admin/create-user
            2. Select STUDENT from the Role dropdown
        Expected: Both assignedFranchise and assignedMentor fields are visible.
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.select_role("STUDENT")

        assert page.is_element_visible(page.ASSIGNED_FRANCHISE), (
            "Expected assignedFranchise field for STUDENT role"
        )
        assert page.is_element_visible(page.ASSIGNED_MENTOR), (
            "Expected assignedMentor field for STUDENT role"
        )

    # ── TC-CU-009 ──────────────────────────────────────────────────────────────
    def test_parent_role_shows_student_id_field(self, admin_driver, base_url):
        """
        Purpose: Selecting PARENT role reveals the studentId input.
        Steps:
            1. Open /admin/create-user
            2. Select PARENT from the Role dropdown
        Expected: studentId input field becomes visible.
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.select_role("PARENT")

        assert page.is_element_visible(page.STUDENT_ID_INPUT), (
            "Expected studentId field to appear when PARENT role is selected"
        )

    # ── TC-CU-010 ──────────────────────────────────────────────────────────────
    def test_mentor_without_franchise_admin_id_shows_error(self, admin_driver, base_url):
        """
        Purpose: Submitting a MENTOR form without franchiseAdminId shows validation error.
        Steps:
            1. Open /admin/create-user
            2. Select MENTOR role
            3. Fill User ID and Password but leave franchiseAdminId blank
            4. Click Submit
        Expected: A validation error is shown (modal or inline).
        """
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.select_role("MENTOR")
        page.enter_user_id("testmentor_nofranchise")
        page.enter_password("securepass123")
        page.click_submit()

        # Error may appear as inline text or as a modal
        inline_error = page.is_element_visible(
            (By.XPATH, "//*[contains(text(),'franchise') or contains(text(),'Franchise') "
                       "or contains(text(),'required') or contains(text(),'Required')]"),
            timeout=5
        )
        modal_shown = page.is_modal_visible()

        assert inline_error or modal_shown, (
            "Expected a validation error when franchiseAdminId is missing for MENTOR"
        )
