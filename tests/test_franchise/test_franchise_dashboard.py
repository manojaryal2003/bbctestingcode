import time
import pytest
from pages.franchise.franchise_dashboard_page import FranchiseDashboardPage


@pytest.mark.franchise
@pytest.mark.regression
class TestFranchiseDashboard:
    """Tests for the Franchise Admin Dashboard (/franchise/dashboard)."""

    # TC-FD-001
    def test_franchise_dashboard_loads(self, franchise_driver, base_url):
        """Dashboard should load after login."""
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.is_on_franchise_dashboard()

    # TC-FD-002
    def test_franchise_url_after_login(self, franchise_driver, base_url):
        """URL after login should contain /franchise or /dashboard."""
        assert "/franchise" in franchise_driver.current_url or "/dashboard" in franchise_driver.current_url

    # TC-FD-003
    def test_stat_cards_render(self, franchise_driver, base_url):
        """Stat cards should be visible on the dashboard."""
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.are_stat_cards_visible()

    # TC-FD-004
    def test_dashboard_shows_stat_cards(self, franchise_driver, base_url):
        """Dashboard should show at least 1 stat card."""
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.get_stat_card_count() >= 1

    # TC-FD-005
    def test_sidebar_visible(self, franchise_driver, base_url):
        """Sidebar should be visible."""
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.is_sidebar_visible()

    # TC-FD-006
    def test_attendance_monitor_link_visible(self, franchise_driver, base_url):
        """Attendance Monitor link should be visible in the sidebar."""
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_ATTENDANCE)

    # TC-FD-007
    def test_attendance_monitor_navigates(self, franchise_driver, base_url):
        """Clicking Attendance Monitor should go to /franchise/attendance."""
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        page.click_attendance_monitor()
        page.wait_for_url_contains("/franchise/attendance")
        assert "/franchise/attendance" in page.get_current_url()

    # TC-FD-008
    def test_payment_proofs_link_visible(self, franchise_driver, base_url):
        """Payment Proofs link should be visible."""
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_PAYMENT_PROOF)

    # TC-FD-009
    def test_franchise_admin_cannot_access_head_admin_routes(self, franchise_driver, base_url):
        """Franchise admin should not access /admin/create-user."""
        franchise_driver.get(f"{base_url}/admin/create-user")
        time.sleep(2)
        assert "/admin/create-user" not in franchise_driver.current_url

    # TC-FD-010
    def test_page_does_not_crash(self, franchise_driver, base_url):
        """Page should load without JS errors."""
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        source = franchise_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source
