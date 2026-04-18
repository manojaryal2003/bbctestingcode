"""
test_attendance.py — Mentor Attendance page regression tests.

Feature: Mentor Attendance at /mentor/attendance
Source:  Frontend/src/pages/mentor/Attendance/Attendance.jsx

Test Cases:
  TC-ATT-001  Attendance page loads for mentor
  TC-ATT-002  Mark Attendance tab is visible
  TC-ATT-003  Attendance Report tab is visible
  TC-ATT-004  Date input is visible on Mark Attendance tab
  TC-ATT-005  Date input defaults to today's date
  TC-ATT-006  Clicking Report tab switches to report view
  TC-ATT-007  Save Attendance button is visible on Mark tab
  TC-ATT-008  Page does not crash on load
"""

import pytest
from datetime import date
from pages.mentor.attendance_page import AttendancePage


@pytest.mark.mentor
@pytest.mark.regression
class TestMentorAttendance:
    """Regression tests for the Mentor Attendance page."""

    # ── TC-ATT-001 ─────────────────────────────────────────────────────────────
    def test_attendance_page_loads(self, mentor_driver, base_url):
        """
        Purpose: Attendance page loads for MENTOR without error.
        Steps:
            1. Navigate to /mentor/attendance using mentor_driver
        Expected: URL contains /mentor/attendance.
        """
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_on_attendance_page(), (
            f"Expected /mentor/attendance URL, got: {page.get_current_url()}"
        )

    # ── TC-ATT-002 ─────────────────────────────────────────────────────────────
    def test_mark_attendance_tab_visible(self, mentor_driver, base_url):
        """
        Purpose: The Mark Attendance tab is rendered on the page.
        Steps:
            1. Open /mentor/attendance
        Expected: Mark Attendance tab button is visible.
        """
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_mark_tab_visible(), (
            "Expected 'Mark' tab button to be visible"
        )

    # ── TC-ATT-003 ─────────────────────────────────────────────────────────────
    def test_report_tab_visible(self, mentor_driver, base_url):
        """
        Purpose: The Attendance Report tab button is rendered.
        Steps:
            1. Open /mentor/attendance
        Expected: Report tab button is visible.
        """
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_report_tab_visible(), (
            "Expected 'Report' tab button to be visible"
        )

    # ── TC-ATT-004 ─────────────────────────────────────────────────────────────
    def test_date_input_visible_on_mark_tab(self, mentor_driver, base_url):
        """
        Purpose: A date input is visible on the Mark Attendance tab.
        Steps:
            1. Open /mentor/attendance
        Expected: Date picker input is visible.
        """
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_date_input_visible(), (
            "Expected date picker input to be visible on Mark Attendance tab"
        )

    # ── TC-ATT-005 ─────────────────────────────────────────────────────────────
    def test_date_input_defaults_to_today(self, mentor_driver, base_url):
        """
        Purpose: Date input defaults to today's date (from Attendance.jsx source).
        Steps:
            1. Open /mentor/attendance
            2. Read the value of the date input
        Expected: Date value equals today's date in YYYY-MM-DD format.
        """
        page = AttendancePage(mentor_driver, base_url)
        page.open()

        today = date.today().strftime("%Y-%m-%d")
        date_value = page.get_element_attribute(page.DATE_INPUT, "value")
        assert date_value == today, (
            f"Expected date input to default to today ({today}), got: '{date_value}'"
        )

    # ── TC-ATT-006 ─────────────────────────────────────────────────────────────
    def test_clicking_report_tab_switches_view(self, mentor_driver, base_url):
        """
        Purpose: Clicking the Report tab changes the view to the report section.
        Steps:
            1. Open /mentor/attendance
            2. Click the Report tab
        Expected: Page remains at /mentor/attendance; report-related elements appear.
        """
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        page.click_report_tab()
        assert page.is_on_attendance_page(), (
            "Expected to remain on /mentor/attendance after clicking Report tab"
        )

    # ── TC-ATT-007 ─────────────────────────────────────────────────────────────
    def test_save_button_visible_on_mark_tab(self, mentor_driver, base_url):
        """
        Purpose: The Save Attendance button is present on the Mark tab.
        Steps:
            1. Open /mentor/attendance
        Expected: Save Attendance button is visible.
        """
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.SAVE_BTN), (
            "Expected Save Attendance button to be visible"
        )

    # ── TC-ATT-008 ─────────────────────────────────────────────────────────────
    def test_page_does_not_crash_on_load(self, mentor_driver, base_url):
        """
        Purpose: Attendance page loads without JavaScript errors.
        Steps:
            1. Open /mentor/attendance
        Expected: Page source has no 'Uncaught' or 'Cannot read' error markers.
        """
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        source = mentor_driver.page_source.lower()
        assert "cannot read" not in source, "Possible JS TypeError on Attendance page"
        assert "uncaught" not in source,    "Uncaught JS error on Attendance page"
