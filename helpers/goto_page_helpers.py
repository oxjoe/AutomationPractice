from locators.general_locators import LOG_IN_BUTTON, WOMEN_TAB, LIST_VIEW_BUTTON, GRID_VIEW_BUTTON


def goto_women_page(driver):
    """
    Clicks on the WOMEN tab in the nav bar

    :param driver: WebDriver
    :return: None
    """
    driver.find_element(*WOMEN_TAB).click()


def goto_sign_in_page(driver):
    """
    Clicks on the Sign In button in the nav bar

    :param driver: WebDriver
    :return: None
    """
    driver.find_element(*LOG_IN_BUTTON).click()


def switch_to_list_view(driver):
    """
    Finds the list view button on the page and clicks it

    :param driver: WebDriver
    :return: None
    """
    driver.find_element(*LIST_VIEW_BUTTON).click()


def switch_to_grid_view(driver):
    """
    Finds the grid view button on the page and clicks it

    :param driver: WebDriver
    :return: None
    """
    driver.find_element(*GRID_VIEW_BUTTON).click()
