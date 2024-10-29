import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

WAIT_TO_LOAD_LONG = 5000  # 5000 milliseconds = 5 sec
WAIT_TO_LOAD_SHORT = 1000  # 1000 milliseconds = 1 sec

LOGIN_PAGE_URL = 'http://localhost:3000/profiles/login'
PRODUCTS_PAGE_URL = 'http://localhost:3000/products'

# LOCATOR SELECTORS
EMAIL = 'input[name="email"]'
PASSWORD = 'input[name="password"]'
LOGIN = 'Login'
CATEGORY = 'Category'
CONDITION = 'Condition'
LOCATION = 'Location'

LOGIN_MSG = 'Login successful!'
PRODUCTS_CONTAINER = '.products-container'
PRODUCT_GRID = '.products'
PRODUCT_ITEM = '.product-item'


ROLE_BUTTON = 'button'
ROLE_OPTION = 'option'

# CHOICES
CATEGORY_CHOICES = ['Textbook', 'Clothing', 'Furniture', 'Electronics', 'Stationary', 'Miscellaneous', 'None']
CONDITION_CHOICES = ['New', 'Used - Like New', 'Used - Good', 'Used - Fair', 'None']
LOCATION_CHOICES = ['Robarts', 'Gerstein', 'Computer Science Library', 'Bahen', 'Galbraith', 'Sanford Fleming', 'None']



@pytest.fixture(scope="session")
def setup_playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def authenticated_context(setup_playwright):
    browser = setup_playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Define user credentials used for testing
    USER_EMAIL = "raisa.aishy@mail.utoronto.ca"
    USER_PASSWORD = "Raisa1234!"

    # Now log in with the test user
    page = context.new_page()
    page.goto(LOGIN_PAGE_URL)
    
    # Interact with the email input field
    email_locator = page.locator(EMAIL)
    email_locator.click()
    email_locator.fill(USER_EMAIL)

    # Interact with the password input field
    password_locator = page.locator(PASSWORD)
    password_locator.click()
    password_locator.fill(USER_PASSWORD)

     # Click the Login button
    page.get_by_role(ROLE_BUTTON, name=LOGIN).click()
    page.wait_for_timeout(WAIT_TO_LOAD_LONG)

    # Wait for a successful login message
    # Verify login success message is visible
    assert page.get_by_text(LOGIN_MSG).is_visible()
    print('Successfully logged in test user')

    # Save context for reuse in other tests
    yield context
    browser.close()

@pytest.fixture
def page(authenticated_context):
    page = authenticated_context.new_page()
    yield page
    page.close()

def test_product_list_displays_correctly(page):
    """ Test to ensure multiple products can be seen on the product grid """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Locate the products container
    product_grid = page.locator(PRODUCT_GRID)
    assert product_grid.locator(PRODUCT_ITEM).count() > 0 # count that more than 1 product is listed in the grid
    print("Test: Product List Grid is displayed properly")


def test_filter_by_category(page):
    """ Test to ensure filter by category works as expected """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Count original products
    original_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count original products listed in the grid
    print(".Original count:", original_product_count)

    for choice in CATEGORY_CHOICES:
        # Click on the Category label or dropdown
        page.get_by_label(CATEGORY).click()
        page.wait_for_timeout(WAIT_TO_LOAD_SHORT)
        
        # Select the option with the name 'Textbook'
        page.get_by_role(ROLE_OPTION, name=choice).click()
        page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

        # Locate the products container
        filtered_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
        print("..Choice is:", choice, " -- Filtered count:", filtered_product_count)

        # filtered items must be less than or equal to original for each individual choice
        # filtered items must be equal to original when filter is 'None'
        if choice == 'None':
            assert filtered_product_count == original_product_count
        else: 
            assert filtered_product_count <= original_product_count
    print("Test: Filter by Category works as expected")


def test_filter_by_condition(page):
    """ Test to ensure filter by condition works as expected """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Count original products
    original_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count original products listed in the grid
    print(".Original count:", original_product_count)

    for choice in CONDITION_CHOICES:
        # Click on the Condition label or dropdown
        page.get_by_label(CONDITION).click()
        page.wait_for_timeout(WAIT_TO_LOAD_SHORT)
        
        # Select the option with the name 'Textbook'
        page.get_by_role(ROLE_OPTION, name=choice, exact=True).click()
        page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

        # Locate the products container
        filtered_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
        print("..Choice is:", choice, " -- Filtered count:", filtered_product_count)

        # filtered items must be less than or equal to original for each individual choice
        # filtered items must be equal to original when filter is 'None'
        if choice == 'None':
            assert filtered_product_count == original_product_count
        else: 
            assert filtered_product_count <= original_product_count
    print("Test: Filter by Condition works as expected")


def test_filter_by_location(page):
    """ Test to ensure filter by location works as expected """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Count original products
    original_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count original products listed in the grid
    print(".Original count:", original_product_count)

    for choice in LOCATION_CHOICES:
        # Click on the Condition label or dropdown
        page.get_by_label(LOCATION).click()
        page.wait_for_timeout(WAIT_TO_LOAD_SHORT)
        
        # Select the option with the name 'Textbook'
        page.get_by_role(ROLE_OPTION, name=choice).click()
        page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

        # Locate the products container
        filtered_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
        print("..Choice is:", choice, " -- Filtered count:", filtered_product_count)

        # filtered items must be less than or equal to original for each individual choice
        # filtered items must be equal to original when filter is 'None'
        if choice == 'None':
            assert filtered_product_count == original_product_count
        else: 
            assert filtered_product_count <= original_product_count
    print("Test: Filter by Location works as expected")

