import pytest
from datetime import date
from pages.mentor.attendance_page import AttendancePage


@pytest.mark.mentor
@pytest.mark.regression
class TestMentorAttendance:
    """Tests for the Mentor Attendance page (/mentor/attendance)."""

    # TC-ATT-001
    def test_attendance_page_loads(self, mentor_driver, base_url):
        """Attendance page should load for mentor."""
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_on_attendance_page()

    # TC-ATT-002
    def test_mark_attendance_tab_visible(self, mentor_driver, base_url):
        """Mark Attendance tab should be visible."""
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_mark_tab_visible()

    # TC-ATT-003
    def test_report_tab_visible(self, mentor_driver, base_url):
        """Attendance Report tab should be visible."""
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_report_tab_visible()

    # TC-ATT-004
    def test_date_input_visible_on_mark_tab(self, mentor_driver, base_url):
        """Date input should be visible on the Mark Attendance tab."""
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_date_input_visible()

    # TC-ATT-005
    def test_date_input_defaults_to_today(self, mentor_driver, base_url):
        """Date input should default to today's date."""
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        today = date.today().strftime("%Y-%m-%d")
        date_value = page.get_element_attribute(page.DATE_INPUT, "value")
        assert date_value == today, f"Expected today ({today}), got: '{date_value}'"

    # TC-ATT-006
    def test_clicking_report_tab_switches_view(self, mentor_driver, base_url):
        """Clicking Report tab should stay on /mentor/attendance."""
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        page.click_report_tab()
        assert page.is_on_attendance_page()

    # TC-ATT-007
    def test_save_button_visible_on_mark_tab(self, mentor_driver, base_url):
        """Save Attendance button should be visible."""
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.SAVE_BTN)

    # TC-ATT-008
    def test_page_does_not_crash_on_load(self, mentor_driver, base_url):
        """Page should load without JavaScript errors."""
        page = AttendancePage(mentor_driver, base_url)
        page.open()
        source = mentor_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source
