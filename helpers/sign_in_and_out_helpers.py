from helpers.goto_page_helpers import goto_sign_in_page
from pages.SignInPage import SignInPage
from testdata.test_data import get_test_user_login


def sign_in_as_a_test_user(driver):
    """
    Will complete the sign in process for a hardcoded test user

    :param driver: WebDriver
    :return: None
    """
    (email, password) = get_test_user_login()
    sign_in_helper(driver, email, password)


def sign_in_helper(driver, email, password):
    """
    Will try to login with the passed in user credentials

    :param driver: WebDriver
    :param email: Text
    :param password: Text
    :return: None
    """
    goto_sign_in_page(driver)

    sign_in = SignInPage(driver)
    sign_in.enter_email(email)

    sign_in.enter_password(password)
    sign_in.click_sign_in_button()
