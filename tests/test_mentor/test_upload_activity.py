import pytest
from pages.mentor.upload_activity_page import UploadActivityPage


@pytest.mark.mentor
@pytest.mark.regression
class TestMentorUploadActivity:
    """Tests for the Mentor Upload Activity page (/mentor/upload-activity)."""

    # TC-UA-001
    def test_upload_activity_page_loads(self, mentor_driver, base_url):
        """Upload Activity page should load for mentor."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_on_upload_activity_page()

    # TC-UA-002
    def test_title_input_visible(self, mentor_driver, base_url):
        """Title input should be visible."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_form_visible()

    # TC-UA-003
    def test_description_field_visible(self, mentor_driver, base_url):
        """Description field should be visible."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.DESCRIPTION_INPUT)

    # TC-UA-004
    def test_file_input_present(self, mentor_driver, base_url):
        """File upload input should be present."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_file_input_present()

    # TC-UA-005
    def test_submit_button_visible(self, mentor_driver, base_url):
        """Submit button should be visible."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.SUBMIT_BTN)

    # TC-UA-006
    def test_empty_title_shows_error(self, mentor_driver, base_url):
        """Submitting without title should show an error."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        page.enter_description("Test description without title")
        page.click_submit()
        assert page.is_error_visible()

    # TC-UA-007
    def test_empty_description_shows_error(self, mentor_driver, base_url):
        """Submitting without description should show an error."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        page.enter_title("Test Activity Title")
        page.click_submit()
        assert page.is_error_visible()

    # TC-UA-008
    def test_visibility_checkboxes_present(self, mentor_driver, base_url):
        """Visibility checkboxes for parents and students should be present."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.CB_PARENTS)
        assert page.is_element_visible(page.CB_STUDENTS)

    # TC-UA-009
    def test_file_category_select_visible(self, mentor_driver, base_url):
        """File category dropdown should be visible."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_element_visible(page.FILE_CATEGORY_SELECT)

    # TC-UA-010
    def test_activity_list_renders(self, mentor_driver, base_url):
        """Page should load without crashing."""
        page = UploadActivityPage(mentor_driver, base_url)
        page.open()
        assert page.is_on_upload_activity_page()
        assert "cannot read" not in mentor_driver.page_source.lower()
