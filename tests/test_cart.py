import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from base.base import Base
from helpers.goto_page_helpers import switch_to_grid_view, goto_women_page, switch_to_list_view
from helpers.multiple_products_page_helpers import get_products_count_in_header_text
from helpers.selenium_helpers import click_through_js
from helpers.test_cart_helpers import verify_cart_dropdown_text
from locators.general_locators import CART_DROPDOWN_COUNT
from pages.CartPopupPage import CartPopupPage
from pages.GridAndListPage import GridAndListPage


class TestCart(Base):

    @staticmethod
    def add_to_cart_and_verify_successfully_added_and_product_name_in_popup(driver, num_of_items_to_add_to_cart,
                                                                            skip_asserts=False):
        """
        Adds N number of items to the cart
        Verifies that the string "Product is successfully added to the cart in the cart" appears in the popup
        Verifies that the product name in the grid/list view matches the product name in the cart popup
        Clicks on continue

        :param driver: WebDriver
        :param num_of_items_to_add_to_cart: Integer
        :param skip_asserts: Boolean
        :return: None
        """
        grid_and_list_page = GridAndListPage(driver)
        # Get the li element of each product into a list
        items_list = grid_and_list_page.get_product_list_elements()

        # Count the total number of products shown to the user on screen
        total_item_count = len(items_list)

        if num_of_items_to_add_to_cart > total_item_count:
            pytest.skip(f"Invalid test data. The number of items on the page is "
                        f"{total_item_count} which is < {num_of_items_to_add_to_cart} (aka the test data that was "
                        f"inputted).")

        # Using enumerate so I can use the index later on to find the specific product element
        for i, item in enumerate(items_list):
            if i == num_of_items_to_add_to_cart:
                break
            # Need ActionChains to trigger the AJAX call by hovering over the product
            action = ActionChains(driver)
            action.move_to_element(item).perform()

            # The data-id-product on the DOM is not 0 based so start I have to increment by 1
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, f'a[data-id-product="{i + 1}"]')

            # Clicking on the Add to cart button using Selenium was very inconsistent, so this uses JS to
            # directly click on it as a workaround. HOWEVER this is not good practice
            # since a real user would do no such thing. Basically this https://stackoverflow.com/a/37880313/7688714
            click_through_js(driver, add_to_cart_button)

            cart_popup_page = CartPopupPage(driver)
            # If I do not want to skip asserts then do the asserts
            if not skip_asserts:
                grid_and_list_view_product_name = item.find_element(By.CSS_SELECTOR, "a.product-name").text
                cart_product_name = cart_popup_page.get_product_name_text()

                # Additional asserts such as product cost, etc... could be added here
                assert grid_and_list_view_product_name == cart_product_name
                assert cart_popup_page.get_product_successfully_added_text().strip() \
                       == "Product successfully added to your shopping cart"

            cart_popup_page.click_continue_shopping_button()

    # It may make more sense to split the parameterization into separate test cases, however since these are VERY
    # similar scenarios I chose to group them into one. If one of the passed in numbers for the test data is > than
    # the amount of products on the page, then pytest will skip that specific number (e.g. see 25 in the fixture).
    @pytest.mark.parametrize("num_of_items_to_add_to_cart", [0, 1, 3, 25])
    def test_add_items_to_cart_through_grid_view_and_verify_number_of_products_in_cart(self,
                                                                                       num_of_items_to_add_to_cart):
        driver = self.driver
        goto_women_page(driver)
        # Grid view should be the default however the system could change that at any point without me knowing so
        # just making sure it doesn't.
        switch_to_grid_view(driver)
        self.add_to_cart_and_verify_successfully_added_and_product_name_in_popup(driver, num_of_items_to_add_to_cart)
        verify_cart_dropdown_text(driver, num_of_items_to_add_to_cart)

    # This is basically a duplicate of
    # 'test_add_items_to_cart_through_grid_view_and_verify_number_of_products_in_cart' but the list version
    @pytest.mark.parametrize("num_of_items_to_add_to_cart", [0, 1, 3, 50])
    def test_add_items_to_cart_through_list_view_and_verify_number_of_products_in_cart(self,
                                                                                       num_of_items_to_add_to_cart):
        driver = self.driver
        goto_women_page(driver)
        switch_to_list_view(driver)
        self.add_to_cart_and_verify_successfully_added_and_product_name_in_popup(driver, num_of_items_to_add_to_cart)
        verify_cart_dropdown_text(driver, num_of_items_to_add_to_cart)

    @pytest.mark.parametrize("num_of_items_to_add_to_cart", [3])
    def test_remove_items_from_cart_dropdown(self, num_of_items_to_add_to_cart):
        driver = self.driver
        goto_women_page(driver)
        switch_to_grid_view(driver)
        # I want to skip the asserts since I only care about adding the items to the cart
        self.add_to_cart_and_verify_successfully_added_and_product_name_in_popup(driver, num_of_items_to_add_to_cart,
                                                                                 True)

        # Element of the cart count on the top right
        cart_count_element = driver.find_element(*CART_DROPDOWN_COUNT)
        # Need ActionChains to trigger the AJAX call by hovering over the product
        action = ActionChains(driver)
        action.move_to_element(cart_count_element).perform()
        # Get each items delete button (i.e. the small x in the circle) in the cart dropdown
        x_items_list = driver.find_elements(By.CSS_SELECTOR,
                                            "#header div.shopping_cart a[class='ajax_cart_block_remove_link']")

        for item in x_items_list:
            # Delete the item
            item.click()
            # Since I just deleted an item from above, subtract 1 to ge the current number of items in the cart.
            num_of_items_in_cart = num_of_items_to_add_to_cart - 1
            verify_cart_dropdown_text(driver, num_of_items_in_cart)

    def test_total_count_of_items_matches_headers(self):
        driver = self.driver
        goto_women_page(driver)
        switch_to_grid_view(driver)

        grid_and_list_page = GridAndListPage(driver)
        items_list = grid_and_list_page.get_product_list_elements()

        items_count = len(items_list)
        total_item_count_in_header = get_products_count_in_header_text(driver).strip()
        assert total_item_count_in_header == f"There are {items_count} products."

        top_of_grid_text = grid_and_list_page.get_products_count_on_top_of_grid_and_list_text().strip()
        final_grid_text_format = " ".join(top_of_grid_text.split())
        assert final_grid_text_format == f"Showing 1 - {items_count} of {items_count} items"
