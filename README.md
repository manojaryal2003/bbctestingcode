# BBC School Management System — Regression Test Suite

**Submitted by:** [Your Name]  
**Institution:** Mindrisers Institute of Technology  
**Certification Task:** Regression Testing  
**Submission Deadline:** April 27, 2026  
**Live Application URL:** https://bbc.smartitsolutionnepal.com  

---

## 1. Project Overview

This repository contains a complete **Regression Test Suite** for the BBC School Management System — a multi-role web application that manages students, mentors, franchise admins, parents, and the head administrator.

**What is Regression Testing?**  
Regression testing is the process of re-running functional and non-functional tests on a modified application to confirm that existing features still work correctly after new code changes, bug fixes, or feature additions. It prevents the introduction of new bugs ("regressions") as the application evolves.

The suite covers:
- Authentication flows (login, logout, protected routes)
- Role-based access control (5 roles × their routes)
- All major pages and forms for each role
- Both **positive** (valid input, expected success) and **negative** (invalid input, expected failure) test cases
- Automatic screenshot capture on every test failure
- HTML report generation

---

## 2. Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.x | Programming language |
| Selenium WebDriver | 4.18.1 | Browser automation |
| pytest | 8.1.1 | Test framework and runner |
| pytest-html | 4.1.1 | HTML report generation |
| webdriver-manager | 4.0.1 | Auto-manages ChromeDriver |
| pytest-ordering | 0.6 | Test execution ordering |
| python-dotenv | 1.0.1 | Load credentials from .env |

---

## 3. Folder Structure

```
testing/
│
├── conftest.py                         # pytest fixtures: driver, credentials, screenshot hook
├── pytest.ini                          # pytest configuration (paths, markers, HTML report)
├── requirements.txt                    # All Python dependencies
├── .env                                # Real credentials — NEVER commit (gitignored)
├── .env.example                        # Placeholder template — safe to commit
├── .gitignore                          # Excludes .env, __pycache__, screenshots, reports
├── README.md                           # This documentation file
│
├── pages/                              # Page Object Model layer
│   ├── base_page.py                    # Base class with shared methods for all pages
│   ├── login_page.py                   # /login — login form interactions
│   │
│   ├── admin/
│   │   ├── admin_dashboard_page.py     # /admin/dashboard
│   │   ├── create_user_page.py         # /admin/create-user
│   │   ├── manage_users_page.py        # /admin/manage-users
│   │   └── fee_management_page.py      # /admin/fee-management
│   │
│   ├── mentor/
│   │   ├── mentor_dashboard_page.py    # /mentor/dashboard
│   │   ├── attendance_page.py          # /mentor/attendance
│   │   ├── upload_activity_page.py     # /mentor/upload-activity
│   │   └── homework_management_page.py # /mentor/send-homework + /mentor/homework-management
│   │
│   ├── student/
│   │   ├── student_dashboard_page.py   # /student/dashboard
│   │   ├── submit_homework_page.py     # /student/submit-homework
│   │   └── student_upload_activity_page.py  # /student/upload-activity
│   │
│   ├── parent/
│   │   ├── parent_dashboard_page.py    # /parent/dashboard
│   │   ├── attendance_report_page.py   # /parent/attendance-report
│   │   └── fee_status_page.py          # /parent/fee-status
│   │
│   └── franchise/
│       ├── franchise_dashboard_page.py # /franchise/dashboard
│       └── attendance_monitor_page.py  # /franchise/attendance
│
├── tests/                              # Test suites grouped by role/feature
│   ├── test_auth/
│   │   ├── test_login.py               # 14 login test cases (all 5 roles + edge cases)
│   │   └── test_protected_routes.py    # 11 route access control test cases
│   │
│   ├── test_admin/
│   │   ├── test_admin_dashboard.py     # 10 admin dashboard tests
│   │   ├── test_create_user.py         # 10 create user form tests
│   │   ├── test_manage_users.py        # 9 manage users tests
│   │   └── test_fee_management.py      # 8 fee package tests
│   │
│   ├── test_mentor/
│   │   ├── test_mentor_dashboard.py    # 10 mentor dashboard tests
│   │   ├── test_attendance.py          # 8 attendance page tests
│   │   ├── test_upload_activity.py     # 10 upload activity tests
│   │   └── test_homework_management.py # 9 homework management tests
│   │
│   ├── test_student/
│   │   ├── test_student_dashboard.py   # 10 student dashboard tests
│   │   ├── test_submit_homework.py     # 7 submit homework tests
│   │   └── test_student_upload_activity.py # 7 student upload tests
│   │
│   ├── test_parent/
│   │   ├── test_parent_dashboard.py    # 10 parent dashboard tests
│   │   ├── test_attendance_report.py   # 5 attendance report tests
│   │   └── test_fee_status.py          # 6 fee status tests
│   │
│   └── test_franchise/
│       ├── test_franchise_dashboard.py # 10 franchise dashboard tests
│       └── test_attendance_monitor.py  # 6 attendance monitor tests
│
├── screenshots/                        # Auto-created — failure screenshots saved here
└── reports/                            # Auto-created — HTML reports saved here
```

**Key design choices:**
- `pages/` contains ONLY page interaction logic (no assertions)
- `tests/` contains ONLY test logic (no direct Selenium calls)
- `conftest.py` is the single source of truth for driver setup and credentials
- Every test is fully independent (fresh browser per test)

---

## 4. What is Page Object Model (POM)?

**Page Object Model** is a design pattern where each web page has a corresponding Python class. The class:
1. Stores all element locators as class-level constants
2. Provides methods for every user action on that page
3. Contains NO test assertions (those live in test files)

**Benefits:**
- If a locator changes in the UI, you update it in ONE place (the page class), not in dozens of tests
- Tests read like plain English: `page.login(user, password)` vs `driver.find_element(By.NAME, "userId").send_keys(user)`
- Reduces code duplication across tests

**Example:**
```python
# BAD — brittle, duplicated everywhere
driver.find_element(By.NAME, "userId").send_keys("admin123")
driver.find_element(By.NAME, "password").send_keys("secret")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# GOOD — using POM
login_page = LoginPage(driver, BASE_URL)
login_page.login("admin123", "secret")
```

---

## 5. Application Roles Discovered

| Role | Login Redirects To | Key Features Tested |
|------|--------------------|---------------------|
| `HEAD_ADMIN` | `/admin/dashboard` | Create/Manage Users, Fee Packages, Dashboard Stats |
| `FRANCHISE_ADMIN` | `/franchise/dashboard` | Attendance Monitor, Payment Proofs, Dashboard Stats |
| `MENTOR` | `/mentor/dashboard` | Mark Attendance, Upload Activity, Send Homework |
| `STUDENT` | `/student/dashboard` | Submit Homework, Upload Activity, Badges, Progress |
| `PARENT` | `/parent/dashboard` | Attendance Report, Fee Status, Messages |

---

## 6. Prerequisites

Before running tests, ensure you have:

1. **Python 3.8 or higher** — download from https://www.python.org/downloads/
   - During install on Windows: **check "Add Python to PATH"**
   - Verify: open a terminal and run `python --version`
2. **Google Chrome** browser (latest version)
3. **Internet connection** — tests run against the live site at https://bbc.smartitsolutionnepal.com
4. **Git** (only needed if cloning the repo)

No need to install ChromeDriver manually — `webdriver-manager` downloads the correct version automatically.

---

## 7. Setup Guide (Step by Step)

### Step 1 — Get the code

If you are cloning from GitHub:
```bash
git clone https://github.com/YOUR_USERNAME/bbc-regression-tests.git
cd bbc-regression-tests/testing
```

If you already have the folder, open a terminal and navigate into it:
```
# Windows (PowerShell or Command Prompt)
cd "C:\Users\YourName\Desktop\My project\Testing"
```

### Step 2 — Create a virtual environment

A virtual environment keeps the project's packages separate from your system Python.

```bash
python -m venv venv
```

### Step 3 — Activate the virtual environment

**Windows (PowerShell):**
```
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```
venv\Scripts\activate.bat
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

You will see `(venv)` appear at the start of your terminal prompt — this means it is active.

> **Important:** You must activate the venv every time you open a new terminal before running tests.

### Step 4 — Install all dependencies

```bash
pip install -r requirements.txt
```

This installs: Selenium, pytest, pytest-html, webdriver-manager, python-dotenv, and all other required packages.

### Step 5 — Create your `.env` credentials file

The `.env` file holds the real login credentials. It is **never committed to GitHub** (it is gitignored).

Copy the template:

**Windows:**
```
copy .env.example .env
```

**Mac / Linux:**
```bash
cp .env.example .env
```

Now open `.env` in any text editor (Notepad, VS Code, etc.) and fill in the real credentials:

```
BASE_URL=https://bbc.smartitsolutionnepal.com

ADMIN_USER_ID=your_admin_username
ADMIN_PASSWORD=your_admin_password

FRANCHISE_USER_ID=your_franchise_username
FRANCHISE_PASSWORD=your_franchise_password

MENTOR_USER_ID=your_mentor_username
MENTOR_PASSWORD=your_mentor_password

STUDENT_USER_ID=your_student_username
STUDENT_PASSWORD=your_student_password

PARENT_USER_ID=your_parent_username
PARENT_PASSWORD=your_parent_password

HEADLESS=false
WAIT_TIMEOUT=10
```

> **NEVER commit `.env` to GitHub.** It contains real passwords. Only `.env.example` (with placeholder values) is pushed.

---

## 8. How to Run Tests

> **Always use `venv\Scripts\python.exe -m pytest` on Windows** instead of just `pytest`.  
> Running plain `pytest` may use your system Python which does not have the packages installed.

All commands below assume you are inside the `testing/` folder.

### Run the full suite (all 160 tests)
```
venv\Scripts\python.exe -m pytest -v
```

### Run with short traceback on failures
```
venv\Scripts\python.exe -m pytest -v --tb=short
```

### Run only authentication & login tests
```
venv\Scripts\python.exe -m pytest tests/test_auth/ -v
```

### Run only admin tests
```
venv\Scripts\python.exe -m pytest tests/test_admin/ -v
```

### Run only mentor tests
```
venv\Scripts\python.exe -m pytest tests/test_mentor/ -v
```

### Run only student tests
```
venv\Scripts\python.exe -m pytest tests/test_student/ -v
```

### Run only parent tests
```
venv\Scripts\python.exe -m pytest tests/test_parent/ -v
```

### Run only franchise tests
```
venv\Scripts\python.exe -m pytest tests/test_franchise/ -v
```

### Run a single test file
```
venv\Scripts\python.exe -m pytest tests/test_auth/test_login.py -v
```

### Run one specific test case
```
venv\Scripts\python.exe -m pytest tests/test_auth/test_login.py::TestLogin::test_admin_login_redirects_to_admin_dashboard -v
```

### View the HTML report
After any run, open this file in your browser:
```
reports/regression_report.html
```
It is generated automatically on every run and contains pass/fail status, logs, and failure screenshots.

---

## 8a. Mac / Linux equivalent commands

On Mac or Linux, after activating the venv (`source venv/bin/activate`), you can use:
```bash
python -m pytest -v
python -m pytest tests/test_auth/ -v
# etc.
```

---

## 9. Complete Test Cases Table

| Test ID | Test Name | Feature | Description | Expected Result |
|---------|-----------|---------|-------------|-----------------|
| TC-AUTH-001 | test_admin_login_redirects_to_admin_dashboard | Login | HEAD_ADMIN login with valid credentials | Redirected to /admin/dashboard |
| TC-AUTH-002 | test_franchise_login_redirects_to_franchise_dashboard | Login | FRANCHISE_ADMIN login with valid credentials | Redirected to /franchise/dashboard |
| TC-AUTH-003 | test_mentor_login_redirects_to_mentor_dashboard | Login | MENTOR login with valid credentials | Redirected to /mentor/dashboard |
| TC-AUTH-004 | test_student_login_redirects_to_student_dashboard | Login | STUDENT login with valid credentials | Redirected to /student/dashboard |
| TC-AUTH-005 | test_parent_login_redirects_to_parent_dashboard | Login | PARENT login with valid credentials | Redirected to /parent/dashboard |
| TC-AUTH-006 | test_empty_form_shows_validation_errors | Login | Submit empty login form | At least one validation error shown |
| TC-AUTH-007 | test_empty_userid_shows_error | Login | Submit with only password | User ID required error visible |
| TC-AUTH-008 | test_empty_password_shows_error | Login | Submit with only user ID | Password required error visible |
| TC-AUTH-009 | test_wrong_password_shows_invalid_credentials | Login | Correct user ID, wrong password | 'Invalid credentials' error; stays on /login |
| TC-AUTH-010 | test_nonexistent_user_shows_invalid_credentials | Login | Non-existent user ID | Error alert; stays on /login |
| TC-AUTH-011 | test_login_page_heading | Login | Check page heading text | 'School Management System' visible |
| TC-AUTH-012 | test_sign_in_button_is_visible | Login | Sign In button present | Button is visible |
| TC-AUTH-013 | test_admin_navbar_shows_head_admin_role | Login | Role label after admin login | Sidebar shows 'Admin' role |
| TC-AUTH-014 | test_logout_returns_to_login_page | Logout | Click Logout button | Redirected to /login |
| TC-ROUTE-001 | test_unauthenticated_admin_route_redirects_to_login | Protected Routes | No session, try /admin/dashboard | Redirect to /login |
| TC-ROUTE-002 | test_unauthenticated_mentor_route_redirects_to_login | Protected Routes | No session, try /mentor/dashboard | Redirect to /login |
| TC-ROUTE-003 | test_unauthenticated_student_route_redirects_to_login | Protected Routes | No session, try /student/dashboard | Redirect to /login |
| TC-ROUTE-004 | test_unauthenticated_parent_route_redirects_to_login | Protected Routes | No session, try /parent/dashboard | Redirect to /login |
| TC-ROUTE-005 | test_unauthenticated_franchise_route_redirects_to_login | Protected Routes | No session, try /franchise/dashboard | Redirect to /login |
| TC-ROUTE-006 | test_admin_can_access_admin_dashboard | Route Access | Admin session, try own dashboard | Stays on /admin/dashboard |
| TC-ROUTE-007 | test_admin_can_access_create_user | Route Access | Admin session, try /admin/create-user | Stays on /admin/create-user |
| TC-ROUTE-008 | test_admin_can_access_manage_users | Route Access | Admin session, try /admin/manage-users | Stays on /admin/manage-users |
| TC-ROUTE-009 | test_mentor_cannot_access_admin_dashboard | Route Access | Mentor session, try /admin/dashboard | Redirected away |
| TC-ROUTE-010 | test_student_cannot_access_mentor_attendance | Route Access | Student session, try /mentor/attendance | Redirected away |
| TC-ROUTE-011 | test_parent_cannot_access_admin_create_user | Route Access | Parent session, try /admin/create-user | Redirected away |
| TC-ADMIN-001 | test_admin_dashboard_loads | Admin Dashboard | Navigate to /admin/dashboard | Page loads; URL correct |
| TC-ADMIN-002 | test_admin_dashboard_url | Admin Dashboard | URL check after login | URL contains /dashboard |
| TC-ADMIN-003 | test_stat_cards_are_visible | Admin Dashboard | Check stat cards | At least one card visible |
| TC-ADMIN-004 | test_dashboard_shows_four_stat_cards | Admin Dashboard | Count stat cards | 4 cards (Users, Franchises, Mentors, Students) |
| TC-ADMIN-005 | test_sidebar_navigation_is_visible | Admin Dashboard | Check sidebar | Create User link visible |
| TC-ADMIN-006 | test_navigate_to_create_user_via_sidebar | Admin Dashboard | Click Create User | URL = /admin/create-user |
| TC-ADMIN-007 | test_navigate_to_manage_users_via_sidebar | Admin Dashboard | Click Manage Users | URL = /admin/manage-users |
| TC-ADMIN-008 | test_navigate_to_fee_packages_via_sidebar | Admin Dashboard | Click Fee Packages | URL = /admin/fee-management |
| TC-ADMIN-009 | test_navigate_to_reports_via_sidebar | Admin Dashboard | Click Reports | URL = /admin/reports |
| TC-ADMIN-010 | test_page_title_contains_school_management | Admin Dashboard | Check browser tab title | Title is non-empty |
| TC-CU-001 | test_create_user_page_loads | Create User | Navigate to /admin/create-user | Page loads; URL correct |
| TC-CU-002 | test_create_user_form_fields_visible | Create User | Check all form fields | User ID, Password, Role, Submit visible |
| TC-CU-003 | test_empty_userid_shows_validation_error | Create User | Submit without User ID | User ID error visible |
| TC-CU-004 | test_empty_password_shows_validation_error | Create User | Submit without Password | Password error visible |
| TC-CU-005 | test_short_password_shows_validation_error | Create User | 3-char password | Password min-length error |
| TC-CU-006 | test_role_dropdown_has_all_options | Create User | Read role dropdown options | All 4 roles present |
| TC-CU-007 | test_mentor_role_shows_franchise_admin_field | Create User | Select MENTOR role | franchiseAdminId field appears |
| TC-CU-008 | test_student_role_shows_franchise_and_mentor_fields | Create User | Select STUDENT role | Both STUDENT fields appear |
| TC-CU-009 | test_parent_role_shows_student_id_field | Create User | Select PARENT role | studentId field appears |
| TC-CU-010 | test_mentor_without_franchise_admin_id_shows_error | Create User | Submit MENTOR without franchiseAdminId | Validation error shown |
| TC-MU-001 | test_manage_users_page_loads | Manage Users | Navigate to /admin/manage-users | Page loads |
| TC-MU-002 | test_role_filter_tabs_are_visible | Manage Users | Check tabs | All 4 role tabs visible |
| TC-MU-003 | test_default_tab_is_franchise | Manage Users | Default tab on load | Franchise tab active |
| TC-MU-004 | test_click_mentor_tab_filters_mentors | Manage Users | Click Mentor tab | Table updates; URL unchanged |
| TC-MU-005 | test_click_student_tab_filters_students | Manage Users | Click Student tab | Table updates |
| TC-MU-006 | test_click_parent_tab_filters_parents | Manage Users | Click Parent tab | Table updates |
| TC-MU-007 | test_user_table_renders | Manage Users | Check table | Table renders |
| TC-MU-008 | test_select_all_checkbox_is_visible | Manage Users | Check select-all checkbox | Checkbox visible |
| TC-MU-009 | test_delete_button_visible_after_selecting_users | Manage Users | Select users then check | Delete button visible |
| TC-FEE-001 | test_fee_management_page_loads | Fee Management | Navigate to /admin/fee-management | Page loads |
| TC-FEE-002 | test_add_package_button_is_visible | Fee Management | Check Add Package button | Button visible |
| TC-FEE-003 | test_add_package_button_opens_modal | Fee Management | Click Add Package | Modal opens |
| TC-FEE-004 | test_package_modal_has_name_and_amount_fields | Fee Management | Open modal, check fields | Name + Amount inputs visible |
| TC-FEE-005 | test_cancel_modal_closes_it | Fee Management | Open modal, click Cancel | Modal closes |
| TC-FEE-006 | test_empty_package_form_shows_error | Fee Management | Save empty form | Error shown |
| TC-FEE-007 | test_package_list_renders | Fee Management | Check package list | Renders without crash |
| TC-FEE-008 | test_page_does_not_crash_on_load | Fee Management | Check page source | No JS errors |
| TC-MD-001–010 | Mentor Dashboard tests | Mentor Dashboard | Navigation, sidebar, role isolation | See test file |
| TC-ATT-001–008 | Mentor Attendance tests | Attendance | Tabs, date input, save button | See test file |
| TC-UA-001–010 | Upload Activity tests | Upload Activity | Form fields, validation, list | See test file |
| TC-HW-001–009 | Homework Management tests | Send Homework | Form, validation, navigation | See test file |
| TC-SD-001–010 | Student Dashboard tests | Student Dashboard | Sidebar, navigation, access | See test file |
| TC-SHW-001–007 | Submit Homework tests | Submit Homework | List, modal, file required | See test file |
| TC-SUA-001–007 | Student Upload Activity tests | Student Upload | Form, validation | See test file |
| TC-PD-001–010 | Parent Dashboard tests | Parent Dashboard | Sidebar, navigation, access | See test file |
| TC-PAR-001–005 | Parent Attendance Report tests | Attendance Report | Page load, table, records | See test file |
| TC-FS-001–006 | Fee Status tests | Fee Status | Bills, status labels | See test file |
| TC-FD-001–010 | Franchise Dashboard tests | Franchise Dashboard | Stats, sidebar, navigation | See test file |
| TC-AM-001–006 | Attendance Monitor tests | Attendance Monitor | Date input, table, rows | See test file |

**Total: 100+ test cases across 5 roles and 20+ pages**

---

## 10. Screenshot on Failure

Every time a test fails, the test suite **automatically captures a screenshot** of the browser at the moment of failure.

**How it works:**
- A `pytest_runtest_makereport` hook in `conftest.py` fires after each test
- If `report.when == "call"` and `report.failed`, it calls `driver.save_screenshot()`
- The screenshot is saved to `screenshots/` with the test name and timestamp in the filename
- The screenshot is also **embedded directly in the HTML report**

**Screenshot filename format:**
```
FAIL__tests_test_auth__test_login__TestLogin__test_wrong_password__20260418_103045.png
```

**To view screenshots:**
1. Check the `screenshots/` folder after a test run
2. Or open `reports/regression_report.html` and look for embedded images next to failed tests

---

## 11. How to Push to GitHub

### Step 1 — Initialize git in the testing folder
```bash
cd "c:/Users/HP/Desktop/My project/testing"
git init
```

### Step 2 — Add the remote repository
```bash
git remote add origin https://github.com/YOUR_USERNAME/bbc-regression-tests.git
```

### Step 3 — Stage all files (excluding gitignored files)
```bash
git add .
```

### Step 4 — Verify .env is NOT staged
```bash
git status
```
The `.env` file must NOT appear in the list. If it does, run:
```bash
git rm --cached .env
```

### Step 5 — Commit
```bash
git commit -m "Add regression test suite for BBC School Management System"
```

### Step 6 — Push
```bash
git push -u origin main
```

> **Do NOT push `.env`** — it contains real credentials. Only `.env.example` (with placeholder values) is committed.

---

## 12. Troubleshooting

### "No module named pytest" — most common issue on Windows
```
C:\Python314\python.exe: No module named pytest
```
**Cause:** You ran `pytest` using the system Python instead of the virtual environment Python.  
**Fix:** Always use the full venv path:
```
venv\Scripts\python.exe -m pytest -v
```
Never just `pytest` on Windows unless you are 100% sure the venv is activated.

---

### `OSError: [WinError 193] %1 is not a valid Win32 application`
**Cause:** A known bug in `webdriver-manager 4.x` — it returns a path to a licence text file instead of `chromedriver.exe`.  
**Fix:** Already patched in `conftest.py`. If you see this error it means `conftest.py` was overwritten. Restore the `_build_driver()` function to include:
```python
driver_path = ChromeDriverManager().install()
if not driver_path.endswith(".exe"):
    driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
service = Service(driver_path)
```

---

### ChromeDriver version mismatch
```
SessionNotCreatedException: This version of ChromeDriver only supports Chrome version XX
```
**Fix:** `webdriver-manager` auto-downloads the correct version. If it still fails, clear the cache and retry:
```
rmdir /s /q "%USERPROFILE%\.wdm"
venv\Scripts\python.exe -m pytest -v
```

---

### `ModuleNotFoundError: No module named 'pages'`
**Cause:** pytest is not being run from inside the `testing/` folder.  
**Fix:** Navigate into the correct folder first:
```
cd "C:\Users\YourName\Desktop\My project\Testing"
venv\Scripts\python.exe -m pytest -v
```

---

### `.env` file not found / all credentials are `None`
**Fix:** The `.env` file must be in the `testing/` folder (same level as `conftest.py`). Check:
```
# Windows
dir .env

# Mac/Linux
ls -la .env
```
If missing, copy `.env.example` to `.env` and fill in the real credentials.

---

### Browser opens and immediately closes
This is **normal behaviour** — each test gets its own fresh browser instance, runs the test, then closes it. You will see Chrome open and close once per test. If it closes before any action happens, the test likely failed at setup — check the HTML report at `reports/regression_report.html`.

---

### `TimeoutException` on slow networks
**Fix:** Increase the wait timeout in `.env`:
```
WAIT_TIMEOUT=20
```
Default is 10 seconds. The live site may be slow at peak times — 15–20 seconds is safer.

---

### PowerShell says "execution of scripts is disabled"
```
venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled
```
**Fix:** Use the `.exe` approach instead — no activation needed:
```
venv\Scripts\python.exe -m pytest -v
```
Or enable scripts for the current session only:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Tests pass locally but fail in headless / CI
**Fix:** Set `HEADLESS=true` in your `.env`. Some UI interactions behave differently headless — increase `WAIT_TIMEOUT` to 20 as well.

---

*Generated for Mindrisers Certification — Regression Testing Assignment*  
*Application: BBC School Management System | https://bbc.smartitsolutionnepal.com*
