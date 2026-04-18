import pytest
from pages.mentor.homework_management_page import HomeworkManagementPage


@pytest.mark.mentor
@pytest.mark.regression
class TestMentorHomeworkManagement:
    """Tests for Mentor Send Homework and Homework Management pages."""

    # TC-HW-001
    def test_send_homework_page_loads(self, mentor_driver, base_url):
        """Send Homework page should load for mentor."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_on_send_homework_page()

    # TC-HW-002
    def test_title_input_visible(self, mentor_driver, base_url):
        """Title input should be visible on Send Homework."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_form_visible()

    # TC-HW-003
    def test_description_field_visible(self, mentor_driver, base_url):
        """Description field should be visible."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_element_visible(page.DESC_INPUT)

    # TC-HW-004
    def test_due_date_input_visible(self, mentor_driver, base_url):
        """Due date input should be visible."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_element_visible(page.DUE_DATE_INPUT)

    # TC-HW-005
    def test_submit_button_visible(self, mentor_driver, base_url):
        """Submit button should be visible."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_element_visible(page.SUBMIT_BTN)

    # TC-HW-006
    def test_submit_without_title_shows_error(self, mentor_driver, base_url):
        """Submitting without title should show an error."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        page.enter_description("Some description without a title")
        page.click_submit()
        assert page.is_error_visible()

    # TC-HW-007
    def test_submit_without_description_shows_error(self, mentor_driver, base_url):
        """Submitting without description should show an error."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        page.enter_title("Homework Without Description")
        page.click_submit()
        assert page.is_error_visible()

    # TC-HW-008
    def test_homework_management_page_loads(self, mentor_driver, base_url):
        """Homework Management page should load for mentor."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_homework_management()
        assert page.is_on_homework_management_page()

    # TC-HW-009
    def test_homework_list_renders_on_send_page(self, mentor_driver, base_url):
        """Send Homework page should load without crashing."""
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_on_send_homework_page()
        assert "cannot read" not in mentor_driver.page_source.lower()
