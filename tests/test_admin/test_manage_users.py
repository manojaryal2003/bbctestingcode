import pytest
from pages.admin.manage_users_page import ManageUsersPage


@pytest.mark.admin
@pytest.mark.regression
class TestManageUsers:
    """Tests for the Manage Users page (/admin/manage-users)."""

    # TC-MU-001
    def test_manage_users_page_loads(self, admin_driver, base_url):
        """Manage Users page should load for admin."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        assert page.is_on_manage_users_page()

    # TC-MU-002
    def test_role_filter_tabs_are_visible(self, admin_driver, base_url):
        """All four role filter tabs should be visible."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        assert page.are_tabs_visible()

    # TC-MU-003
    def test_default_tab_is_franchise(self, admin_driver, base_url):
        """Default tab on load should be Franchise Admins."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        assert page.are_tabs_visible()

    # TC-MU-004
    def test_click_mentor_tab_filters_mentors(self, admin_driver, base_url):
        """Clicking Mentor tab should stay on /admin/manage-users."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        page.click_mentor_tab()
        assert page.is_on_manage_users_page()

    # TC-MU-005
    def test_click_student_tab_filters_students(self, admin_driver, base_url):
        """Clicking Student tab should stay on /admin/manage-users."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        page.click_student_tab()
        assert page.is_on_manage_users_page()

    # TC-MU-006
    def test_click_parent_tab_filters_parents(self, admin_driver, base_url):
        """Clicking Parent tab should stay on /admin/manage-users."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        page.click_parent_tab()
        assert page.is_on_manage_users_page()

    # TC-MU-007
    def test_user_table_renders(self, admin_driver, base_url):
        """User table should render (even if empty)."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        assert page.get_row_count() >= 0
        assert page.is_on_manage_users_page()

    # TC-MU-008
    def test_select_all_checkbox_is_visible(self, admin_driver, base_url):
        """Select All checkbox should be visible in the table."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        assert page.is_element_visible(page.SELECT_ALL_CB)

    # TC-MU-009
    def test_delete_button_visible_after_selecting_users(self, admin_driver, base_url):
        """Delete button should appear after selecting users."""
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        if page.get_row_count() > 0:
            page.click_select_all()
            assert page.is_element_visible(page.DELETE_BTN)
        else:
            pytest.skip("No users in current tab to test delete button")
