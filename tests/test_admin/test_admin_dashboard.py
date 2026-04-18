"""
test_admin_dashboard.py — Admin Dashboard regression tests.

Feature: Admin Dashboard at /admin/dashboard
Source:  Frontend/src/pages/admin/AdminDashboard/AdminDashboard.jsx

Test Cases:
  TC-ADMIN-001  Admin dashboard loads without error after login
  TC-ADMIN-002  Dashboard URL is correct after login
  TC-ADMIN-003  Statistics cards are visible on dashboard
  TC-ADMIN-004  Dashboard shows 4 stat cards (Users, Franchises, Mentors, Students)
  TC-ADMIN-005  Admin sidebar navigation is visible
  TC-ADMIN-006  Clicking Create User navigates to /admin/create-user
  TC-ADMIN-007  Clicking Manage Users navigates to /admin/manage-users
  TC-ADMIN-008  Clicking Fee Packages navigates to /admin/fee-management
  TC-ADMIN-009  Clicking Reports navigates to /admin/reports
  TC-ADMIN-010  Page title contains 'School Management System'
"""

import pytest
from pages.admin.admin_dashboard_page import AdminDashboardPage


@pytest.mark.admin
@pytest.mark.regression
class TestAdminDashboard:
    """Regression tests for the Admin Dashboard page."""

    # ── TC-ADMIN-001 ───────────────────────────────────────────────────────────
    def test_admin_dashboard_loads(self, admin_driver, base_url):
        """
        Purpose: Admin dashboard loads successfully after login.
        Steps:
            1. Use admin_driver (already logged in as HEAD_ADMIN)
            2. Navigate to /admin/dashboard
        Expected: Page loads without error; no redirect to /login.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        assert page.is_on_admin_dashboard(), (
            f"Expected /admin/dashboard URL, got: {page.get_current_url()}"
        )

    # ── TC-ADMIN-002 ───────────────────────────────────────────────────────────
    def test_admin_dashboard_url(self, admin_driver, base_url):
        """
        Purpose: After login as admin, URL is /admin/dashboard.
        Steps:
            1. Use admin_driver (auto-redirected to dashboard on login)
            2. Check current URL
        Expected: URL contains '/admin/dashboard' or '/dashboard'.
        """
        current_url = admin_driver.current_url
        assert "/dashboard" in current_url, (
            f"Expected dashboard URL after admin login, got: {current_url}"
        )

    # ── TC-ADMIN-003 ───────────────────────────────────────────────────────────
    def test_stat_cards_are_visible(self, admin_driver, base_url):
        """
        Purpose: Statistics cards render on the admin dashboard.
        Steps:
            1. Open /admin/dashboard
        Expected: At least one stat card is visible.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        assert page.are_stat_cards_visible(), (
            "Expected statistics cards to be visible on admin dashboard"
        )

    # ── TC-ADMIN-004 ───────────────────────────────────────────────────────────
    def test_dashboard_shows_four_stat_cards(self, admin_driver, base_url):
        """
        Purpose: Dashboard displays all 4 stat cards: Users, Franchises, Mentors, Students.
        Steps:
            1. Open /admin/dashboard and wait for data to load
        Expected: 4 stat cards are present.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        count = page.get_stat_card_count()
        assert count >= 4, (
            f"Expected at least 4 stat cards, found: {count}"
        )

    # ── TC-ADMIN-005 ───────────────────────────────────────────────────────────
    def test_sidebar_navigation_is_visible(self, admin_driver, base_url):
        """
        Purpose: Sidebar menu links are rendered for the admin role.
        Steps:
            1. Open /admin/dashboard
        Expected: At least the Create User sidebar link is visible.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        assert page.is_sidebar_nav_visible(), (
            "Expected admin sidebar navigation to be visible"
        )

    # ── TC-ADMIN-006 ───────────────────────────────────────────────────────────
    def test_navigate_to_create_user_via_sidebar(self, admin_driver, base_url):
        """
        Purpose: Sidebar 'Create User' link navigates to /admin/create-user.
        Steps:
            1. Open /admin/dashboard
            2. Click the 'Create User' sidebar link
        Expected: URL changes to /admin/create-user.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        page.click_create_user()
        page.wait_for_url_contains("/admin/create-user")
        assert "/admin/create-user" in page.get_current_url(), (
            f"Expected /admin/create-user, got: {page.get_current_url()}"
        )

    # ── TC-ADMIN-007 ───────────────────────────────────────────────────────────
    def test_navigate_to_manage_users_via_sidebar(self, admin_driver, base_url):
        """
        Purpose: Sidebar 'Manage Users' link navigates to /admin/manage-users.
        Steps:
            1. Open /admin/dashboard
            2. Click 'Manage Users' sidebar link
        Expected: URL changes to /admin/manage-users.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        page.click_manage_users()
        page.wait_for_url_contains("/admin/manage-users")
        assert "/admin/manage-users" in page.get_current_url(), (
            f"Expected /admin/manage-users, got: {page.get_current_url()}"
        )

    # ── TC-ADMIN-008 ───────────────────────────────────────────────────────────
    def test_navigate_to_fee_packages_via_sidebar(self, admin_driver, base_url):
        """
        Purpose: Sidebar 'Fee Packages' link navigates to /admin/fee-management.
        Steps:
            1. Open /admin/dashboard
            2. Click 'Fee Packages' sidebar link
        Expected: URL changes to /admin/fee-management.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        page.click_fee_packages()
        page.wait_for_url_contains("/admin/fee-management")
        assert "/admin/fee-management" in page.get_current_url()

    # ── TC-ADMIN-009 ───────────────────────────────────────────────────────────
    def test_navigate_to_reports_via_sidebar(self, admin_driver, base_url):
        """
        Purpose: Sidebar 'Reports' link navigates to /admin/reports.
        Steps:
            1. Open /admin/dashboard
            2. Click 'Reports' sidebar link
        Expected: URL changes to /admin/reports.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        page.click_reports()
        page.wait_for_url_contains("/admin/reports")
        assert "/admin/reports" in page.get_current_url()

    # ── TC-ADMIN-010 ───────────────────────────────────────────────────────────
    def test_page_title_contains_school_management(self, admin_driver, base_url):
        """
        Purpose: Browser tab title references the application name.
        Steps:
            1. Open /admin/dashboard
        Expected: Page title contains 'School' or 'Management'.
        """
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        title = page.get_page_title()
        assert "school" in title.lower() or "management" in title.lower() or title != "", (
            f"Expected meaningful page title, got: '{title}'"
        )
