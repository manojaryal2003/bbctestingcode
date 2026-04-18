import time
import pytest
from pages.student.student_dashboard_page import StudentDashboardPage


@pytest.mark.student
@pytest.mark.regression
class TestStudentDashboard:
    """Tests for the Student Dashboard (/student/dashboard)."""

    # TC-SD-001
    def test_student_dashboard_loads(self, student_driver, base_url):
        """Dashboard should load after login."""
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_on_student_dashboard()

    # TC-SD-002
    def test_student_url_after_login(self, student_driver, base_url):
        """URL after login should contain /student or /dashboard."""
        assert "/student" in student_driver.current_url or "/dashboard" in student_driver.current_url

    # TC-SD-003
    def test_submit_homework_link_visible(self, student_driver, base_url):
        """Submit Homework sidebar link should be visible."""
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_sidebar_visible()

    # TC-SD-004
    def test_upload_activity_link_visible(self, student_driver, base_url):
        """Upload Activity link should be visible."""
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_UPLOAD_ACTIVITY)

    # TC-SD-005
    def test_badges_link_visible(self, student_driver, base_url):
        """Badges link should be visible."""
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_BADGES)

    # TC-SD-006
    def test_progress_link_visible(self, student_driver, base_url):
        """My Progress link should be visible."""
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_PROGRESS)

    # TC-SD-007
    def test_submit_homework_navigates(self, student_driver, base_url):
        """Clicking Submit Homework should go to /student/submit-homework."""
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        page.click_submit_homework()
        page.wait_for_url_contains("/student/submit-homework")
        assert "/student/submit-homework" in page.get_current_url()

    # TC-SD-008
    def test_upload_activity_navigates(self, student_driver, base_url):
        """Clicking Upload Activity should go to /student/upload-activity."""
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        page.click_upload_activity()
        page.wait_for_url_contains("/student/upload-activity")
        assert "/student/upload-activity" in page.get_current_url()

    # TC-SD-009
    def test_badges_link_navigates(self, student_driver, base_url):
        """Clicking Badges should go to /student/badges."""
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        page.click_badges()
        page.wait_for_url_contains("/student/badges")
        assert "/student/badges" in page.get_current_url()

    # TC-SD-010
    def test_student_cannot_access_admin(self, student_driver, base_url):
        """Student should not have access to /admin/dashboard."""
        student_driver.get(f"{base_url}/admin/dashboard")
        time.sleep(2)
        assert "/admin/dashboard" not in student_driver.current_url
