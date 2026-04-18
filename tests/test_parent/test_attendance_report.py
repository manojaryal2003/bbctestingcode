import pytest
from pages.parent.attendance_report_page import AttendanceReportPage


@pytest.mark.parent
@pytest.mark.regression
class TestParentAttendanceReport:
    """Tests for the Parent Attendance Report page (/parent/attendance-report)."""

    # TC-PAR-001
    def test_attendance_report_page_loads(self, parent_driver, base_url):
        """Attendance Report page should load for parent."""
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        assert page.is_on_attendance_report_page()

    # TC-PAR-002
    def test_attendance_table_renders(self, parent_driver, base_url):
        """Attendance table should be visible."""
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        assert page.is_attendance_table_visible()

    # TC-PAR-003
    def test_page_url_is_correct(self, parent_driver, base_url):
        """URL should contain /parent/attendance-report."""
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        assert "/parent/attendance-report" in page.get_current_url()

    # TC-PAR-004
    def test_page_does_not_crash(self, parent_driver, base_url):
        """Page should load without JS errors."""
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        source = parent_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source

    # TC-PAR-005
    def test_present_or_absent_labels_visible_if_records_exist(self, parent_driver, base_url):
        """If records exist, Present or Absent labels should be visible."""
        page = AttendanceReportPage(parent_driver, base_url)
        page.open()
        if page.get_row_count() > 0:
            assert page.are_present_records_shown() or page.is_element_visible(page.STATUS_ABSENT, timeout=3)
        else:
            pytest.skip("No attendance records to verify")
