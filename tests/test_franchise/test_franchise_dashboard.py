"""
test_franchise_dashboard.py — Franchise Admin Dashboard regression tests.

Feature: Franchise Dashboard at /franchise/dashboard
Source:  Frontend/src/pages/franchise/FranchiseDashboard/FranchiseDashboard.jsx

Test Cases:
  TC-FD-001  Franchise dashboard loads after login
  TC-FD-002  URL contains /franchise/dashboard
  TC-FD-003  Stat cards render (Total Students, Total Mentors, Attendance Rate)
  TC-FD-004  Dashboard shows at least one stat card
  TC-FD-005  Sidebar is visible
  TC-FD-006  Attendance Monitor sidebar link is visible
  TC-FD-007  Clicking Attendance Monitor navigates to /franchise/attendance
  TC-FD-008  Payment Proofs link is visible
  TC-FD-009  Franchise Admin cannot access HEAD_ADMIN routes
  TC-FD-010  Page does not crash on load
"""

import pytest
from pages.franchise.franchise_dashboard_page import FranchiseDashboardPage


@pytest.mark.franchise
@pytest.mark.regression
class TestFranchiseDashboard:
    """Regression tests for the Franchise Admin Dashboard."""

    # ── TC-FD-001 ──────────────────────────────────────────────────────────────
    def test_franchise_dashboard_loads(self, franchise_driver, base_url):
        """
        Purpose: Franchise dashboard loads after login.
        Steps:
            1. Use franchise_driver (logged in as FRANCHISE_ADMIN)
            2. Open /franchise/dashboard
        Expected: URL contains /franchise/dashboard.
        """
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.is_on_franchise_dashboard(), (
            f"Expected /franchise/dashboard URL, got: {page.get_current_url()}"
        )

    # ── TC-FD-002 ──────────────────────────────────────────────────────────────
    def test_franchise_url_after_login(self, franchise_driver, base_url):
        """
        Purpose: URL after franchise login contains /franchise or /dashboard.
        Steps:
            1. Check current URL of franchise_driver
        Expected: URL contains '/franchise' or '/dashboard'.
        """
        current_url = franchise_driver.current_url
        assert "/franchise" in current_url or "/dashboard" in current_url, (
            f"Expected franchise dashboard URL after login, got: {current_url}"
        )

    # ── TC-FD-003 ──────────────────────────────────────────────────────────────
    def test_stat_cards_render(self, franchise_driver, base_url):
        """
        Purpose: Stat cards render on the franchise dashboard.
        Steps:
            1. Open /franchise/dashboard
        Expected: At least one stat card is visible.
        """
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.are_stat_cards_visible(), (
            "Expected stat cards to render on franchise dashboard"
        )

    # ── TC-FD-004 ──────────────────────────────────────────────────────────────
    def test_dashboard_shows_stat_cards(self, franchise_driver, base_url):
        """
        Purpose: Dashboard shows at least one stat card (Students, Mentors, or Attendance Rate).
        Steps:
            1. Open /franchise/dashboard
        Expected: Stat card count >= 1.
        """
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        count = page.get_stat_card_count()
        assert count >= 1, (
            f"Expected at least 1 stat card on franchise dashboard, found: {count}"
        )

    # ── TC-FD-005 ──────────────────────────────────────────────────────────────
    def test_sidebar_visible(self, franchise_driver, base_url):
        """
        Purpose: Sidebar renders with franchise-specific nav links.
        Steps:
            1. Open /franchise/dashboard
        Expected: Sidebar (Attendance Monitor link) is visible.
        """
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.is_sidebar_visible(), (
            "Expected franchise sidebar to be visible"
        )

    # ── TC-FD-006 ──────────────────────────────────────────────────────────────
    def test_attendance_monitor_link_visible(self, franchise_driver, base_url):
        """
        Purpose: Attendance Monitor sidebar link renders.
        Steps:
            1. Open /franchise/dashboard
        Expected: Attendance Monitor link is visible.
        """
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_ATTENDANCE), (
            "Expected Attendance Monitor link to be visible"
        )

    # ── TC-FD-007 ──────────────────────────────────────────────────────────────
    def test_attendance_monitor_navigates(self, franchise_driver, base_url):
        """
        Purpose: Clicking Attendance Monitor navigates to /franchise/attendance.
        Steps:
            1. Open /franchise/dashboard
            2. Click Attendance Monitor sidebar link
        Expected: URL changes to /franchise/attendance.
        """
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        page.click_attendance_monitor()
        page.wait_for_url_contains("/franchise/attendance")
        assert "/franchise/attendance" in page.get_current_url()

    # ── TC-FD-008 ──────────────────────────────────────────────────────────────
    def test_payment_proofs_link_visible(self, franchise_driver, base_url):
        """
        Purpose: Payment Proofs sidebar link renders for FRANCHISE_ADMIN.
        Steps:
            1. Open /franchise/dashboard
        Expected: Payment Proofs link is visible.
        """
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        assert page.is_element_visible(page.NAV_PAYMENT_PROOF), (
            "Expected Payment Proofs link to be visible in franchise sidebar"
        )

    # ── TC-FD-009 ──────────────────────────────────────────────────────────────
    def test_franchise_admin_cannot_access_head_admin_routes(
            self, franchise_driver, base_url):
        """
        Purpose: FRANCHISE_ADMIN cannot access /admin/create-user.
        Steps:
            1. Navigate to /admin/create-user using franchise_driver
        Expected: Redirected away from /admin/create-user.
        """
        import time
        franchise_driver.get(f"{base_url}/admin/create-user")
        time.sleep(2)
        current = franchise_driver.current_url
        assert "/admin/create-user" not in current, (
            f"FRANCHISE_ADMIN should not access /admin/create-user, got: {current}"
        )

    # ── TC-FD-010 ──────────────────────────────────────────────────────────────
    def test_page_does_not_crash(self, franchise_driver, base_url):
        """
        Purpose: Franchise dashboard loads without JavaScript errors.
        Steps:
            1. Open /franchise/dashboard
        Expected: No 'Uncaught' or 'Cannot read' markers in page source.
        """
        page = FranchiseDashboardPage(franchise_driver, base_url)
        page.open()
        source = franchise_driver.page_source.lower()
        assert "cannot read" not in source
        assert "uncaught" not in source
