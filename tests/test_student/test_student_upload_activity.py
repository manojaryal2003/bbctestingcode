"""
test_student_upload_activity.py — Student Upload Activity regression tests.

Feature: Student Upload Activity at /student/upload-activity
Source:  Frontend/src/pages/student/UploadActivity/UploadActivity.jsx

Test Cases:
  TC-SUA-001  Student Upload Activity page loads
  TC-SUA-002  Title input is visible
  TC-SUA-003  Description field is visible
  TC-SUA-004  File input is present
  TC-SUA-005  Submit button is visible
  TC-SUA-006  Submitting without title shows error
  TC-SUA-007  Page does not crash on load
"""

import pytest
from pages.student.student_upload_activity_page import StudentUploadActivityPage


@pytest.mark.student
@pytest.mark.regression
class TestStudentUploadActivity:
    """Regression tests for the Student Upload Activity page."""

    # ── TC-SUA-001 ─────────────────────────────────────────────────────────────
    def test_upload_activity_page_loads(self, student_driver, base_url):
        """
        Purpose: Student Upload Activity page loads without error.
        Steps:
            1. Navigate to /student/upload-activity
        Expected: URL contains /student/upload-activity.
        """
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_on_upload_activity_page(), (
            f"Expected /student/upload-activity, got: {page.get_current_url()}"
        )

    # ── TC-SUA-002 ─────────────────────────────────────────────────────────────
    def test_title_input_visible(self, student_driver, base_url):
        """
        Purpose: Title input is rendered on the upload form.
        Steps:
            1. Open /student/upload-activity
        Expected: Title input is visible.
        """
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_form_visible(), (
            "Expected title input to be visible on Student Upload Activity"
        )

    # ── TC-SUA-003 ─────────────────────────────────────────────────────────────
    def test_description_field_visible(self, student_driver, base_url):
        """
        Purpose: Description field is rendered.
        Steps:
            1. Open /student/upload-activity
        Expected: Description field is visible.
        """
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.DESC_INPUT), (
            "Expected description field to be visible"
        )

    # ── TC-SUA-004 ─────────────────────────────────────────────────────────────
    def test_file_input_present(self, student_driver, base_url):
        """
        Purpose: File upload input is present on the form.
        Steps:
            1. Open /student/upload-activity
        Expected: File input is visible.
        """
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.FILE_INPUT), (
            "Expected file input to be visible"
        )

    # ── TC-SUA-005 ─────────────────────────────────────────────────────────────
    def test_submit_button_visible(self, student_driver, base_url):
        """
        Purpose: Submit button is rendered on the form.
        Steps:
            1. Open /student/upload-activity
        Expected: Submit button is visible.
        """
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        assert page.is_element_visible(page.SUBMIT_BTN), (
            "Expected submit button to be visible"
        )

    # ── TC-SUA-006 ─────────────────────────────────────────────────────────────
    def test_submit_without_title_shows_error(self, student_driver, base_url):
        """
        Purpose: Submitting without a title shows an error.
        Steps:
            1. Open /student/upload-activity
            2. Enter description, leave title blank
            3. Click Submit
        Expected: Error message is visible.
        """
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        page.enter_description("Test description without title")
        page.click_submit()

        assert page.is_error_visible(), (
            "Expected error when submitting student activity without title"
        )

    # ── TC-SUA-007 ─────────────────────────────────────────────────────────────
    def test_page_does_not_crash(self, student_driver, base_url):
        """
        Purpose: Page loads without JS errors.
        Steps:
            1. Open /student/upload-activity
        Expected: No 'Uncaught' or 'Cannot read' in page source.
        """
        page = StudentUploadActivityPage(student_driver, base_url)
        page.open()
        source = student_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source
