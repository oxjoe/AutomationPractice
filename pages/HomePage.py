from selenium.webdriver.common.by import By


class HomePage:
    search_input = (By.ID, "search_query_top")
    search_button = (By.CSS_SELECTOR, "button[name='submit_search']")

    def __init__(self, driver):
        self.driver = driver

    def input_text_into_search(self, text):
        self.driver.find_element(*self.search_input).clear()
        self.driver.find_element(*self.search_input).send_keys(text)

    def click_on_search_button(self):
        self.driver.find_element(*self.search_button).click()
