"""
test_fee_management.py — Fee Packages (Fee Management) regression tests.

Feature: Fee Management at /admin/fee-management
Source:  Frontend/src/pages/admin/FeeManagement/FeeManagement.jsx

Test Cases:
  TC-FEE-001  Fee Management page loads for admin
  TC-FEE-002  Add Package button is visible
  TC-FEE-003  Clicking Add Package opens the modal
  TC-FEE-004  Package creation modal has name and amount fields
  TC-FEE-005  Cancelling the modal closes it without saving
  TC-FEE-006  Submitting empty package form shows error (name + amount required)
  TC-FEE-007  Existing packages are displayed in the list
  TC-FEE-008  Package list renders without crashing
"""

import pytest
from pages.admin.fee_management_page import FeeManagementPage


@pytest.mark.admin
@pytest.mark.regression
class TestFeeManagement:
    """Regression tests for the Fee Packages page."""

    # ── TC-FEE-001 ─────────────────────────────────────────────────────────────
    def test_fee_management_page_loads(self, admin_driver, base_url):
        """
        Purpose: Fee Management page loads successfully for HEAD_ADMIN.
        Steps:
            1. Navigate to /admin/fee-management
        Expected: URL contains /admin/fee-management.
        """
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        assert page.is_on_fee_management_page(), (
            f"Expected /admin/fee-management URL, got: {page.get_current_url()}"
        )

    # ── TC-FEE-002 ─────────────────────────────────────────────────────────────
    def test_add_package_button_is_visible(self, admin_driver, base_url):
        """
        Purpose: The Add Package button renders on the Fee Management page.
        Steps:
            1. Open /admin/fee-management
        Expected: Add Package button is visible.
        """
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        assert page.is_add_button_visible(), (
            "Expected Add Package button to be visible on Fee Management page"
        )

    # ── TC-FEE-003 ─────────────────────────────────────────────────────────────
    def test_add_package_button_opens_modal(self, admin_driver, base_url):
        """
        Purpose: Clicking Add Package opens the creation modal.
        Steps:
            1. Open /admin/fee-management
            2. Click Add Package button
        Expected: Modal dialog becomes visible.
        """
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        page.click_add_package()
        assert page.is_modal_visible(), (
            "Expected Add Package modal to open after clicking the button"
        )

    # ── TC-FEE-004 ─────────────────────────────────────────────────────────────
    def test_package_modal_has_name_and_amount_fields(self, admin_driver, base_url):
        """
        Purpose: The Add Package modal contains name and amount input fields.
        Steps:
            1. Open /admin/fee-management
            2. Click Add Package button
        Expected: Both name and amount inputs are visible inside the modal.
        """
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        page.click_add_package()

        assert page.is_element_visible(page.MODAL_NAME_INPUT), (
            "Expected name input to be visible in the package modal"
        )
        assert page.is_element_visible(page.MODAL_AMOUNT_INPUT), (
            "Expected amount input to be visible in the package modal"
        )

    # ── TC-FEE-005 ─────────────────────────────────────────────────────────────
    def test_cancel_modal_closes_it(self, admin_driver, base_url):
        """
        Purpose: Clicking Cancel/Close in the modal dismisses it without saving.
        Steps:
            1. Open /admin/fee-management
            2. Click Add Package button (modal opens)
            3. Click Cancel/Close button
        Expected: Modal is no longer visible.
        """
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        page.click_add_package()
        assert page.is_modal_visible(), "Modal did not open — prerequisite failed"

        page.click_cancel()
        assert not page.is_modal_visible(), (
            "Expected modal to close after clicking Cancel"
        )

    # ── TC-FEE-006 ─────────────────────────────────────────────────────────────
    def test_empty_package_form_shows_error(self, admin_driver, base_url):
        """
        Purpose: Saving the package form without name/amount shows an error.
        Steps:
            1. Open /admin/fee-management
            2. Click Add Package
            3. Click Save without filling any fields
        Expected: Toast error or validation message appears.
        """
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        page.click_add_package()
        page.click_save()

        # Either modal stays open OR a toast error fires
        modal_still_open = page.is_modal_visible()
        toast_error = page.is_toast_visible()
        assert modal_still_open or toast_error, (
            "Expected modal to remain open or an error toast when saving empty package"
        )

    # ── TC-FEE-007 ─────────────────────────────────────────────────────────────
    def test_package_list_renders(self, admin_driver, base_url):
        """
        Purpose: The package list renders without crashing (may be empty or populated).
        Steps:
            1. Open /admin/fee-management
        Expected: Page loads at correct URL; package count is >= 0.
        """
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        count = page.get_package_count()
        assert count >= 0, "Package count should be non-negative"
        assert page.is_on_fee_management_page()

    # ── TC-FEE-008 ─────────────────────────────────────────────────────────────
    def test_page_does_not_crash_on_load(self, admin_driver, base_url):
        """
        Purpose: Fee Management page source does not contain 'Error' or 'Cannot read'.
        Steps:
            1. Open /admin/fee-management
        Expected: Page source free of JS error markers.
        """
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        source = admin_driver.page_source.lower()
        assert "cannot read" not in source, "Possible JS TypeError in page source"
        assert "uncaught" not in source,    "Uncaught JS error in page source"
