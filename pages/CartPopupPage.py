from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CartPopupPage:
    product_successfully_added = (By.CSS_SELECTOR, "#layer_cart > div.clearfix > div.layer_cart_product > h2")
    continue_shopping_button = (By.CSS_SELECTOR, "span[title='Continue shopping']")
    product_name = (By.CSS_SELECTOR, "#layer_cart #layer_cart_product_title")

    def __init__(self, driver):
        self.driver = driver

    def get_product_successfully_added_text(self):
        element = self.driver.find_element(*self.product_successfully_added)
        return element.get_attribute('innerText')

    def click_continue_shopping_button(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_shopping_button))
        element.click()

    def get_product_name_text(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.product_name))
        return element.text
