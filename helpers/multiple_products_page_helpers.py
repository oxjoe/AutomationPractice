from locators.general_locators import HEADING_COUNTER


def get_products_count_in_header_text(driver):
    """
    Returns the text that is on the top right of the page when viewing products in list or grid view

    :param driver: WebDriver
    :return: String
    """
    element = driver.find_element(*HEADING_COUNTER)
    return element.text
