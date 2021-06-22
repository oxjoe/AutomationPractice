from base.base import Base
from helpers.selenium_helpers import is_element_present
from helpers.sign_in_and_out_helpers import sign_in_as_a_test_user
from locators.general_locators import LOG_OUT_BUTTON, LOG_IN_BUTTON


class TestSignOut(Base):
    # In order to test sign out, the user must be logged in. So instead of logging in through the UI via Selenium,
    # an alternative could be to use Cookies to save the login from a previous instance?
    def test_sign_out_success(self):
        driver = self.driver
        sign_in_as_a_test_user(driver)

        log_out_button = driver.find_element(*LOG_OUT_BUTTON)
        log_out_button.click()

        assert is_element_present(driver, *LOG_IN_BUTTON)

    def test_if_no_one_is_signed_in_then_sign_out_button_is_not_present(self):
        driver = self.driver
        # Verify that the log out button is NOT present since there's no one currently logged in.
        assert not is_element_present(driver, *LOG_OUT_BUTTON)
