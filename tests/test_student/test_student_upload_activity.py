import pytest
from pages.student.student_upload_activity_page import StudentUploadActivityPage


@pytest.mark.student
@pytest.mark.regression
class TestStudentUploadActivity:
    """Tests for the Student Upload Activity page (/student/upload-activity)."""

    # TC-SUA-001
    def test_upload_activity_page_loads(self, student_driver, base_url):
        """Upload Activity page should load for student."""
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_on_upload_activity_page()

    # TC-SUA-002
    def test_title_input_visible(self, student_driver, base_url):
        """Title input should be visible."""
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_form_visible()

    # TC-SUA-003
    def test_description_field_visible(self, student_driver, base_url):
        """Description field should be visible."""
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.DESC_INPUT)

    # TC-SUA-004
    def test_file_input_present(self, student_driver, base_url):
        """File upload input should be present."""
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.FILE_INPUT)

    # TC-SUA-005
    def test_submit_button_visible(self, student_driver, base_url):
        """Submit button should be visible."""
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.SUBMIT_BTN)

    # TC-SUA-006
    def test_submit_without_title_shows_error(self, student_driver, base_url):
        """Submitting without title should show an error."""
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        page.enter_description("Test description without title")
        page.click_submit()
        assert page.is_error_visible()

    # TC-SUA-007
    def test_page_does_not_crash(self, student_driver, base_url):
        """Page should load without JS errors."""
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        source = student_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source
