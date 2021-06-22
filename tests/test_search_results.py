import pytest
from selenium.webdriver.common.by import By

from base.base import Base
from helpers.goto_page_helpers import switch_to_list_view
from helpers.multiple_products_page_helpers import get_products_count_in_header_text
from helpers.selenium_helpers import is_element_present
from pages.HomePage import HomePage
from pages.SearchResultsPage import SearchResultsPage


class TestSearchResults(Base):

    @staticmethod
    def search_text_from_home_page(driver, to_be_searched):
        home_page = HomePage(driver)
        home_page.input_text_into_search(to_be_searched)
        home_page.click_on_search_button()

    @pytest.mark.parametrize("to_be_searched", ["shirt",
                                                "BLOUSE"])
    def test_search_bar_and_search_header_match(self, to_be_searched):
        driver = self.driver
        self.search_text_from_home_page(driver, to_be_searched)

        results_page = SearchResultsPage(driver)
        # This is the search bar where user inputs what to search
        search_text = results_page.get_search_input_text()
        # This is the header that should show a duplicate of what the user searched for
        header_text = results_page.get_search_header_text()

        assert to_be_searched == search_text
        assert header_text.lower() == f'"{search_text}"'.lower()

    # An iffy edge case (which is not included) is the following string (notice the two quotes) ""Dress"" The string
    # technically doesn't have any matches but the system behaves as if there are no quotes. Maybe something to do
    # with direct searches or something.
    @pytest.mark.parametrize("to_be_searched", ["Men"])
    def test_no_results_found(self, to_be_searched):
        driver = self.driver
        self.search_text_from_home_page(driver, to_be_searched)

        assert get_products_count_in_header_text(driver) == "0 results have been found."
        # Checks just to make sure that the alert box is present.
        assert is_element_present(driver, By.CSS_SELECTOR, "#center_column > p")

    # This test is expected to have one failure.
    @pytest.mark.parametrize("to_be_searched", ["top",
                                                "shirt",
                                                pytest.param("dress", marks=pytest.mark.xfail(
                                                    reason="dress is expected to fail this test because the system "
                                                           "counts Faded Short Sleeve T-shirts and Blouse as a dress "
                                                           "for some reason"))
                                                ])
    def test_item_names_or_descriptions_contain_the_searched_term(self, to_be_searched):
        driver = self.driver
        self.search_text_from_home_page(driver, to_be_searched)

        switch_to_list_view(driver)

        # Find all the product names and product descriptions
        product_name_el_list = driver.find_elements(By.CSS_SELECTOR, "#center_column a.product-name")
        product_desc_el_list = driver.find_elements(By.CSS_SELECTOR, "#center_column p.product-desc")

        # Loop through the product names and descriptions and see if the string that was entered in the search bar is
        # in EITHER of them. Bc if the product name has the string and the description doesn't have it or vice versa,
        # that's okay since the product as a whole has the string somewhere.
        for name, desc in zip(product_name_el_list, product_desc_el_list):
            name_text = name.text.lower()
            desc_text = desc.text.lower()
            assert to_be_searched.lower() in name_text or to_be_searched.lower() in desc_text, \
                f"The search term: {to_be_searched.lower()} was not found in either the product name or description."
