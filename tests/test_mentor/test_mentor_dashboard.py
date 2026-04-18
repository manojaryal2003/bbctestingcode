import time
import pytest
from pages.mentor.mentor_dashboard_page import MentorDashboardPage


@pytest.mark.mentor
@pytest.mark.regression
class TestMentorDashboard:
    """Tests for the Mentor Dashboard (/mentor/dashboard)."""

    # TC-MD-001
    def test_mentor_dashboard_loads(self, mentor_driver, base_url):
        """Dashboard should load without error."""
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_on_mentor_dashboard()

    # TC-MD-002
    def test_mentor_dashboard_url_after_login(self, mentor_driver, base_url):
        """After login, URL should contain /mentor or /dashboard."""
        assert "/mentor" in mentor_driver.current_url or "/dashboard" in mentor_driver.current_url

    # TC-MD-003
    def test_sidebar_visible_for_mentor(self, mentor_driver, base_url):
        """Sidebar navigation should be visible."""
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_sidebar_visible()

    # TC-MD-004
    def test_attendance_link_visible(self, mentor_driver, base_url):
        """Attendance sidebar link should be visible."""
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_ATTENDANCE)

    # TC-MD-005
    def test_upload_activity_link_visible(self, mentor_driver, base_url):
        """Upload Activity sidebar link should be visible."""
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_UPLOAD_ACTIVITY)

    # TC-MD-006
    def test_homework_management_link_visible(self, mentor_driver, base_url):
        """Homework Management sidebar link should be visible."""
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_HOMEWORK_MGMT)

    # TC-MD-007
    def test_attendance_link_navigates_correctly(self, mentor_driver, base_url):
        """Clicking Attendance should go to /mentor/attendance."""
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        page.click_attendance()
        page.wait_for_url_contains("/mentor/attendance")
        assert "/mentor/attendance" in page.get_current_url()

    # TC-MD-008
    def test_upload_activity_link_navigates_correctly(self, mentor_driver, base_url):
        """Clicking Upload Activity should go to /mentor/upload-activity."""
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        page.click_upload_activity()
        page.wait_for_url_contains("/mentor/upload-activity")
        assert "/mentor/upload-activity" in page.get_current_url()

    # TC-MD-009
    def test_homework_management_link_navigates_correctly(self, mentor_driver, base_url):
        """Clicking Homework Management should go to /mentor/homework-management."""
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        page.click_homework_management()
        page.wait_for_url_contains("/mentor/homework-management")
        assert "/mentor/homework-management" in page.get_current_url()

    # TC-MD-010
    def test_mentor_cannot_access_admin_route(self, mentor_driver, base_url):
        """Mentor should not have access to /admin/dashboard."""
        mentor_driver.get(f"{base_url}/admin/dashboard")
        time.sleep(2)
        current = mentor_driver.current_url
        assert "/admin/dashboard" not in current or "/login" in current
