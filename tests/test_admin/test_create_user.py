import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.admin.create_user_page import CreateUserPage


@pytest.mark.admin
@pytest.mark.regression
class TestCreateUser:
    """Tests for the Create User page (/admin/create-user)."""

    # TC-CU-001
    def test_create_user_page_loads(self, admin_driver, base_url):
        """Create User page should load for admin."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        assert page.is_on_create_user_page()

    # TC-CU-002
    def test_create_user_form_fields_visible(self, admin_driver, base_url):
        """All required form fields should be visible."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        assert page.is_element_visible(page.USER_ID_INPUT),  "User ID input not visible"
        assert page.is_element_visible(page.PASSWORD_INPUT), "Password input not visible"
        assert page.is_element_visible(page.ROLE_SELECT),    "Role select not visible"
        assert page.is_element_visible(page.SUBMIT_BUTTON),  "Submit button not visible"

    # TC-CU-003
    def test_empty_userid_shows_validation_error(self, admin_driver, base_url):
        """Submitting without User ID should show a validation error."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.enter_password("validpass123")
        page.click_submit()
        assert page.is_userid_error_visible()

    # TC-CU-004
    def test_empty_password_shows_validation_error(self, admin_driver, base_url):
        """Submitting without Password should show a validation error."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.enter_user_id("testuser999")
        page.click_submit()
        assert page.is_password_error_visible()

    # TC-CU-005
    def test_short_password_shows_validation_error(self, admin_driver, base_url):
        """Password shorter than 6 characters should show a validation error."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.enter_user_id("testuser999")
        page.enter_password("abc")
        page.click_submit()
        assert page.is_password_error_visible()

    # TC-CU-006
    def test_role_dropdown_has_all_options(self, admin_driver, base_url):
        """Role dropdown should contain all 4 role options."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        select = Select(admin_driver.find_element(*page.ROLE_SELECT))
        values = [o.get_attribute("value") for o in select.options]
        assert "FRANCHISE_ADMIN" in values
        assert "MENTOR"          in values
        assert "STUDENT"         in values
        assert "PARENT"          in values

    # TC-CU-007
    def test_mentor_role_shows_franchise_admin_field(self, admin_driver, base_url):
        """Selecting MENTOR role should show the franchiseAdminId field."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.select_role("MENTOR")
        assert page.is_element_visible(page.FRANCHISE_ADMIN_ID)

    # TC-CU-008
    def test_student_role_shows_franchise_and_mentor_fields(self, admin_driver, base_url):
        """Selecting STUDENT role should show assignedFranchise and assignedMentor fields."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.select_role("STUDENT")
        assert page.is_element_visible(page.ASSIGNED_FRANCHISE)
        assert page.is_element_visible(page.ASSIGNED_MENTOR)

    # TC-CU-009
    def test_parent_role_shows_student_id_field(self, admin_driver, base_url):
        """Selecting PARENT role should show the studentId field."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.select_role("PARENT")
        assert page.is_element_visible(page.STUDENT_ID_INPUT)

    # TC-CU-010
    def test_mentor_without_franchise_admin_id_shows_error(self, admin_driver, base_url):
        """Submitting MENTOR form without franchiseAdminId should show an error."""
        page = CreateUserPage(admin_driver, base_url)
        page.open()
        page.select_role("MENTOR")
        page.enter_user_id("testmentor_nofranchise")
        page.enter_password("securepass123")
        page.click_submit()

        inline_error = page.is_element_visible(
            (By.XPATH, "//*[contains(text(),'franchise') or contains(text(),'Franchise') "
                       "or contains(text(),'required') or contains(text(),'Required')]"),
            timeout=5
        )
        assert inline_error or page.is_modal_visible()
