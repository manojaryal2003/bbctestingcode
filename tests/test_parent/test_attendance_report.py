"""
test_attendance_report.py — Parent Attendance Report regression tests.

Feature: Parent Attendance Report at /parent/attendance-report
Source:  Frontend/src/pages/parent/AttendanceReport/AttendanceReport.jsx

Test Cases:
  TC-PAR-001  Attendance Report page loads for parent
  TC-PAR-002  Attendance table or list renders
  TC-PAR-003  Page URL is correct
  TC-PAR-004  Page does not crash on load
  TC-PAR-005  If records exist, Present/Absent labels are shown
"""

import pytest
from pages.parent.attendance_report_page import AttendanceReportPage


@pytest.mark.parent
@pytest.mark.regression
class TestParentAttendanceReport:
    """Regression tests for the Parent Attendance Report page."""

    # ── TC-PAR-001 ─────────────────────────────────────────────────────────────
    def test_attendance_report_page_loads(self, parent_driver, base_url):
        """
        Purpose: Attendance Report page loads for PARENT without error.
        Steps:
            1. Navigate to /parent/attendance-report
        Expected: URL contains /parent/attendance-report.
        """
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        assert page.is_on_attendance_report_page(), (
            f"Expected /parent/attendance-report, got: {page.get_current_url()}"
        )

    # ── TC-PAR-002 ─────────────────────────────────────────────────────────────
    def test_attendance_table_renders(self, parent_driver, base_url):
        """
        Purpose: Attendance table or list container renders on the page.
        Steps:
            1. Open /parent/attendance-report
        Expected: Attendance table/list is visible.
        """
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        assert page.is_attendance_table_visible(), (
            "Expected attendance table/list to be visible"
        )

    # ── TC-PAR-003 ─────────────────────────────────────────────────────────────
    def test_page_url_is_correct(self, parent_driver, base_url):
        """
        Purpose: Browser URL is correct for the Attendance Report page.
        Steps:
            1. Open /parent/attendance-report
        Expected: URL contains '/parent/attendance-report'.
        """
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        assert "/parent/attendance-report" in page.get_current_url()

    # ── TC-PAR-004 ─────────────────────────────────────────────────────────────
    def test_page_does_not_crash(self, parent_driver, base_url):
        """
        Purpose: Attendance Report page loads without JS errors.
        Steps:
            1. Open /parent/attendance-report
        Expected: No 'Uncaught' or 'Cannot read' in page source.
        """
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        source = parent_driver.page_source.lower()
        assert "cannot read" not in source, "JS TypeError on Attendance Report page"
        assert "uncaught" not in source,    "Uncaught JS error on Attendance Report page"

    # ── TC-PAR-005 ─────────────────────────────────────────────────────────────
    def test_present_or_absent_labels_visible_if_records_exist(
            self, parent_driver, base_url):
        """
        Purpose: If attendance records exist, Present/Absent labels are displayed.
        Steps:
            1. Open /parent/attendance-report
            2. Check row count
        Expected: If rows > 0, either Present or Absent label is visible.
        """
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()

        row_count = page.get_row_count()
        if row_count > 0:
            present_visible = page.are_present_records_shown()
            absent_visible  = page.is_element_visible(page.STATUS_ABSENT, timeout=3)
            assert present_visible or absent_visible, (
                "Expected Present or Absent labels when attendance records exist"
            )
        else:
            pytest.skip("No attendance records to verify status labels")
