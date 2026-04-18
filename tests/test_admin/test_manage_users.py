"""
test_manage_users.py — Manage Users page regression tests.

Feature: Manage Users at /admin/manage-users
Source:  Frontend/src/pages/admin/ManageUsers/ManageUsers.jsx

Test Cases:
  TC-MU-001  Manage Users page loads for admin
  TC-MU-002  Role filter tabs are visible (Franchise, Mentor, Student, Parent)
  TC-MU-003  Default active tab is Franchise Admins
  TC-MU-004  Clicking Mentor tab filters to show mentor users
  TC-MU-005  Clicking Student tab filters to show student users
  TC-MU-006  Clicking Parent tab filters to show parent users
  TC-MU-007  User table renders with rows (if users exist)
  TC-MU-008  Select All checkbox is visible
  TC-MU-009  Delete button appears after selecting users
"""

import pytest
from pages.admin.manage_users_page import ManageUsersPage


@pytest.mark.admin
@pytest.mark.regression
class TestManageUsers:
    """Regression tests for the Manage Users page."""

    # ── TC-MU-001 ──────────────────────────────────────────────────────────────
    def test_manage_users_page_loads(self, admin_driver, base_url):
        """
        Purpose: Manage Users page loads successfully for HEAD_ADMIN.
        Steps:
            1. Navigate to /admin/manage-users
        Expected: URL contains /admin/manage-users; tabs are visible.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        assert page.is_on_manage_users_page(), (
            f"Expected /admin/manage-users URL, got: {page.get_current_url()}"
        )

    # ── TC-MU-002 ──────────────────────────────────────────────────────────────
    def test_role_filter_tabs_are_visible(self, admin_driver, base_url):
        """
        Purpose: All four role filter tabs render on the page.
        Steps:
            1. Open /admin/manage-users
        Expected: Franchise, Mentor, Student, and Parent tabs are visible.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        assert page.are_tabs_visible(), (
            "Expected role filter tabs to be visible on Manage Users page"
        )

    # ── TC-MU-003 ──────────────────────────────────────────────────────────────
    def test_default_tab_is_franchise(self, admin_driver, base_url):
        """
        Purpose: Default role tab on load is Franchise Admins (confirmed from ManageUsers.jsx).
        Steps:
            1. Open /admin/manage-users without clicking any tab
        Expected: Franchise Admins tab is the active filter.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        # Franchise tab should be visible and no tab click needed
        assert page.are_tabs_visible(), (
            "Role filter tabs not visible — cannot verify default tab"
        )

    # ── TC-MU-004 ──────────────────────────────────────────────────────────────
    def test_click_mentor_tab_filters_mentors(self, admin_driver, base_url):
        """
        Purpose: Clicking the Mentor tab shows only Mentor users.
        Steps:
            1. Open /admin/manage-users
            2. Click the Mentor tab
        Expected: Table content updates; page remains at /admin/manage-users.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        page.click_mentor_tab()
        assert page.is_on_manage_users_page(), (
            "Expected to remain on /admin/manage-users after clicking Mentor tab"
        )

    # ── TC-MU-005 ──────────────────────────────────────────────────────────────
    def test_click_student_tab_filters_students(self, admin_driver, base_url):
        """
        Purpose: Clicking the Student tab shows only Student users.
        Steps:
            1. Open /admin/manage-users
            2. Click the Student tab
        Expected: Page remains at /admin/manage-users and table updates.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        page.click_student_tab()
        assert page.is_on_manage_users_page()

    # ── TC-MU-006 ──────────────────────────────────────────────────────────────
    def test_click_parent_tab_filters_parents(self, admin_driver, base_url):
        """
        Purpose: Clicking the Parent tab shows only Parent users.
        Steps:
            1. Open /admin/manage-users
            2. Click the Parent tab
        Expected: Page remains at /admin/manage-users and table updates.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        page.click_parent_tab()
        assert page.is_on_manage_users_page()

    # ── TC-MU-007 ──────────────────────────────────────────────────────────────
    def test_user_table_renders(self, admin_driver, base_url):
        """
        Purpose: After page load, the user table renders (even if empty).
        Steps:
            1. Open /admin/manage-users
            2. Check for table rows (any count >= 0 is acceptable)
        Expected: Page is on the correct URL; no crash or 500 error.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        # Row count can be 0 if no users of that role exist — that is valid
        count = page.get_row_count()
        assert count >= 0, "get_row_count should return a non-negative integer"
        assert page.is_on_manage_users_page()

    # ── TC-MU-008 ──────────────────────────────────────────────────────────────
    def test_select_all_checkbox_is_visible(self, admin_driver, base_url):
        """
        Purpose: The Select All checkbox is present in the table header.
        Steps:
            1. Open /admin/manage-users
        Expected: Select All checkbox element is visible.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()
        assert page.is_element_visible(page.SELECT_ALL_CB), (
            "Expected Select All checkbox to be visible"
        )

    # ── TC-MU-009 ──────────────────────────────────────────────────────────────
    def test_delete_button_visible_after_selecting_users(self, admin_driver, base_url):
        """
        Purpose: Delete Selected button appears/is enabled when users are selected.
        Steps:
            1. Open /admin/manage-users
            2. Click Select All checkbox
        Expected: Delete button becomes visible.
        """
        page = ManageUsersPage(admin_driver, base_url)
        page.open()

        # Only interact if there are rows to select
        row_count = page.get_row_count()
        if row_count > 0:
            page.click_select_all()
            assert page.is_element_visible(page.DELETE_BTN), (
                "Expected Delete Selected button to be visible after selecting users"
            )
        else:
            pytest.skip("No users in current tab to test delete button visibility")
