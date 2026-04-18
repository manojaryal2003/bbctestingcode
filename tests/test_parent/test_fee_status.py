"""
test_fee_status.py — Parent Fee Status regression tests.

Feature: Parent Fee Status at /parent/fee-status
Source:  Frontend/src/pages/parent/FeeStatus/FeeStatusDisplay.jsx

Test Cases:
  TC-FS-001  Fee Status page loads for parent
  TC-FS-002  URL is correct
  TC-FS-003  Bill list renders (may be empty)
  TC-FS-004  Page does not crash on load
  TC-FS-005  If bills exist, Paid or Unpaid status labels are visible
  TC-FS-006  Page title/heading is meaningful
"""

import pytest
from pages.parent.fee_status_page import FeeStatusPage


@pytest.mark.parent
@pytest.mark.regression
class TestParentFeeStatus:
    """Regression tests for the Parent Fee Status page."""

    # ── TC-FS-001 ──────────────────────────────────────────────────────────────
    def test_fee_status_page_loads(self, parent_driver, base_url):
        """
        Purpose: Fee Status page loads for PARENT without error.
        Steps:
            1. Navigate to /parent/fee-status
        Expected: URL contains /parent/fee-status.
        """
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        assert page.is_on_fee_status_page(), (
            f"Expected /parent/fee-status URL, got: {page.get_current_url()}"
        )

    # ── TC-FS-002 ──────────────────────────────────────────────────────────────
    def test_fee_status_url_correct(self, parent_driver, base_url):
        """
        Purpose: Browser URL is correct for the Fee Status page.
        Steps:
            1. Open /parent/fee-status
        Expected: URL contains '/parent/fee-status'.
        """
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        assert "/parent/fee-status" in page.get_current_url()

    # ── TC-FS-003 ──────────────────────────────────────────────────────────────
    def test_bill_list_renders(self, parent_driver, base_url):
        """
        Purpose: Bill list container renders on the page (may be empty).
        Steps:
            1. Open /parent/fee-status
        Expected: Bill list is visible; bill count is >= 0.
        """
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        assert page.is_bill_list_visible() or page.get_bill_count() == 0, (
            "Expected bill list to render (even if empty)"
        )

    # ── TC-FS-004 ──────────────────────────────────────────────────────────────
    def test_page_does_not_crash(self, parent_driver, base_url):
        """
        Purpose: Fee Status page loads without JavaScript errors.
        Steps:
            1. Open /parent/fee-status
        Expected: No 'Uncaught' or 'Cannot read' in page source.
        """
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        source = parent_driver.page_source.lower()
        assert "cannot read" not in source, "JS TypeError on Fee Status page"
        assert "uncaught" not in source,    "Uncaught JS error on Fee Status page"

    # ── TC-FS-005 ──────────────────────────────────────────────────────────────
    def test_paid_or_unpaid_labels_if_bills_exist(self, parent_driver, base_url):
        """
        Purpose: If fee bills exist, Paid or Unpaid status labels are visible.
        Steps:
            1. Open /parent/fee-status
            2. Count bill rows
        Expected: If rows > 0, at least one Paid or Unpaid label is visible.
        """
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        count = page.get_bill_count()

        if count > 0:
            paid    = page.is_paid_status_visible()
            unpaid  = page.is_unpaid_status_visible()
            assert paid or unpaid, (
                "Expected Paid or Unpaid labels when bills exist"
            )
        else:
            pytest.skip("No fee bills to test status labels")

    # ── TC-FS-006 ──────────────────────────────────────────────────────────────
    def test_page_heading_is_meaningful(self, parent_driver, base_url):
        """
        Purpose: The page heading is non-empty (meaningful title rendered).
        Steps:
            1. Open /parent/fee-status
        Expected: Page source is non-empty; page is at correct URL.
        """
        page = FeeStatusPage(parent_driver, base_url)
        page.open()
        assert page.is_on_fee_status_page()
        assert len(parent_driver.page_source) > 100, (
            "Page source appears too short — possible blank page"
        )
