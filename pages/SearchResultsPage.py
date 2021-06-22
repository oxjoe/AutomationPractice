from selenium.webdriver.common.by import By


class SearchResultsPage:
    search_input = (By.ID, "search_query_top")
    search_header = (By.CSS_SELECTOR, "#center_column > h1 > span.lighter")

    def __init__(self, driver):
        self.driver = driver

    def get_search_input_text(self):
        search_input = self.driver.find_element(*self.search_input)
        return search_input.get_attribute("value")

    def get_search_header_text(self):
        return self.driver.find_element(*self.search_header).text
