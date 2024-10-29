import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
import random

# CONSTANT TIMES
WAIT_TO_LOAD_LONG = 5000  # 5000 milliseconds = 5 sec
WAIT_TO_LOAD_SHORT = 1000  # 1000 milliseconds = 1 sec

# CONSTANT URL PATHS
LOGIN_PAGE_URL = 'http://localhost:3000/profiles/login'
PRODUCTS_PAGE_URL = 'http://localhost:3000/products'

# LOCATOR SELECTORS
EMAIL = 'input[name="email"]'
PASSWORD = 'input[name="password"]'
LOGIN = 'Login'
CATEGORY = 'Category'
CONDITION = 'Condition'
LOCATION = 'Location'
SORT_BY = 'Sort By'
SEARCH_BAR = 'Search...'
LOGIN_MSG = 'Login successful!'
PRODUCTS_CONTAINER = '.products-container'
PRODUCT_GRID = '.products'
PRODUCT_ITEM = '.product-item'
PRODUCT_PRICE = '.product-price'
PRODUCT_TITLE = '.product-title'
PRICE_SLIDER_TRACK = ".MuiSlider-track"
CLEAR_FILTERS = 'Clear Filters'

# ROLES
ROLE_BUTTON = 'button'
ROLE_OPTION = 'option'

# CHOICES
CATEGORY_CHOICES = ['Textbook', 'Clothing', 'Furniture', 'Electronics', 'Stationary', 'Miscellaneous', 'None']
CONDITION_CHOICES = ['New', 'Used - Like New', 'Used - Good', 'Used - Fair', 'None']
LOCATION_CHOICES = ['Robarts', 'Gerstein', 'Computer Science Library', 'Bahen', 'Galbraith', 'Sanford Fleming', 'None']
SORT_BY_CHOICES = ['Price: Low to High', 'Price: High to Low', 'Name: A-Z']


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


def create_random_combination_of_filters(page):
    """ Helper function to create a random combination of filters"""
    # Count original products
    original_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count original products listed in the grid
    print(".Original count:", original_product_count)

    # Generate a random category, condition, location and random percentage where we want to drag the slider
    random_category_index = random.randint(0, len(CATEGORY_CHOICES)-1)
    random_condtion_index = random.randint(0, len(CONDITION_CHOICES)-1)
    random_location_index = random.randint(0, len(LOCATION_CHOICES)-1)
    random_number_slider = random.randint(1, 100)
    random_width_percentage = random_number_slider / 100
    
    # Set up a random combination of filters
    page.get_by_label(CATEGORY).click()
    page.get_by_role(ROLE_OPTION, name=CATEGORY_CHOICES[random_category_index]).click()  # Choose a random category
    page.get_by_label(CONDITION).click()
    page.get_by_role(ROLE_OPTION, name=CONDITION_CHOICES[random_condtion_index]).click()  # Choose a random condition
    page.get_by_label(LOCATION).click()
    page.get_by_role(ROLE_OPTION, name=LOCATION_CHOICES[random_location_index]).click()  # Choose a random location
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Set up the price slider
    price_slider = page.locator(PRICE_SLIDER_TRACK)
    price_slider_position = price_slider.bounding_box()
    target_x = price_slider_position['x'] + price_slider_position['width'] * random_width_percentage
    target_y = price_slider_position['y'] + price_slider_position['height'] / 2 
    page.mouse.click(target_x, target_y)
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Count number of products returned after single filter
    filtered_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
    print("..After all filtering -- Filtered count:", filtered_product_count)
    print("..Created random filter combination")
    return original_product_count, filtered_product_count, page


def create_random_sort_by_choice(page):
    """ Helper function to choose a random sort by order choice"""
    random_sort_by_index = random.randint(0, len(SORT_BY_CHOICES)-1)
    if random_sort_by_index in [0, 1]:
        # Find the unfiltered, unsorted prices list
        unsorted = page.locator(PRODUCT_PRICE).all_text_contents()

        if random_sort_by_index == 0:
            # Sort the unsorted prices, this is what we expect it to look like later
            sorted_expected = sorted(unsorted, key=lambda x: float(x.replace("$", "")))
        elif random_sort_by_index == 1:
            # Sort the unsorted prices, this is what we expect it to look like later
            sorted_expected = sorted(unsorted, key=lambda x: float(x.replace("$", "")), reverse=True)

        # Apply sorting by price: low to high on the UI
        page.get_by_label("Sort By").click()
        page.get_by_role(ROLE_OPTION, name=SORT_BY_CHOICES[random_sort_by_index]).click()
        page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

        after_sorting = page.locator(PRODUCT_PRICE).all_text_contents()
        
    elif random_sort_by_index == 2 :
        # Find the unfiltered, unsorted nams list
        unsorted = page.locator(PRODUCT_TITLE).all_text_contents()

        # Sort the unsorted names, this is what we expect it to look like later
        # Sorting is not uppder case senstivie in our app
        sorted_expected = sorted(unsorted, key=lambda x: x.lower())

        # Apply sorting by name: A - Z in the UI
        page.get_by_label("Sort By").click()
        page.get_by_role(ROLE_OPTION, name=SORT_BY_CHOICES[random_sort_by_index]).click()
        page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

        after_sorting = page.locator(PRODUCT_TITLE).all_text_contents()
        
    print("..Create random sort by order choice")
    return sorted_expected, after_sorting, page


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


def test_price_slider_halfway(page):
    """ Test to ensure price slider can be dragged to halfway"""
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Count original products
    original_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count original products listed in the grid
    print(".Original count:", original_product_count)

    # Find the slider position
    price_slider = page.locator(PRICE_SLIDER_TRACK)
    price_slider_position = price_slider.bounding_box()

    # Slider will be dragged halfway for this test
    target_x = price_slider_position['x'] + price_slider_position['width'] * 0.5
    target_y = price_slider_position['y'] + price_slider_position['height'] / 2 
    page.mouse.click(target_x, target_y)
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Locate the products container
    filtered_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
    print("..Slider is dragged halfway -- Filtered count:", filtered_product_count)
    assert filtered_product_count <= original_product_count
    print("Test: Slider can be dragged to halfway")


def test_price_slider_random(page):
    """ Test to ensure price slider can be dragged to any length of the slider chosen randomly"""
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Count original products
    original_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count original products listed in the grid
    print(".Original count:", original_product_count)

    # Find the slider position
    price_slider = page.locator(PRICE_SLIDER_TRACK)
    price_slider_position = price_slider.bounding_box()

    # Generate a random percentage where we want to drag the slider
    random_number = random.randint(1, 100)
    random_width_percentage = random_number / 100

    # Slider will be dragged to a random position for this test
    target_x = price_slider_position['x'] + price_slider_position['width'] * random_width_percentage
    target_y = price_slider_position['y'] + price_slider_position['height'] / 2 
    page.mouse.click(target_x, target_y)
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Locate the products container
    filtered_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
    print("..Slider is dragged to", random_number, "% width -- Filtered count:", filtered_product_count)
    assert filtered_product_count <= original_product_count
    print("Test: Slider can be dragged to any length of the slider generated randomly")


def test_all_filter_combinations(page):
    """ Test to ensure all filters can be combined together"""
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Count original products
    original_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count original products listed in the grid
    print(".Original count:", original_product_count)

    # Generate a random category, condition, location and random percentage where we want to drag the slider
    random_category_index = random.randint(0, len(CATEGORY_CHOICES)-1)
    random_condtion_index = random.randint(0, len(CONDITION_CHOICES)-1)
    random_location_index = random.randint(0, len(LOCATION_CHOICES)-1)
    random_number_slider = random.randint(1, 100)
    random_width_percentage = random_number_slider / 100

    # Click on the Category chosen randomly
    page.get_by_label(CATEGORY).click()
    page.get_by_role(ROLE_OPTION, name=CATEGORY_CHOICES[random_category_index]).click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Count number of products returned after single filter
    filtered_product_count_1_filter = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
    print("..After category filtering -- Filtered count:", filtered_product_count_1_filter)
    assert filtered_product_count_1_filter <= original_product_count

    # Click on the Condition chosen randomly
    page.get_by_label(CONDITION).click()
    page.get_by_role(ROLE_OPTION, name=CONDITION_CHOICES[random_condtion_index]).click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Count number of products returned after two filters
    filtered_product_count_2_filter = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
    print("..After category & condition filtering -- Filtered count:", filtered_product_count_2_filter)
    assert filtered_product_count_2_filter <= filtered_product_count_1_filter

    # Click on the Location chosen randomly
    page.get_by_label(LOCATION).click()
    page.get_by_role(ROLE_OPTION, name=LOCATION_CHOICES[random_location_index]).click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Count number of products returned after three filters
    filtered_product_count_3_filter = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
    print("..After category, condition & location filtering -- Filtered count:", filtered_product_count_3_filter)
    assert filtered_product_count_3_filter <= filtered_product_count_2_filter

    # Drag slider to the chosen posiion
    price_slider = page.locator(PRICE_SLIDER_TRACK)
    price_slider_position = price_slider.bounding_box()
    target_x = price_slider_position['x'] + price_slider_position['width'] * random_width_percentage
    target_y = price_slider_position['y'] + price_slider_position['height'] / 2 
    page.mouse.click(target_x, target_y)
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    # Count number of products returned after four filters
    filtered_product_count_4_filter = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
    print("..After category, condition, locaion & price filtering -- Filtered count:", filtered_product_count_4_filter)
    assert filtered_product_count_4_filter <= filtered_product_count_3_filter
    print("Test: Multiple filters can be combined together")


def test_clear_all_filters(page):
    """ Test to ensure all filters can be cleared after multiple filters are applied """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    original_product_count, filtered_product_count, page = create_random_combination_of_filters(page)
    
    # Locate "Clear Filters" button and click
    page.get_by_role(ROLE_BUTTON, name=CLEAR_FILTERS).click()
    unfiltered_product_count = page.locator(PRODUCT_GRID).locator(PRODUCT_ITEM).count() # count filtered products listed in the grid
    print("..After clearing all filtering -- Product Count:", unfiltered_product_count)
    assert unfiltered_product_count >= filtered_product_count
    assert unfiltered_product_count == original_product_count
    print("Test: All filters can be cleared")


def test_sort_by_price_ascending(page):
    """ Test to products can be sorted by price from low to high """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Find the unfiltered, unsorted prices list
    unsorted_prices = page.locator(PRODUCT_PRICE).all_text_contents()

    # Sort the unsorted prices, this is what we expect it to look like later
    sorted_prices_expected = sorted(unsorted_prices, key=lambda x: float(x.replace("$", "")))

    # Apply sorting by price: low to high on the UI
    page.get_by_label("Sort By").click()
    page.get_by_role(ROLE_OPTION, name=SORT_BY_CHOICES[0]).click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    after_sorting_prices = page.locator(PRODUCT_PRICE).all_text_contents()
    assert after_sorting_prices == sorted_prices_expected
    print("Test: Sorting by price in ascending order works as expected")


def test_sort_by_price_descending(page):
    """ Test to products can be sorted by price from high to low """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Find the unfiltered, unsorted prices list
    unsorted_prices = page.locator(PRODUCT_PRICE).all_text_contents()

    # Sort the unsorted prices, this is what we expect it to look like later
    sorted_prices_expected = sorted(unsorted_prices, key=lambda x: float(x.replace("$", "")), reverse=True)

    # Apply sorting by price: high to low on the UI
    page.get_by_label("Sort By").click()
    page.get_by_role(ROLE_OPTION, name=SORT_BY_CHOICES[1]).click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    after_sorting_prices = page.locator(PRODUCT_PRICE).all_text_contents()
    assert after_sorting_prices == sorted_prices_expected
    print("Test: Sorting by price in descending order works as expected")


def test_sort_by_name_alphabetically(page):
    """ Test to products can be sorted by name from A - Z """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Find the unfiltered, unsorted nams list
    unsorted_names = page.locator(PRODUCT_TITLE).all_text_contents()

    # Sort the unsorted names, this is what we expect it to look like later
    # Sorting is not uppder case senstivie in our app
    sorted_names_expected = sorted(unsorted_names, key=lambda x: x.lower())

    # Apply sorting by name: A - Z in the UI
    page.get_by_label("Sort By").click()
    page.get_by_role(ROLE_OPTION, name=SORT_BY_CHOICES[2]).click()
    page.wait_for_timeout(WAIT_TO_LOAD_SHORT)

    after_sorting_names = page.locator(PRODUCT_TITLE).all_text_contents()
    assert after_sorting_names == sorted_names_expected
    print("Test: Sorting by price in ascending order works as expected")


def test_search_a_product(page):
    """ Test to search for a product """
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()

    # Find the unfiltered, unsorted prices list
    unfiltered_names = page.locator(PRODUCT_TITLE).all_text_contents()

    # This is the string we want to search with
    search_string = "book"

    # Find the names which have the search string in them, this is the expected result
    # Searching is not upper case sensitive in our app
    searched_names_expected = []
    for name in unfiltered_names:
        if search_string.lower() in name.lower():
            searched_names_expected.append(name)

    # Locate the searchbar and search something
    search_bar = page.get_by_placeholder("Search...")
    search_bar.click()
    search_bar.fill(search_string)
    search_bar.press("Enter")
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 

    after_searching_names = page.locator(PRODUCT_TITLE).all_text_contents()
    assert after_searching_names == searched_names_expected
    print("Test: Search by name works as expected")


def test_sort_by_and_filtering(page):
    page.goto(PRODUCTS_PAGE_URL)
    page.wait_for_timeout(WAIT_TO_LOAD_LONG) 
    assert page.locator(PRODUCTS_CONTAINER).is_visible()
    
    # add a random combination of filters, ensure it's applied properly
    original_product_count, filtered_product_count, page = create_random_combination_of_filters(page)
    assert filtered_product_count <= original_product_count

    # ensure that after sorting and filter results are as expected
    # choose a random sort by option
    sorted_expected, after_sorting, page = create_random_sort_by_choice(page)
    assert after_sorting == sorted_expected

    print("Test: Random combination of sort by and filtering works as expected")


def test_search_sort_by_filter(page):
    # Carry out a search first
    test_search_a_product(page)

    # ensure sorting and filtering works after a search is made
    # add a random combination of filters, ensure it's applied properly
    original_product_count, filtered_product_count, page = create_random_combination_of_filters(page)
    assert filtered_product_count <= original_product_count

    # ensure that after sorting and filter results are as expected
    # choose a random sort by option
    sorted_expected, after_sorting, page = create_random_sort_by_choice(page)
    assert after_sorting == sorted_expected
    print("Test: Random combination of search, sort by and filtering works as expected")
