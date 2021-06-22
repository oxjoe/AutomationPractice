from selenium.webdriver.common.by import By


class GridAndListPage:
    """ This is the page where all the products are displayed in either grid or list view """
    products_count_on_top_of_grid = (By.CLASS_NAME, "product-count")
    product_list = (By.CSS_SELECTOR, "ul.product_list li.ajax_block_product")

    def __init__(self, driver):
        self.driver = driver

    def get_products_count_on_top_of_grid_and_list_text(self):
        return self.driver.find_element(*self.products_count_on_top_of_grid).text

    def get_product_list_elements(self):
        return self.driver.find_elements(*self.product_list)
