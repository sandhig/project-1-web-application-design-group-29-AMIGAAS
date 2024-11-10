import pytest
from playwright.sync_api import sync_playwright, expect

# CONSTANT TIMES
WAIT_TO_LOAD_LONG = 5000  # 5000 milliseconds = 5 sec
WAIT_TO_LOAD_SHORT = 1000  # 1000 milliseconds = 1 sec

# CONSTANT URL PATHS
WELCOME_PAGE_URL = 'http://localhost:3000/'
SIGNUP_PAGE_URL = 'http://localhost:3000/profiles/signup'
LOGIN_PAGE_URL = 'http://localhost:3000/profiles/login'
VERIFY_PAGE_URL = 'http://localhost:3000/profiles/verify-email'
FORGOT_PASSWORD_URL = 'http://localhost:3000/password_reset_request'
HOMEPAGE_URL = 'http://localhost:3000/products'

# LOCATOR SELECTORS
SIGNUP = "Sign Up"
LOG_IN = "Log In"
LOGIN = "Login"
VERIFY = "Verify Email"
FORGOT_PASSWORD = "Forgot Password?"
SEND_LINK = "Send me a llink"
FIRST_NAME = "First Name *"
LAST_NAME = "Last Name *"
EMAIL = "UofT Email *"
PASSWORD = "Password *"
CODE = "Verification Code *"
LOGOUT = "logout"

# ROLES
ROLE_BUTTON = 'button'
ROLE_OPTION = 'option'
ROLE_LINK = 'link'
ROLE_HEADING = 'heading'

# AUTHORIZED TEST USER TODO: delete/change later
AUTHORIZED_USER_EMAIL = 'raisa.aishy@mail.utoronto.ca'
AUTHORIZED_USER_PASSWORD = 'Raisa1234!'

@pytest.fixture(scope="session")
def setup_playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def authenticated_context(setup_playwright):
    browser = setup_playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Now log in with the test user
    page = context.new_page()
    page.goto(WELCOME_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG)

    # Save context for reuse in other tests
    yield context
    browser.close()

@pytest.fixture
def page(authenticated_context):
    page = authenticated_context.new_page()
    yield page
    page.close()

# Test for navigating to the urls
def test_navigate_signup_button(page):
    '''Test the signup button navigates to the signup page'''
    # Click on Sign Up Button
    page.goto(WELCOME_PAGE_URL)
    signup_button = page.get_by_role(ROLE_BUTTON, SIGNUP)
    signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_LONG)

    assert page.url == SIGNUP_PAGE_URL
    expect(page.get_by_role(ROLE_HEADING)).to_contain_text(SIGNUP)
    print("Signup button works as expected")


def test_navigate_login_button(page):
    '''Test the login button navigates to the login page'''
    # Click on Sign Up Button
    page.goto(WELCOME_PAGE_URL)
    login_button = page.get_by_role(ROLE_BUTTON, LOG_IN)
    login_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_LONG)

    assert page.url == LOGIN_PAGE_URL
    expect(page.get_by_role(ROLE_HEADING)).to_contain_text("Login")
    print("Login button works as expected")


def test_navigate_to_verify_email_page(page):
    '''Test that anypne can go to the verify email page'''
    page.goto(VERIFY_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG)
    expect(page.get_by_role(ROLE_HEADING)).to_contain_text("Email Verification")
    print("Verify email page displayed as expected")


def test_navigate_to_forgot_password_page(page):
    '''Test that anyone can go to the forgot password page'''
    # Click on the Forgot Password Button
    page.goto(LOGIN_PAGE_URL)
    forgot_password_button = page.get_by_role(ROLE_BUTTON, FORGOT_PASSWORD)
    forgot_password_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_LONG)

    assert page.url == FORGOT_PASSWORD_URL
    expect(page.get_by_role(ROLE_HEADING)).to_contain_text("Forgot Password")
    print("Forgot Password page displayed as expected")


# Test for signups with edge cases
def test_no_input_signup(page):
    '''Test for no input given'''
    page.goto(SIGNUP_PAGE_URL)
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter your first name.").is_visible(), "Empty first name error message not displayed"
    assert page.get_by_text("Please enter your last name.").is_visible(), "Empty last name error message not displayed"
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Invalid email error message not displayed"
    assert page.get_by_text("Please enter your password.").is_visible(), "Empty password error message not displayed"

    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Signup with no input works as expected")


def test_signup_without_first_name(page):
    '''Test for all valid input given but not the first name'''
    # Find the locators for input boxes
    page.goto(SIGNUP_PAGE_URL)
    last_name_box = page.get_by_label(LAST_NAME)
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # fill valid input for the rest
    last_name_box.click()
    last_name_box.fill("TestUserLastName")
    email_box.click()
    email_box.fill("playwright.test@mail.utoronto.ca")
    password_box.click()
    password_box.fill("Pwtest123")

    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter your first name.").is_visible(), "Empty first name error message not displayed"

    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Signup without first name works as expected")


def test_signup_without_last_name(page):
    '''Test for all valid input given but not the last name'''
    # Find the locators for input boxes
    page.goto(SIGNUP_PAGE_URL)
    first_name_box = page.get_by_label(FIRST_NAME)
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # fill valid input for the rest
    first_name_box.click()
    first_name_box.fill("TestUserFirstName")
    email_box.click()
    email_box.fill("playwright.test@mail.utoronto.ca")
    password_box.click()
    password_box.fill("Pwtest123")

    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter your last name.").is_visible(), "Empty last name error message not displayed"

    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Signup without last name works as expected")


def test_signup_without_email(page):
    '''Test for all valid input given but not the email'''
    # Find the locators for input boxes
    page.goto(SIGNUP_PAGE_URL)
    first_name_box = page.get_by_label(FIRST_NAME)
    last_name_box = page.get_by_label(LAST_NAME)
    password_box = page.get_by_label(PASSWORD)

    # fill valid input for the rest
    first_name_box.click()
    first_name_box.fill("TestUserFirstName")
    last_name_box.click()
    last_name_box.fill("TestUserLastName")
    password_box.click()
    password_box.fill("Pwtest123")

    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Invalid email error message not displayed"

    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Signup without email works as expected")


def test_signup_without_password(page):
    '''Test for all valid input given but not the first name'''
    # Find the locators for input boxes
    page.goto(SIGNUP_PAGE_URL)
    first_name_box = page.get_by_label(FIRST_NAME)
    last_name_box = page.get_by_label(LAST_NAME)
    email_box = page.get_by_label(EMAIL)

    # fill valid input for the rest
    first_name_box.click()
    first_name_box.fill("TestuserLastName")
    last_name_box.click()
    last_name_box.fill("TestUserLastName")
    email_box.click()
    email_box.fill("playwright.test@mail.utoronto.ca")

    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter your password.").is_visible(), "Empty password error message not displayed"


    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Signup without password works as expected")


def test_signup_invalid_email(page):
    '''Test for all valid input given but not UofT email'''
    # Find the locators for input boxes
    page.goto(SIGNUP_PAGE_URL)
    first_name_box = page.get_by_label(FIRST_NAME)
    last_name_box = page.get_by_label(LAST_NAME)
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # fill valid input for the rest
    first_name_box.click()
    first_name_box.fill("TestUserFirstName")
    last_name_box.click()
    last_name_box.fill("TestUserLastName")
    password_box.click()
    password_box.fill("Pwtest123")

    # give a non uoft email
    email_box.click()
    email_box.fill("playwright.test@gmail.com")

    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Invalid email error message not displayed"

    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Signup with invalid email works as expected")


def test_signup_valid_email_exists(page):
    '''Test for all valid input given but not UofT email'''
    # Find the locators for input boxes
    page.goto(SIGNUP_PAGE_URL)
    first_name_box = page.get_by_label(FIRST_NAME)
    last_name_box = page.get_by_label(LAST_NAME)
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # fill valid input for the rest
    first_name_box.click()
    first_name_box.fill("TestUserFirstName")
    last_name_box.click()
    last_name_box.fill("TestUserLastName")
    password_box.click()
    password_box.fill("Pwtest123")

    # give email already used in database
    email_box.click()
    email_box.fill("raisa.aishy@mail.utoronto.ca")

    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Email already exists.").is_visible(), "Invalid email error message not displayed"

    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Signup with valid email exists works as expected")


def test_signup_invalid_password(page):
    '''Test for all valid input given but weak password'''
    # Find the locators for input boxes
    page.goto(SIGNUP_PAGE_URL)
    first_name_box = page.get_by_label(FIRST_NAME)
    last_name_box = page.get_by_label(LAST_NAME)
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # fill valid input for the rest
    first_name_box.click()
    first_name_box.fill("TestuserLastName")
    last_name_box.click()
    last_name_box.fill("TestUserLastName")
    email_box.click()
    email_box.fill("playwright.test@mail.utoronto.ca")

    # give a small password
    password_box.click()
    password_box.fill("AB12")

    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Password must be at least 6 characters long.").is_visible(), "Weak password error message not displayed"


    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Signup with invalid password works as expected")


def test_valid_input_signup(page):
    '''Test for all valid input given but not the first name'''
    # Find the locators for input boxes
    page.goto(SIGNUP_PAGE_URL)
    first_name_box = page.get_by_label(FIRST_NAME)
    last_name_box = page.get_by_label(LAST_NAME)
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # fill with valid inputs
    first_name_box.click()
    first_name_box.fill("TestUserFirstName")
    last_name_box.click()
    last_name_box.fill("TestUserLastName")
    email_box.click()
    email_box.fill("playwright.test@mail.utoronto.ca")
    password_box.click()
    password_box.fill("Pwtest123")

    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    submit_signup_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_LONG + WAIT_TO_LOAD_LONG)

    # Check that the submit button is disabled
    submit_signup_button = page.get_by_role(ROLE_BUTTON, name="Sign Up")
    assert submit_signup_button.is_disabled(), "Submit button is not disabled when there are errors"

    # Check for redirection to verification page
    assert page.url == VERIFY_PAGE_URL
    print("Test: Signup with valid inputs works as expected")


# Tests for verification with edge cases
def test_verification_no_input(page):
    '''Test for verifying account after signing up with no input'''
    page.goto(VERIFY_PAGE_URL)
    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=VERIFY)
    submit_verify_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Invalid email error message not displayed"
    assert page.get_by_text("Please enter your verification code.").is_visible(), "Empty code error message not displayed"

    # Check that the submit button is disabled
    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=VERIFY)
    assert submit_verify_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Verification with no input works as expected")


def test_verification_no_email(page):
    '''Test for verifying account after signing up with no email input'''
    page.goto(VERIFY_PAGE_URL)

    # Find the locators for input boxes
    code_box = page.get_by_label(CODE)

    # fill with a code
    code_box.click()
    code_box.fill("123456")

    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=VERIFY)
    submit_verify_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Invalid email error message not displayed"

    # Check that the submit button is disabled
    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=VERIFY)
    assert submit_verify_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Verification with no email input works as expected")


def test_verification_no_code(page):
    '''Test for verifying account after signing up with no code input'''
    page.goto(VERIFY_PAGE_URL)

    # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)

    # fill with a email
    email_box.click()
    email_box.fill("playwright.test@mail.utoronto.ca")

    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=VERIFY)
    submit_verify_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter your verification code.").is_visible(), "Empty code error message not displayed"

    # Check that the submit button is disabled
    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=VERIFY)
    assert submit_verify_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Verification with no code works as expected")


def test_verification_wrong_code(page):
    '''Test for verifying account after signing up with wrong code'''
    page.goto(VERIFY_PAGE_URL)

    # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)
    code_box = page.get_by_label(CODE)

    # fill with a email
    email_box.click()
    email_box.fill("playwright.test@mail.utoronto.ca")
    code_box.click()
    code_box.fill("123456")  # assuming this is wrong code

    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=VERIFY)
    submit_verify_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Invalid verification code.").is_visible(), "Invalid code error message not displayed"
    print("Test: Verification with wrong code works as expected")


def test_verification_wrong_email(page):
    '''Test for verifying account after signing up with wrong email'''
    page.goto(VERIFY_PAGE_URL)

    # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)
    code_box = page.get_by_label(CODE)

    # fill with a email
    email_box.click()
    email_box.fill("neversignup.user@mail.utoronto.ca")
    code_box.click()
    code_box.fill("123456")  # assuming this is wrong code

    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=VERIFY)
    submit_verify_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Email not found.").is_visible(), "Invalid email error message not displayed"
    print("Test: Verification with wrong email works as expected")


# TODO how to know the verification code sent for this fake test email without accessing backend 
def test_verification_valid_input(page):
    pass

# Tests for login with edge cases
def test_login_no_input(page):
    '''Test for logging in to an account with no input'''
    page.goto(LOGIN_PAGE_URL)
    submit_login_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    submit_login_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message for price
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Invalid email error message not displayed"
    assert page.get_by_text("Please enter your password.").is_visible(), "Empty password error message not displayed"

    # Check that the submit button is disabled
    submit_login_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    assert submit_login_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Login with no input works as expected")


def test_login_no_email(page):
    '''Test for logging in to an account with no email'''
    page.goto(LOGIN_PAGE_URL)

    # Find the locators for input boxes
    password_box = page.get_by_label(PASSWORD)

    # give input
    password_box.click()
    password_box.fill(AUTHORIZED_USER_PASSWORD)

    submit_login_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    submit_login_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Invalid email error message not displayed"

    # Check that the submit button is disabled
    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    assert submit_verify_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Login with no email works as expected")


def test_login_no_password(page):
    '''Test for logging in to an account with no password'''
    page.goto(LOGIN_PAGE_URL)

    # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)

    # give input
    email_box.click()
    email_box.fill(AUTHORIZED_USER_EMAIL)

    submit_login_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    submit_login_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message
    assert page.get_by_text("Please enter your password.").is_visible(), "Empty password error message not displayed"

    # Check that the submit button is disabled
    submit_verify_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    assert submit_verify_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Login with no password works as expected")


def test_login_wrong_password(page):
    '''Test for logging in to an account with no password'''
    page.goto(LOGIN_PAGE_URL)

    # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # give input
    email_box.click()
    email_box.fill(AUTHORIZED_USER_EMAIL)
    password_box.click()
    password_box.fill("WrongPassword")

    submit_login_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    submit_login_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message
    assert page.get_by_text("Incorrect email or password.").is_visible(), "Error message not displayed"
    print("Test: Login with wrong password works as expected")


def test_login_wrong_email(page):
    '''Test for logging in to an account with no password'''
    page.goto(LOGIN_PAGE_URL)

    # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # give input
    email_box.click()
    email_box.fill(AUTHORIZED_USER_EMAIL.replace('raisa', 'raisaa'))
    password_box.click()
    password_box.fill(AUTHORIZED_USER_PASSWORD)

    submit_login_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    submit_login_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Check for the specific error message
    try: # if the incorrect email is someone else's email
        assert page.get_by_text("Incorrect email or password.").is_visible(), "Error message not displayed"
    except: # if user doesn't exist for the email provided
        assert page.get_by_text("User not found.").is_visible(), "Non-existent user email message not displayed"
    print("Test: Login with wrong password works as expected")


def test_login_valid_input(page):
    '''Test for logging in to an account with valid input'''
    page.goto(LOGIN_PAGE_URL)

    # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # give input
    email_box.click()
    email_box.fill(AUTHORIZED_USER_EMAIL)
    password_box.click()
    password_box.fill(AUTHORIZED_USER_PASSWORD)

    submit_login_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    submit_login_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Should be logged in and redirected to the homepage
    assert page.url == HOMEPAGE_URL
    print("Test: Login with wrong password works as expected")


def login_user(page):
    '''Helper function to login a user for tests that need authentication'''
    page.goto(LOGIN_PAGE_URL)

    # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)
    password_box = page.get_by_label(PASSWORD)

    # give input
    email_box.click()
    email_box.fill(AUTHORIZED_USER_EMAIL)
    password_box.click()
    password_box.fill(AUTHORIZED_USER_PASSWORD)

    submit_login_button = page.get_by_role(ROLE_BUTTON, name=LOGIN)
    submit_login_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)
    return page



# Test for pasword reset link
def test_password_reset_no_email(page):
    '''Test for sending a reseting password link for no provided email'''
    page.goto(FORGOT_PASSWORD_URL)

    submit_rest_button = page.get_by_role(ROLE_BUTTON, name=SEND_LINK)
    submit_rest_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)
    
    # Check for the specific error message
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Email error message not displayed"

    # Check that the submit button is disabled
    submit_rest_button = page.get_by_role(ROLE_BUTTON, name=SEND_LINK)
    assert submit_rest_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Send password link without email works as expected")


def test_password_reset_invalid_email(page):
    '''Test for sending a reseting password link for a non-UofT provided email'''
    page.goto(FORGOT_PASSWORD_URL)

     # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)

    # give input
    email_box.click()
    email_box.fill("playwright.test@email.com")

    submit_rest_button = page.get_by_role(ROLE_BUTTON, name=SEND_LINK)
    submit_rest_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)
    
    # Check for the specific error message
    assert page.get_by_text("Please enter a valid UofT email address.").is_visible(), "Email error message not displayed"

    # Check that the submit button is disabled
    submit_rest_button = page.get_by_role(ROLE_BUTTON, name=SEND_LINK)
    assert submit_rest_button.is_disabled(), "Submit button is not disabled when there are errors"
    print("Test: Send password link with non uoft email works as expected")


def test_password_reset_invalid_email(page):
    '''Test for sending a reseting password link for a non-UofT provided email'''
    page.goto(FORGOT_PASSWORD_URL)

     # Find the locators for input boxes
    email_box = page.get_by_label(EMAIL)

    # give input
    email_box.click()
    email_box.fill("playwright.test@mail.utoronto.ca")

    submit_rest_button = page.get_by_role(ROLE_BUTTON, name=SEND_LINK)
    submit_rest_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)
    
    # Check for the specific success message
    assert page.get_by_text("If this email is registered, a password reset link will be sent shortly. This may take a few minutes.").is_visible(), "Success message not displayed"

    # Check that the submit button is disabled
    submit_rest_button = page.get_by_role(ROLE_BUTTON, name=SEND_LINK)
    assert submit_rest_button.is_disabled(), "Submit button is not disabled after submission"
    print("Test: Send password link with uoft email works as expected")


# Test for logging out
def test_logout_button(page):
    '''Test the logout functionality'''
    page = login_user(page)

    # locate logout button and click on it
    logout_button = page.get_by_label("logout")
    logout_button.click()
    page.wait_for_timeout(WAIT_TO_LOAD_LONG)

    # should be redirected to the login page
    assert page.url == LOGIN_PAGE_URL
    expect(page.get_by_role(ROLE_HEADING)).to_contain_text("Login")

    # Should not be able to go back to homepage
    page.goto(HOMEPAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG)
    assert page.url != HOMEPAGE_URL  # should not be able to access it anymore
    assert page.url == LOGIN_PAGE_URL  # should be redirected here
    print("Logout button works as expected")












