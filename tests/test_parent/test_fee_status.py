import pytest
from pages.parent.fee_status_page import FeeStatusPage


@pytest.mark.parent
@pytest.mark.regression
class TestParentFeeStatus:
    """Tests for the Parent Fee Status page (/parent/fee-status)."""

    # TC-FS-001
    def test_fee_status_page_loads(self, parent_driver, base_url):
        """Fee Status page should load for parent."""
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        assert page.is_on_fee_status_page()

    # TC-FS-002
    def test_fee_status_url_correct(self, parent_driver, base_url):
        """URL should contain /parent/fee-status."""
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        assert "/parent/fee-status" in page.get_current_url()

    # TC-FS-003
    def test_bill_list_renders(self, parent_driver, base_url):
        """Bill list should render (can be empty)."""
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        assert page.is_bill_list_visible() or page.get_bill_count() == 0

    # TC-FS-004
    def test_page_does_not_crash(self, parent_driver, base_url):
        """Page should load without JS errors."""
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        source = parent_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source

    # TC-FS-005
    def test_paid_or_unpaid_labels_if_bills_exist(self, parent_driver, base_url):
        """If bills exist, Paid or Unpaid labels should be visible."""
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        if page.get_bill_count() > 0:
            assert page.is_paid_status_visible() or page.is_unpaid_status_visible()
        else:
            pytest.skip("No fee bills to verify status labels")

    # TC-FS-006
    def test_page_heading_is_meaningful(self, parent_driver, base_url):
        """Page should have meaningful content (not blank)."""
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        assert page.is_on_fee_status_page()
        assert len(parent_driver.page_source) > 100
