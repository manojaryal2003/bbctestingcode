"""
test_homework_management.py — Mentor Send Homework / Homework Management regression tests.

Feature: Send Homework at /mentor/send-homework
         Homework Management at /mentor/homework-management
Source:  Frontend/src/pages/mentor/SendHomework/SendHomework.jsx
         Frontend/src/pages/mentor/MentorTeacher/HomeworkManagement.jsx

Test Cases:
  TC-HW-001  Send Homework page loads for mentor
  TC-HW-002  Title input is visible
  TC-HW-003  Description field is visible
  TC-HW-004  Due date input is visible
  TC-HW-005  Submit button is visible
  TC-HW-006  Submitting without title shows error
  TC-HW-007  Submitting without description shows error
  TC-HW-008  Homework Management page loads for mentor
  TC-HW-009  Previously sent homework list renders on Send Homework page
"""

import pytest
from pages.mentor.homework_management_page import HomeworkManagementPage


@pytest.mark.mentor
@pytest.mark.regression
class TestMentorHomeworkManagement:
    """Regression tests for Mentor Send Homework and Homework Management."""

    # ── TC-HW-001 ──────────────────────────────────────────────────────────────
    def test_send_homework_page_loads(self, mentor_driver, base_url):
        """
        Purpose: Send Homework page loads for MENTOR without error.
        Steps:
            1. Navigate to /mentor/send-homework using mentor_driver
        Expected: URL contains /mentor/send-homework.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_on_send_homework_page(), (
            f"Expected /mentor/send-homework URL, got: {page.get_current_url()}"
        )

    # ── TC-HW-002 ──────────────────────────────────────────────────────────────
    def test_title_input_visible(self, mentor_driver, base_url):
        """
        Purpose: Title input field is rendered on the Send Homework form.
        Steps:
            1. Open /mentor/send-homework
        Expected: Title input is visible.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_form_visible(), (
            "Expected title input to be visible on Send Homework page"
        )

    # ── TC-HW-003 ──────────────────────────────────────────────────────────────
    def test_description_field_visible(self, mentor_driver, base_url):
        """
        Purpose: Description textarea is rendered.
        Steps:
            1. Open /mentor/send-homework
        Expected: Description field is visible.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_element_visible(page.DESC_INPUT), (
            "Expected description field to be visible"
        )

    # ── TC-HW-004 ──────────────────────────────────────────────────────────────
    def test_due_date_input_visible(self, mentor_driver, base_url):
        """
        Purpose: Due date input is present (confirmed as name='dueDate').
        Steps:
            1. Open /mentor/send-homework
        Expected: Due date input is visible.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_element_visible(page.DUE_DATE_INPUT), (
            "Expected due date input to be visible"
        )

    # ── TC-HW-005 ──────────────────────────────────────────────────────────────
    def test_submit_button_visible(self, mentor_driver, base_url):
        """
        Purpose: Submit button is rendered on the Send Homework form.
        Steps:
            1. Open /mentor/send-homework
        Expected: Submit button is visible.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_element_visible(page.SUBMIT_BTN), (
            "Expected Submit button to be visible on Send Homework form"
        )

    # ── TC-HW-006 ──────────────────────────────────────────────────────────────
    def test_submit_without_title_shows_error(self, mentor_driver, base_url):
        """
        Purpose: Submitting the form without a title shows an error.
        Steps:
            1. Open /mentor/send-homework
            2. Enter description only, leave title blank
            3. Click Submit
        Expected: Error message is displayed.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        page.enter_description("Some description without a title")
        page.click_submit()

        assert page.is_error_visible(), (
            "Expected error when submitting homework without a title"
        )

    # ── TC-HW-007 ──────────────────────────────────────────────────────────────
    def test_submit_without_description_shows_error(self, mentor_driver, base_url):
        """
        Purpose: Submitting the form without a description shows an error.
        Steps:
            1. Open /mentor/send-homework
            2. Enter title only, leave description blank
            3. Click Submit
        Expected: Error message is displayed.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        page.enter_title("Homework Without Description")
        page.click_submit()

        assert page.is_error_visible(), (
            "Expected error when submitting homework without a description"
        )

    # ── TC-HW-008 ──────────────────────────────────────────────────────────────
    def test_homework_management_page_loads(self, mentor_driver, base_url):
        """
        Purpose: Homework Management page loads for MENTOR.
        Steps:
            1. Navigate to /mentor/homework-management
        Expected: URL contains /mentor/homework-management.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_homework_management()
        assert page.is_on_homework_management_page(), (
            f"Expected /mentor/homework-management URL, got: {page.get_current_url()}"
        )

    # ── TC-HW-009 ──────────────────────────────────────────────────────────────
    def test_homework_list_renders_on_send_page(self, mentor_driver, base_url):
        """
        Purpose: The previously sent homework list renders (may be empty).
        Steps:
            1. Open /mentor/send-homework
        Expected: Page loads without crash; URL is correct.
        """
        page = HomeworkManagementPage(mentor_driver, base_url)
        page.open_send_homework()
        assert page.is_on_send_homework_page()
        source = mentor_driver.page_source.lower()
        assert "cannot read" not in source, "JS error on Send Homework page"
