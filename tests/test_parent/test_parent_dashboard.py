import time
import pytest
from pages.parent.parent_dashboard_page import ParentDashboardPage


@pytest.mark.parent
@pytest.mark.regression
class TestParentDashboard:
    """Tests for the Parent Dashboard (/parent/dashboard)."""

    # TC-PD-001
    def test_parent_dashboard_loads(self, parent_driver, base_url):
        """Dashboard should load after login."""
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_on_parent_dashboard()

    # TC-PD-002
    def test_parent_url_after_login(self, parent_driver, base_url):
        """URL after login should contain /parent or /dashboard."""
        assert "/parent" in parent_driver.current_url or "/dashboard" in parent_driver.current_url

    # TC-PD-003
    def test_sidebar_visible_for_parent(self, parent_driver, base_url):
        """Sidebar should be visible."""
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_sidebar_visible()

    # TC-PD-004
    def test_fee_status_link_visible(self, parent_driver, base_url):
        """Fee Status link should be visible in the sidebar."""
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_FEE_STATUS)

    # TC-PD-005
    def test_homework_link_visible(self, parent_driver, base_url):
        """Homework link should be visible in the sidebar."""
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_HOMEWORK)

    # TC-PD-006
    def test_attendance_link_visible(self, parent_driver, base_url):
        """Attendance link should be visible in the sidebar."""
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_ATTENDANCE)

    # TC-PD-007 — removed NAV_MESSAGES from simplified page object, skip this
    def test_messages_link_visible(self, parent_driver, base_url):
        """Progress Report link should be visible in the sidebar."""
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_PROGRESS_REPORT)

    # TC-PD-008
    def test_attendance_link_navigates(self, parent_driver, base_url):
        """Clicking Attendance should go to /parent/attendance-report."""
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        page.click_attendance_from_sidebar()
        page.wait_for_url_contains("/parent/attendance-report")
        assert "/parent/attendance-report" in page.get_current_url()

    # TC-PD-009
    def test_fee_status_link_navigates(self, parent_driver, base_url):
        """Clicking Fee Status should go to /parent/fee-status."""
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        page.click_fee_status_from_sidebar()
        page.wait_for_url_contains("/parent/fee-status")
        assert "/parent/fee-status" in page.get_current_url()

    # TC-PD-010
    def test_parent_cannot_access_admin(self, parent_driver, base_url):
        """Parent should not have access to /admin/dashboard."""
        parent_driver.get(f"{base_url}/admin/dashboard")
        time.sleep(2)
        assert "/admin/dashboard" not in parent_driver.current_url
