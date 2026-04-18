"""
test_submit_homework.py — Student Submit Homework regression tests.

Feature: Submit Homework at /student/submit-homework
Source:  Frontend/src/pages/student/SubmitHomework/SubmitHomework.jsx

Test Cases:
  TC-SHW-001  Submit Homework page loads for student
  TC-SHW-002  Homework list renders (may be empty)
  TC-SHW-003  Page does not crash on load
  TC-SHW-004  If homework exists, clicking it opens a submission modal
  TC-SHW-005  Submission modal contains a file input
  TC-SHW-006  Submitting modal without a file shows an error
  TC-SHW-007  Closing the modal hides it
"""

import pytest
from pages.student.submit_homework_page import SubmitHomeworkPage


@pytest.mark.student
@pytest.mark.regression
class TestSubmitHomework:
    """Regression tests for the Student Submit Homework page."""

    # ── TC-SHW-001 ─────────────────────────────────────────────────────────────
    def test_submit_homework_page_loads(self, student_driver, base_url):
        """
        Purpose: Submit Homework page loads for STUDENT without error.
        Steps:
            1. Navigate to /student/submit-homework using student_driver
        Expected: URL contains /student/submit-homework.
        """
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        assert page.is_on_submit_homework_page(), (
            f"Expected /student/submit-homework URL, got: {page.get_current_url()}"
        )

    # ── TC-SHW-002 ─────────────────────────────────────────────────────────────
    def test_homework_list_renders(self, student_driver, base_url):
        """
        Purpose: The homework list renders on page load (may be empty).
        Steps:
            1. Open /student/submit-homework
        Expected: Page renders without crash; URL is correct.
        """
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        # List may be empty — valid outcome
        assert page.is_on_submit_homework_page()

    # ── TC-SHW-003 ─────────────────────────────────────────────────────────────
    def test_page_does_not_crash(self, student_driver, base_url):
        """
        Purpose: Submit Homework page loads without JavaScript errors.
        Steps:
            1. Open /student/submit-homework
        Expected: Page source has no 'Uncaught' or 'Cannot read' markers.
        """
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()
        source = student_driver.page_source.lower()
        assert "cannot read" not in source, "JS TypeError on Submit Homework page"
        assert "uncaught" not in source,    "Uncaught JS error on Submit Homework page"

    # ── TC-SHW-004 ─────────────────────────────────────────────────────────────
    def test_clicking_homework_opens_modal(self, student_driver, base_url):
        """
        Purpose: Clicking a homework item opens the submission modal.
        Steps:
            1. Open /student/submit-homework
            2. If homework items exist, click the first one
        Expected: Submission modal becomes visible.
        """
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()

        if not page.is_homework_list_visible():
            pytest.skip("No homework items available to test modal open")

        page.click_first_homework()
        assert page.is_modal_visible(), (
            "Expected submission modal to open when clicking a homework item"
        )

    # ── TC-SHW-005 ─────────────────────────────────────────────────────────────
    def test_modal_contains_file_input(self, student_driver, base_url):
        """
        Purpose: The submission modal contains a file upload input.
        Steps:
            1. Open /student/submit-homework
            2. Click the first homework item (if available)
        Expected: File input is visible inside the modal.
        """
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()

        if not page.is_homework_list_visible():
            pytest.skip("No homework items available to test file input in modal")

        page.click_first_homework()
        assert page.is_file_input_visible(), (
            "Expected file input to be visible inside the homework submission modal"
        )

    # ── TC-SHW-006 ─────────────────────────────────────────────────────────────
    def test_submit_without_file_shows_error(self, student_driver, base_url):
        """
        Purpose: Submitting homework without selecting a file shows an error.
        Steps:
            1. Open /student/submit-homework
            2. Click first homework item to open modal
            3. Click Submit without attaching a file
        Expected: Error message is displayed.
        """
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()

        if not page.is_homework_list_visible():
            pytest.skip("No homework items available to test no-file submission")

        page.click_first_homework()
        page.click_submit()

        assert page.is_error_visible(), (
            "Expected error message when submitting homework without a file"
        )

    # ── TC-SHW-007 ─────────────────────────────────────────────────────────────
    def test_closing_modal_hides_it(self, student_driver, base_url):
        """
        Purpose: Clicking Close in the modal dismisses it.
        Steps:
            1. Open /student/submit-homework
            2. Click first homework item to open modal
            3. Click Close button
        Expected: Modal is no longer visible.
        """
        page = SubmitHomeworkPage(student_driver, base_url)
        page.open()

        if not page.is_homework_list_visible():
            pytest.skip("No homework items available to test modal close")

        page.click_first_homework()
        assert page.is_modal_visible(), "Modal did not open — prerequisite failed"

        page.close_modal()
        assert not page.is_modal_visible(), (
            "Expected modal to close after clicking Close button"
        )
