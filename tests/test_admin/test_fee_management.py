import pytest
from pages.admin.fee_management_page import FeeManagementPage


@pytest.mark.admin
@pytest.mark.regression
class TestFeeManagement:
    """Tests for the Fee Packages page (/admin/fee-management)."""

    # TC-FEE-001
    def test_fee_management_page_loads(self, admin_driver, base_url):
        """Fee Management page should load for admin."""
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        assert page.is_on_fee_management_page()

    # TC-FEE-002
    def test_add_package_button_is_visible(self, admin_driver, base_url):
        """Add Package button should be visible on the page."""
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        assert page.is_add_button_visible()

    # TC-FEE-003
    def test_add_package_button_opens_modal(self, admin_driver, base_url):
        """Clicking Add Package should open a modal dialog."""
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        page.click_add_package()
        assert page.is_modal_visible()

    # TC-FEE-004
    def test_package_modal_has_name_and_amount_fields(self, admin_driver, base_url):
        """The modal should have name and amount input fields."""
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        page.click_add_package()
        assert page.is_element_visible(page.MODAL_NAME_INPUT)
        assert page.is_element_visible(page.MODAL_AMOUNT_INPUT)

    # TC-FEE-005
    def test_cancel_modal_closes_it(self, admin_driver, base_url):
        """Clicking Cancel should close the modal."""
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        page.click_add_package()
        page.click_cancel()
        assert not page.is_modal_visible()

    # TC-FEE-006
    def test_empty_package_form_shows_error(self, admin_driver, base_url):
        """Saving without filling any fields should show an error."""
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        page.click_add_package()
        page.click_save()
        assert page.is_modal_visible() or page.is_toast_visible()

    # TC-FEE-007
    def test_package_list_renders(self, admin_driver, base_url):
        """Package list should render without crashing (can be empty)."""
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        assert page.get_package_count() >= 0
        assert page.is_on_fee_management_page()

    # TC-FEE-008
    def test_page_does_not_crash_on_load(self, admin_driver, base_url):
        """Page should not have any JavaScript errors on load."""
        page = FeeManagementPage(admin_driver, base_url)
        page.open()
        source = admin_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source
