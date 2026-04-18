"""
test_parent_dashboard.py — Parent Dashboard regression tests.

Feature: Parent Dashboard at /parent/dashboard
Source:  Frontend/src/pages/parent/ParentDashboard/ParentDashboard.jsx

Test Cases:
  TC-PD-001  Parent dashboard loads after login
  TC-PD-002  URL contains /parent/dashboard
  TC-PD-003  Sidebar is visible with parent-specific links
  TC-PD-004  Fee Status link is visible
  TC-PD-005  Homework link is visible
  TC-PD-006  Attendance link is visible
  TC-PD-007  Messages link is visible
  TC-PD-008  Clicking Attendance navigates to /parent/attendance-report
  TC-PD-009  Clicking Fee Status navigates to /parent/fee-status
  TC-PD-010  Parent cannot access admin routes
"""

import pytest
from pages.parent.parent_dashboard_page import ParentDashboardPage


@pytest.mark.parent
@pytest.mark.regression
class TestParentDashboard:
    """Regression tests for the Parent Dashboard page."""

    # ── TC-PD-001 ──────────────────────────────────────────────────────────────
    def test_parent_dashboard_loads(self, parent_driver, base_url):
        """
        Purpose: Parent dashboard loads after login.
        Steps:
            1. Use parent_driver (logged in as PARENT)
            2. Open /parent/dashboard
        Expected: URL contains /parent/dashboard.
        """
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_on_parent_dashboard(), (
            f"Expected /parent/dashboard URL, got: {page.get_current_url()}"
        )

    # ── TC-PD-002 ──────────────────────────────────────────────────────────────
    def test_parent_url_after_login(self, parent_driver, base_url):
        """
        Purpose: URL after parent login contains /parent or /dashboard.
        Steps:
            1. Check current URL of parent_driver
        Expected: URL contains '/parent' or '/dashboard'.
        """
        current_url = parent_driver.current_url
        assert "/parent" in current_url or "/dashboard" in current_url, (
            f"Expected parent dashboard URL after login, got: {current_url}"
        )

    # ── TC-PD-003 ──────────────────────────────────────────────────────────────
    def test_sidebar_visible_for_parent(self, parent_driver, base_url):
        """
        Purpose: Sidebar renders with parent-specific navigation.
        Steps:
            1. Open /parent/dashboard
        Expected: Sidebar with Fee Status link is visible.
        """
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_sidebar_visible(), (
            "Expected parent sidebar to be visible"
        )

    # ── TC-PD-004 ──────────────────────────────────────────────────────────────
    def test_fee_status_link_visible(self, parent_driver, base_url):
        """
        Purpose: Fee Status sidebar link renders for PARENT role.
        Steps:
            1. Open /parent/dashboard
        Expected: Fee Status link is visible.
        """
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_FEE_STATUS), (
            "Expected Fee Status link to be visible in parent sidebar"
        )

    # ── TC-PD-005 ──────────────────────────────────────────────────────────────
    def test_homework_link_visible(self, parent_driver, base_url):
        """
        Purpose: Homework sidebar link renders for PARENT role.
        Steps:
            1. Open /parent/dashboard
        Expected: Homework link is visible.
        """
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_HOMEWORK), (
            "Expected Homework link to be visible in parent sidebar"
        )

    # ── TC-PD-006 ──────────────────────────────────────────────────────────────
    def test_attendance_link_visible(self, parent_driver, base_url):
        """
        Purpose: Attendance sidebar link renders for PARENT role.
        Steps:
            1. Open /parent/dashboard
        Expected: Attendance link is visible.
        """
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_ATTENDANCE), (
            "Expected Attendance link to be visible in parent sidebar"
        )

    # ── TC-PD-007 ──────────────────────────────────────────────────────────────
    def test_messages_link_visible(self, parent_driver, base_url):
        """
        Purpose: Notice/Messages sidebar link renders for PARENT role.
        Steps:
            1. Open /parent/dashboard
        Expected: Messages link is visible.
        """
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_MESSAGES), (
            "Expected Messages link to be visible in parent sidebar"
        )

    # ── TC-PD-008 ──────────────────────────────────────────────────────────────
    def test_attendance_link_navigates(self, parent_driver, base_url):
        """
        Purpose: Clicking Attendance navigates to /parent/attendance-report.
        Steps:
            1. Open /parent/dashboard
            2. Click Attendance sidebar link
        Expected: URL changes to /parent/attendance-report.
        """
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        page.click_attendance_from_sidebar()
        page.wait_for_url_contains("/parent/attendance-report")
        assert "/parent/attendance-report" in page.get_current_url()

    # ── TC-PD-009 ──────────────────────────────────────────────────────────────
    def test_fee_status_link_navigates(self, parent_driver, base_url):
        """
        Purpose: Clicking Fee Status navigates to /parent/fee-status.
        Steps:
            1. Open /parent/dashboard
            2. Click Fee Status sidebar link
        Expected: URL changes to /parent/fee-status.
        """
        page = ParentDashboardPage(parent_driver, base_url)
        page.open()
        page.click_fee_status_from_sidebar()
        page.wait_for_url_contains("/parent/fee-status")
        assert "/parent/fee-status" in page.get_current_url()

    # ── TC-PD-010 ──────────────────────────────────────────────────────────────
    def test_parent_cannot_access_admin(self, parent_driver, base_url):
        """
        Purpose: PARENT cannot access /admin/dashboard.
        Steps:
            1. Navigate to /admin/dashboard using parent_driver
        Expected: Redirected away from /admin/dashboard.
        """
        import time
        parent_driver.get(f"{base_url}/admin/dashboard")
        time.sleep(2)
        current = parent_driver.current_url
        assert "/admin/dashboard" not in current, (
            f"PARENT should not access /admin/dashboard, got: {current}"
        )
