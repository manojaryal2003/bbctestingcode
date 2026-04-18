"""
test_attendance_monitor.py — Franchise Attendance Monitor regression tests.

Feature: Franchise Attendance Monitor at /franchise/attendance
Source:  Frontend/src/pages/franchise/AttendanceMonitor/AttendanceMonitor.jsx

Test Cases:
  TC-AM-001  Attendance Monitor page loads for franchise admin
  TC-AM-002  URL is correct
  TC-AM-003  Date input is visible
  TC-AM-004  Attendance table/list renders
  TC-AM-005  Page does not crash on load
  TC-AM-006  Row count is non-negative
"""

import pytest
from pages.franchise.attendance_monitor_page import AttendanceMonitorPage


@pytest.mark.franchise
@pytest.mark.regression
class TestFranchiseAttendanceMonitor:
    """Regression tests for the Franchise Attendance Monitor page."""

    # ── TC-AM-001 ──────────────────────────────────────────────────────────────
    def test_attendance_monitor_loads(self, franchise_driver, base_url):
        """
        Purpose: Attendance Monitor page loads for FRANCHISE_ADMIN.
        Steps:
            1. Navigate to /franchise/attendance
        Expected: URL contains /franchise/attendance.
        """
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert page.is_on_attendance_monitor_page(), (
            f"Expected /franchise/attendance URL, got: {page.get_current_url()}"
        )

    # ── TC-AM-002 ──────────────────────────────────────────────────────────────
    def test_url_is_correct(self, franchise_driver, base_url):
        """
        Purpose: Browser URL is correct for Attendance Monitor.
        Steps:
            1. Open /franchise/attendance
        Expected: URL contains '/franchise/attendance'.
        """
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert "/franchise/attendance" in page.get_current_url()

    # ── TC-AM-003 ──────────────────────────────────────────────────────────────
    def test_date_input_visible(self, franchise_driver, base_url):
        """
        Purpose: A date filter input is visible on the Attendance Monitor.
        Steps:
            1. Open /franchise/attendance
        Expected: Date input (type='date') is visible.
        """
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert page.is_date_input_visible(), (
            "Expected date filter input to be visible on Attendance Monitor"
        )

    # ── TC-AM-004 ──────────────────────────────────────────────────────────────
    def test_attendance_table_renders(self, franchise_driver, base_url):
        """
        Purpose: Attendance table or list container renders on the page.
        Steps:
            1. Open /franchise/attendance
        Expected: Attendance table/list is visible.
        """
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert page.is_attendance_table_visible(), (
            "Expected attendance table/list to render on Attendance Monitor"
        )

    # ── TC-AM-005 ──────────────────────────────────────────────────────────────
    def test_page_does_not_crash(self, franchise_driver, base_url):
        """
        Purpose: Attendance Monitor page loads without JS errors.
        Steps:
            1. Open /franchise/attendance
        Expected: No 'Uncaught' or 'Cannot read' in page source.
        """
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        source = franchise_driver.page_source.lower()
        assert "cannot read" not in source, "JS TypeError on Attendance Monitor"
        assert "uncaught" not in source,    "Uncaught JS error on Attendance Monitor"

    # ── TC-AM-006 ──────────────────────────────────────────────────────────────
    def test_row_count_is_non_negative(self, franchise_driver, base_url):
        """
        Purpose: Row count returned is a valid non-negative integer.
        Steps:
            1. Open /franchise/attendance
            2. Count attendance rows
        Expected: Count is 0 or greater.
        """
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        count = page.get_row_count()
        assert count >= 0, f"Expected non-negative row count, got: {count}"
