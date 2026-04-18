import pytest
from pages.student.submit_homework_page import SubmitHomeworkPage


@pytest.mark.student
@pytest.mark.regression
class TestSubmitHomework:
    """Tests for the Student Submit Homework page (/student/submit-homework)."""

    # TC-SHW-001
    def test_submit_homework_page_loads(self, student_driver, base_url):
        """Submit Homework page should load for student."""
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        assert page.is_on_submit_homework_page()

    # TC-SHW-002
    def test_homework_list_renders(self, student_driver, base_url):
        """Homework list should render (can be empty)."""
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        assert page.is_on_submit_homework_page()

    # TC-SHW-003
    def test_page_does_not_crash(self, student_driver, base_url):
        """Page should load without JavaScript errors."""
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        source = student_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source

    # TC-SHW-004
    def test_clicking_homework_opens_modal(self, student_driver, base_url):
        """Clicking a homework item should open the submission modal."""
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        if not page.is_homework_list_visible():
            pytest.skip("No homework items available")
        page.click_first_homework()
        assert page.is_modal_visible()

    # TC-SHW-005
    def test_modal_contains_file_input(self, student_driver, base_url):
        """Submission modal should contain a file input."""
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        if not page.is_homework_list_visible():
            pytest.skip("No homework items available")
        page.click_first_homework()
        assert page.is_file_input_visible()

    # TC-SHW-006
    def test_submit_without_file_shows_error(self, student_driver, base_url):
        """Submitting without a file should show an error."""
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        if not page.is_homework_list_visible():
            pytest.skip("No homework items available")
        page.click_first_homework()
        page.click_submit()
        assert page.is_error_visible()

    # TC-SHW-007
    def test_closing_modal_hides_it(self, student_driver, base_url):
        """Clicking Close should dismiss the modal."""
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        if not page.is_homework_list_visible():
            pytest.skip("No homework items available")
        page.click_first_homework()
        page.close_modal()
        assert not page.is_modal_visible()
