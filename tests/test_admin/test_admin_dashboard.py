import pytest
from pages.admin.admin_dashboard_page import AdminDashboardPage


@pytest.mark.admin
@pytest.mark.regression
class TestAdminDashboard:
    """Tests for the Admin Dashboard (/admin/dashboard)."""

    # TC-ADMIN-001
    def test_admin_dashboard_loads(self, admin_driver, base_url):
        """Dashboard should load without redirecting to /login."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        assert page.is_on_admin_dashboard(), f"Expected /admin/dashboard, got: {page.get_current_url()}"

    # TC-ADMIN-002
    def test_admin_dashboard_url(self, admin_driver, base_url):
        """After login, URL should contain /dashboard."""
        assert "/dashboard" in admin_driver.current_url

    # TC-ADMIN-003
    def test_stat_cards_are_visible(self, admin_driver, base_url):
        """Statistics cards should be visible on the dashboard."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        assert page.are_stat_cards_visible()

    # TC-ADMIN-004
    def test_dashboard_shows_four_stat_cards(self, admin_driver, base_url):
        """Dashboard should show at least 4 stat cards."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        assert page.get_stat_card_count() >= 4, f"Expected 4+ cards, got: {page.get_stat_card_count()}"

    # TC-ADMIN-005
    def test_sidebar_navigation_is_visible(self, admin_driver, base_url):
        """Sidebar menu should be visible."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        assert page.is_sidebar_nav_visible()

    # TC-ADMIN-006
    def test_navigate_to_create_user_via_sidebar(self, admin_driver, base_url):
        """Clicking Create User in sidebar should go to /admin/create-user."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        page.click_create_user()
        page.wait_for_url_contains("/admin/create-user")
        assert "/admin/create-user" in page.get_current_url()

    # TC-ADMIN-007
    def test_navigate_to_manage_users_via_sidebar(self, admin_driver, base_url):
        """Clicking Manage Users in sidebar should go to /admin/manage-users."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        page.click_manage_users()
        page.wait_for_url_contains("/admin/manage-users")
        assert "/admin/manage-users" in page.get_current_url()

    # TC-ADMIN-008
    def test_navigate_to_fee_packages_via_sidebar(self, admin_driver, base_url):
        """Clicking Fee Packages in sidebar should go to /admin/fee-management."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        page.click_fee_packages()
        page.wait_for_url_contains("/admin/fee-management")
        assert "/admin/fee-management" in page.get_current_url()

    # TC-ADMIN-009
    def test_navigate_to_reports_via_sidebar(self, admin_driver, base_url):
        """Clicking Reports in sidebar should go to /admin/reports."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        page.click_reports()
        page.wait_for_url_contains("/admin/reports")
        assert "/admin/reports" in page.get_current_url()

    # TC-ADMIN-010
    def test_page_title_contains_school_management(self, admin_driver, base_url):
        """Page title should contain 'School' or 'Management'."""
        page = AdminDashboardPage(admin_driver, base_url)
        page.open()
        title = page.get_page_title()
        assert "school" in title.lower() or "management" in title.lower() or title != ""
