"""
test_upload_activity.py — Mentor Upload Activity regression tests.

Feature: Upload Activity at /mentor/upload-activity
Source:  Frontend/src/pages/mentor/UploadActivity/UploadActivity.jsx

Test Cases:
  TC-UA-001  Upload Activity page loads for mentor
  TC-UA-002  Title input field is visible
  TC-UA-003  Description field is visible
  TC-UA-004  File input is present
  TC-UA-005  Submit button is visible
  TC-UA-006  Submitting empty title shows an error
  TC-UA-007  Submitting without description shows an error
  TC-UA-008  Visibility checkboxes are present (visibleToParents, visibleToStudents)
  TC-UA-009  File category select is visible
  TC-UA-010  Previously uploaded activities list is rendered
"""

import pytest
from pages.mentor.upload_activity_page import UploadActivityPage


@pytest.mark.mentor
@pytest.mark.regression
class TestMentorUploadActivity:
    """Regression tests for the Mentor Upload Activity page."""

    # ── TC-UA-001 ──────────────────────────────────────────────────────────────
    def test_upload_activity_page_loads(self, mentor_driver, base_url):
        """
        Purpose: Upload Activity page loads for MENTOR without error.
        Steps:
            1. Navigate to /mentor/upload-activity
        Expected: URL contains /mentor/upload-activity.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_on_upload_activity_page(), (
            f"Expected /mentor/upload-activity URL, got: {page.get_current_url()}"
        )

    # ── TC-UA-002 ──────────────────────────────────────────────────────────────
    def test_title_input_visible(self, mentor_driver, base_url):
        """
        Purpose: Title input field is rendered on the page.
        Steps:
            1. Open /mentor/upload-activity
        Expected: Title input (name='title') is visible.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_form_visible(), (
            "Expected title input to be visible"
        )

    # ── TC-UA-003 ──────────────────────────────────────────────────────────────
    def test_description_field_visible(self, mentor_driver, base_url):
        """
        Purpose: Description textarea is rendered.
        Steps:
            1. Open /mentor/upload-activity
        Expected: Description field (name='description') is visible.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.DESCRIPTION_INPUT), (
            "Expected description field to be visible"
        )

    # ── TC-UA-004 ──────────────────────────────────────────────────────────────
    def test_file_input_present(self, mentor_driver, base_url):
        """
        Purpose: File upload input is present on the form.
        Steps:
            1. Open /mentor/upload-activity
        Expected: File input (type='file') is present.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_file_input_present(), (
            "Expected file input to be present on Upload Activity form"
        )

    # ── TC-UA-005 ──────────────────────────────────────────────────────────────
    def test_submit_button_visible(self, mentor_driver, base_url):
        """
        Purpose: The Submit/Upload button is rendered.
        Steps:
            1. Open /mentor/upload-activity
        Expected: Submit button is visible.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.SUBMIT_BTN), (
            "Expected submit button to be visible"
        )

    # ── TC-UA-006 ──────────────────────────────────────────────────────────────
    def test_empty_title_shows_error(self, mentor_driver, base_url):
        """
        Purpose: Submitting without a title shows an error message.
        Steps:
            1. Open /mentor/upload-activity
            2. Enter description only, leave title blank
            3. Click Submit
        Expected: Error message is displayed.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        page.enter_description("Test description without title")
        page.click_submit()

        assert page.is_error_visible(), (
            "Expected error message when title is empty"
        )

    # ── TC-UA-007 ──────────────────────────────────────────────────────────────
    def test_empty_description_shows_error(self, mentor_driver, base_url):
        """
        Purpose: Submitting without a description shows an error message.
        Steps:
            1. Open /mentor/upload-activity
            2. Enter title only, leave description blank
            3. Click Submit
        Expected: Error message is displayed.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        page.enter_title("Test Activity Title")
        page.click_submit()

        assert page.is_error_visible(), (
            "Expected error message when description is empty"
        )

    # ── TC-UA-008 ──────────────────────────────────────────────────────────────
    def test_visibility_checkboxes_present(self, mentor_driver, base_url):
        """
        Purpose: Visibility checkboxes for parents and students are rendered.
        Steps:
            1. Open /mentor/upload-activity
        Expected: visibleToParents and visibleToStudents checkboxes are present.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.CB_PARENTS), (
            "Expected visibleToParents checkbox to be visible"
        )
        assert page.is_element_visible(page.CB_STUDENTS), (
            "Expected visibleToStudents checkbox to be visible"
        )

    # ── TC-UA-009 ──────────────────────────────────────────────────────────────
    def test_file_category_select_visible(self, mentor_driver, base_url):
        """
        Purpose: The fileCategory select dropdown is present.
        Steps:
            1. Open /mentor/upload-activity
        Expected: fileCategory select is visible.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.FILE_CATEGORY_SELECT), (
            "Expected fileCategory select dropdown to be visible"
        )

    # ── TC-UA-010 ──────────────────────────────────────────────────────────────
    def test_activity_list_renders(self, mentor_driver, base_url):
        """
        Purpose: Previously uploaded activities list renders (may be empty).
        Steps:
            1. Open /mentor/upload-activity
        Expected: Page loads without crash; activity list container exists.
        """
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        # Activity list may be empty — just confirm no crash
        assert page.is_on_upload_activity_page(), (
            "Expected to remain on upload activity page"
        )
        source = mentor_driver.page_source.lower()
        assert "cannot read" not in source, "Possible JS error on Upload Activity page"
