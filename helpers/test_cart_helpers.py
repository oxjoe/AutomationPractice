import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators.general_locators import CART_DROPDOWN_COUNT


def verify_cart_dropdown_text(driver, number_of_items_in_cart):
    """
    Verifies the number of products in the top right cart dropdown

    :param driver: WebDriver
    :param number_of_items_in_cart: Integer
    :return: None
    """
    # Figures out what cart text should be shown depending on the number of items in the cart. expected_cart_text
    # could also be passed in as a tuple for test data parameterized fixtures but putting it here reduces test data
    # duplication.
    if number_of_items_in_cart == 0:
        expected_cart_text = "Cart (empty)"
    elif number_of_items_in_cart == 1:
        expected_cart_text = f"Cart {number_of_items_in_cart} Product"
    else:
        expected_cart_text = f"Cart {number_of_items_in_cart} Products"

    # Wait for the cart dropdown to be updated since Selenium checks it before AJAX has time to complete
    try:
        element = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                CART_DROPDOWN_COUNT,
                expected_cart_text))
        # If text is present then assert element/true
        assert element
    except TimeoutException:
        pytest.fail("Cart Dropdown did not show the expected text.")
