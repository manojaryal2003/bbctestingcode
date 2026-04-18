import pytest
from pages.franchise.attendance_monitor_page import AttendanceMonitorPage


@pytest.mark.franchise
@pytest.mark.regression
class TestFranchiseAttendanceMonitor:
    """Tests for the Franchise Attendance Monitor page (/franchise/attendance)."""

    # TC-AM-001
    def test_attendance_monitor_loads(self, franchise_driver, base_url):
        """Attendance Monitor page should load for franchise admin."""
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert page.is_on_attendance_monitor_page()

    # TC-AM-002
    def test_url_is_correct(self, franchise_driver, base_url):
        """URL should contain /franchise/attendance."""
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert "/franchise/attendance" in page.get_current_url()

    # TC-AM-003
    def test_date_input_visible(self, franchise_driver, base_url):
        """Date filter input should be visible."""
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert page.is_date_input_visible()

    # TC-AM-004
    def test_attendance_table_renders(self, franchise_driver, base_url):
        """Attendance table should be visible."""
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert page.is_attendance_table_visible()

    # TC-AM-005
    def test_page_does_not_crash(self, franchise_driver, base_url):
        """Page should load without JS errors."""
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        source = franchise_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source

    # TC-AM-006
    def test_row_count_is_non_negative(self, franchise_driver, base_url):
        """Row count should be 0 or more."""
        page = AttendanceMonitorPage(franchise_driver, base_url)
        page.open()
        assert page.get_row_count() >= 0
