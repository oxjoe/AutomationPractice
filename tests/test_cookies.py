from base.base import Base
from helpers.selenium_helpers import is_element_present
from helpers.sign_in_and_out_helpers import sign_in_as_a_test_user
from locators.general_locators import LOG_IN_BUTTON


# There are a lot of tests for cookies that could actually be done.
# Some other test cases for cookie testing that could be implemented
# https://www.softwaretestinghelp.com/website-cookie-testing-test-cases/
class TestCookies(Base):

    def test_corrupt_cookie_value_after_sign_in(self):
        driver = self.driver
        sign_in_as_a_test_user(driver)

        cookies = driver.get_cookies()
        # From what I can tell when a user is logged in, only one cookie is kept. I need this assert to make sure that
        # I get the first cookie.
        assert len(cookies) == 1

        cookie = cookies[0]
        # Update the cookie with an invalid value in order to corrupt it
        cookie.update({'value': 'invalid_cookie_value'})

        driver.delete_all_cookies()
        driver.add_cookie(cookie)
        driver.refresh()

        assert is_element_present(driver, *LOG_IN_BUTTON)

    def test_delete_cookies_after_sign_in(self):
        driver = self.driver
        sign_in_as_a_test_user(driver)

        driver.delete_all_cookies()
        driver.refresh()

        assert is_element_present(driver, *LOG_IN_BUTTON)

    def test_cookie_will_expire_at_some_point(self):
        driver = self.driver
        sign_in_as_a_test_user(driver)

        cookies = driver.get_cookies()
        assert len(cookies) == 1
        # Get the expiry value from the cookie
        expiry_value = cookies[0].get("expiry")

        # Verify that this cookie will simply expire AT SOME POINT since most cookies on sites have an expiration
        # dates on them. A stronger check would be to verify that it expires at a certain time as per some requirement.
        assert isinstance(expiry_value, int)
