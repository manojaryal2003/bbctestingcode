"""
test_student_dashboard.py — Student Dashboard regression tests.

Feature: Student Dashboard at /student/dashboard
Source:  Frontend/src/pages/student/StudentDashboard/StudentDashboard.jsx
         Frontend/src/components/layout/Sidebar/Sidebar.jsx (STUDENT section)

Test Cases:
  TC-SD-001  Student dashboard loads after login
  TC-SD-002  URL contains /student/dashboard
  TC-SD-003  Submit Homework sidebar link is visible
  TC-SD-004  Upload Activity sidebar link is visible
  TC-SD-005  Badges sidebar link is visible
  TC-SD-006  My Progress sidebar link is visible
  TC-SD-007  Clicking Submit Homework navigates correctly
  TC-SD-008  Clicking Upload Activity navigates correctly
  TC-SD-009  Clicking Badges navigates to /student/badges
  TC-SD-010  Student cannot access admin routes
"""

import pytest
from pages.student.student_dashboard_page import StudentDashboardPage


@pytest.mark.student
@pytest.mark.regression
class TestStudentDashboard:
    """Regression tests for the Student Dashboard."""

    # ── TC-SD-001 ──────────────────────────────────────────────────────────────
    def test_student_dashboard_loads(self, student_driver, base_url):
        """
        Purpose: Student dashboard loads successfully after login.
        Steps:
            1. Use student_driver (already logged in as STUDENT)
            2. Open /student/dashboard
        Expected: URL contains /student/dashboard.
        """
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_on_student_dashboard(), (
            f"Expected /student/dashboard URL, got: {page.get_current_url()}"
        )

    # ── TC-SD-002 ──────────────────────────────────────────────────────────────
    def test_student_url_after_login(self, student_driver, base_url):
        """
        Purpose: URL after student login contains /student or /dashboard.
        Steps:
            1. Check current URL of student_driver (auto-redirected post-login)
        Expected: URL contains '/student' or '/dashboard'.
        """
        current_url = student_driver.current_url
        assert "/student" in current_url or "/dashboard" in current_url, (
            f"Expected student dashboard URL after login, got: {current_url}"
        )

    # ── TC-SD-003 ──────────────────────────────────────────────────────────────
    def test_submit_homework_link_visible(self, student_driver, base_url):
        """
        Purpose: Submit Homework sidebar link is visible for STUDENT.
        Steps:
            1. Open /student/dashboard
        Expected: Submit Homework link is visible.
        """
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_sidebar_visible(), (
            "Expected Submit Homework sidebar link to be visible"
        )

    # ── TC-SD-004 ──────────────────────────────────────────────────────────────
    def test_upload_activity_link_visible(self, student_driver, base_url):
        """
        Purpose: Upload Activity sidebar link is visible.
        Steps:
            1. Open /student/dashboard
        Expected: Upload Activity link is visible.
        """
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_UPLOAD_ACTIVITY), (
            "Expected Upload Activity link to be visible"
        )

    # ── TC-SD-005 ──────────────────────────────────────────────────────────────
    def test_badges_link_visible(self, student_driver, base_url):
        """
        Purpose: Badges sidebar link is visible for STUDENT.
        Steps:
            1. Open /student/dashboard
        Expected: Badges link is visible.
        """
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_BADGES), (
            "Expected Badges sidebar link to be visible"
        )

    # ── TC-SD-006 ──────────────────────────────────────────────────────────────
    def test_progress_link_visible(self, student_driver, base_url):
        """
        Purpose: My Progress sidebar link is visible for STUDENT.
        Steps:
            1. Open /student/dashboard
        Expected: My Progress link is visible.
        """
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_PROGRESS), (
            "Expected My Progress sidebar link to be visible"
        )

    # ── TC-SD-007 ──────────────────────────────────────────────────────────────
    def test_submit_homework_navigates(self, student_driver, base_url):
        """
        Purpose: Clicking Submit Homework navigates to /student/submit-homework.
        Steps:
            1. Open /student/dashboard
            2. Click Submit Homework
        Expected: URL changes to /student/submit-homework.
        """
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        page.click_submit_homework()
        page.wait_for_url_contains("/student/submit-homework")
        assert "/student/submit-homework" in page.get_current_url()

    # ── TC-SD-008 ──────────────────────────────────────────────────────────────
    def test_upload_activity_navigates(self, student_driver, base_url):
        """
        Purpose: Clicking Upload Activity navigates to /student/upload-activity.
        Steps:
            1. Open /student/dashboard
            2. Click Upload Activity
        Expected: URL changes to /student/upload-activity.
        """
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        page.click_upload_activity()
        page.wait_for_url_contains("/student/upload-activity")
        assert "/student/upload-activity" in page.get_current_url()

    # ── TC-SD-009 ──────────────────────────────────────────────────────────────
    def test_badges_link_navigates(self, student_driver, base_url):
        """
        Purpose: Clicking Badges navigates to /student/badges.
        Steps:
            1. Open /student/dashboard
            2. Click Badges
        Expected: URL changes to /student/badges.
        """
        page = StudentDashboardPage(student_driver, base_url)
        page.open()
        page.click_badges()
        page.wait_for_url_contains("/student/badges")
        assert "/student/badges" in page.get_current_url()

    # ── TC-SD-010 ──────────────────────────────────────────────────────────────
    def test_student_cannot_access_admin(self, student_driver, base_url):
        """
        Purpose: STUDENT cannot access /admin/dashboard.
        Steps:
            1. Navigate directly to /admin/dashboard using student_driver
        Expected: Redirected away from /admin/dashboard.
        """
        import time
        student_driver.get(f"{base_url}/admin/dashboard")
        time.sleep(2)
        current = student_driver.current_url
        assert "/admin/dashboard" not in current, (
            f"STUDENT should not access /admin/dashboard, but URL is: {current}"
        )
