from selenium.common.exceptions import NoSuchElementException


def click_through_js(driver, element):
    driver.execute_script("arguments[0].click();", element)


def is_element_present(driver, by, value):
    """
    Checks if the passed in selectors is present or not

    :param driver: WebDriver
    :param by:
    :param value:
    :return: True if found, False if not found (NoSuchElementException is raised)
    """
    try:
        driver.find_element(by=by, value=value)
    except NoSuchElementException:
        return False
    return True
