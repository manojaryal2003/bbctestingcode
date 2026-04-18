"""
test_mentor_dashboard.py — Mentor Dashboard regression tests.

Feature: Mentor Dashboard at /mentor/dashboard
Source:  Frontend/src/pages/mentor/MentorDashboard/MentorDashboard.jsx
         Frontend/src/components/layout/Sidebar/Sidebar.jsx (MENTOR section)

Test Cases:
  TC-MD-001  Mentor dashboard loads after login
  TC-MD-002  URL is correct (/mentor/dashboard)
  TC-MD-003  Sidebar navigation is visible for Mentor role
  TC-MD-004  Attendance sidebar link is visible
  TC-MD-005  Upload Activity sidebar link is visible
  TC-MD-006  Homework Management sidebar link is visible
  TC-MD-007  Clicking Attendance navigates to /mentor/attendance
  TC-MD-008  Clicking Upload Activity navigates to /mentor/upload-activity
  TC-MD-009  Clicking Homework Management navigates to /mentor/homework-management
  TC-MD-010  Mentor cannot navigate to admin route
"""

import pytest
from pages.mentor.mentor_dashboard_page import MentorDashboardPage


@pytest.mark.mentor
@pytest.mark.regression
class TestMentorDashboard:
    """Regression tests for the Mentor Dashboard."""

    # ── TC-MD-001 ──────────────────────────────────────────────────────────────
    def test_mentor_dashboard_loads(self, mentor_driver, base_url):
        """
        Purpose: Mentor dashboard loads without error.
        Steps:
            1. Use mentor_driver (logged in as MENTOR)
            2. Open /mentor/dashboard
        Expected: URL contains /mentor/dashboard.
        """
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_on_mentor_dashboard(), (
            f"Expected /mentor/dashboard URL, got: {page.get_current_url()}"
        )

    # ── TC-MD-002 ──────────────────────────────────────────────────────────────
    def test_mentor_dashboard_url_after_login(self, mentor_driver, base_url):
        """
        Purpose: After mentor login, URL contains /mentor or /dashboard.
        Steps:
            1. Check current URL of mentor_driver (already redirected post-login)
        Expected: URL contains '/mentor' or '/dashboard'.
        """
        current_url = mentor_driver.current_url
        assert "/mentor" in current_url or "/dashboard" in current_url, (
            f"Expected mentor-related URL after login, got: {current_url}"
        )

    # ── TC-MD-003 ──────────────────────────────────────────────────────────────
    def test_sidebar_visible_for_mentor(self, mentor_driver, base_url):
        """
        Purpose: Sidebar navigation renders for the MENTOR role.
        Steps:
            1. Open /mentor/dashboard
        Expected: Attendance sidebar link is visible.
        """
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_sidebar_visible(), (
            "Expected mentor sidebar to be visible (Attendance link not found)"
        )

    # ── TC-MD-004 ──────────────────────────────────────────────────────────────
    def test_attendance_link_visible(self, mentor_driver, base_url):
        """
        Purpose: Attendance nav link renders in the MENTOR sidebar.
        Steps:
            1. Open /mentor/dashboard
        Expected: Attendance link (href=/mentor/attendance) is visible.
        """
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_ATTENDANCE), (
            "Expected Attendance sidebar link to be visible"
        )

    # ── TC-MD-005 ──────────────────────────────────────────────────────────────
    def test_upload_activity_link_visible(self, mentor_driver, base_url):
        """
        Purpose: Upload Activity nav link renders in the MENTOR sidebar.
        Steps:
            1. Open /mentor/dashboard
        Expected: Upload Activity link is visible.
        """
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_UPLOAD_ACTIVITY), (
            "Expected Upload Activity sidebar link to be visible"
        )

    # ── TC-MD-006 ──────────────────────────────────────────────────────────────
    def test_homework_management_link_visible(self, mentor_driver, base_url):
        """
        Purpose: Homework Management nav link renders in the MENTOR sidebar.
        Steps:
            1. Open /mentor/dashboard
        Expected: Homework Management link is visible.
        """
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_HOMEWORK_MGMT), (
            "Expected Homework Management sidebar link to be visible"
        )

    # ── TC-MD-007 ──────────────────────────────────────────────────────────────
    def test_attendance_link_navigates_correctly(self, mentor_driver, base_url):
        """
        Purpose: Clicking the Attendance sidebar link navigates to /mentor/attendance.
        Steps:
            1. Open /mentor/dashboard
            2. Click Attendance
        Expected: URL changes to /mentor/attendance.
        """
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        page.click_attendance()
        page.wait_for_url_contains("/mentor/attendance")
        assert "/mentor/attendance" in page.get_current_url()

    # ── TC-MD-008 ──────────────────────────────────────────────────────────────
    def test_upload_activity_link_navigates_correctly(self, mentor_driver, base_url):
        """
        Purpose: Clicking Upload Activity navigates to /mentor/upload-activity.
        Steps:
            1. Open /mentor/dashboard
            2. Click Upload Activity
        Expected: URL changes to /mentor/upload-activity.
        """
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        page.click_upload_activity()
        page.wait_for_url_contains("/mentor/upload-activity")
        assert "/mentor/upload-activity" in page.get_current_url()

    # ── TC-MD-009 ──────────────────────────────────────────────────────────────
    def test_homework_management_link_navigates_correctly(self, mentor_driver, base_url):
        """
        Purpose: Clicking Homework Management navigates to /mentor/homework-management.
        Steps:
            1. Open /mentor/dashboard
            2. Click Homework Management
        Expected: URL changes to /mentor/homework-management.
        """
        page = MentorDashboardPage(mentor_driver, base_url)
        page.open()
        page.click_homework_management()
        page.wait_for_url_contains("/mentor/homework-management")
        assert "/mentor/homework-management" in page.get_current_url()

    # ── TC-MD-010 ──────────────────────────────────────────────────────────────
    def test_mentor_cannot_access_admin_route(self, mentor_driver, base_url):
        """
        Purpose: MENTOR is denied access to /admin/dashboard.
        Steps:
            1. Use mentor_driver (logged in as MENTOR)
            2. Navigate directly to /admin/dashboard
        Expected: Redirected away (not left on /admin/dashboard).
        """
        import time
        mentor_driver.get(f"{base_url}/admin/dashboard")
        time.sleep(2)
        current = mentor_driver.current_url
        assert "/admin/dashboard" not in current or "/login" in current, (
            f"Mentor should NOT have access to /admin/dashboard, but stayed at: {current}"
        )
