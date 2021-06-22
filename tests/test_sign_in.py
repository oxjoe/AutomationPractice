import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from base.base import Base
from helpers.sign_in_and_out_helpers import sign_in_helper


class TestSignIn(Base):
    # Since there's only two logins, I didn't separate out test data from the code. If there was more test data then
    # I would store the data in a some external source like CSV. I think I could pass it to the fixture using
    # pytest_generate_tests(metafunc) or use some pytest plugin.
    @pytest.mark.parametrize("email, password, name", [('xigoy27304@greenkic.com', 'xigoy27304', 'John Lennon'),
                                                       ('comonor619@moxkid.com', 'comonor619', 'Paul McCartney')
                                                       ])
    def test_sign_in_success(self, email, password, name):
        driver = self.driver
        # Helper to sign the user in
        sign_in_helper(driver, email, password)
        # Verifies the name on the top right after a user signs in
        name_on_site = driver.find_element(By.CLASS_NAME, "account")
        assert name_on_site.text == name
        assert driver.title == "My account - My Store"

        # For the below assertions, if I had to verify more elements I'd put them in a page object instead.
        # account_header has to be capitalized bc it's a h1 element
        account_header = "MY ACCOUNT"
        assert driver.find_element(By.CSS_SELECTOR, "h1.page-heading").text == account_header

        info_account = "Welcome to your account. Here you can manage all of your personal information and orders."
        assert driver.find_element(By.CSS_SELECTOR, "p.info-account").text == info_account

    # Same comment here about the externalizing test data as the previous test.
    @pytest.mark.parametrize("email, password", [("testing@test.com", "invalid_password"),
                                                 ("blah_test@blah1234.com", "invalid_email")
                                                 ])
    # This test just checks for the authentication banner. Other tests such as checking for what the error actually
    # says (i.e. if I entered an invalid password then make sure banner says Invalid password) could also be
    # implemented.
    def test_sign_in_failure(self, email, password):
        driver = self.driver
        sign_in_helper(driver, email, password)
        # Verifies that an error banner will pop up since the user login is incorrect
        try:
            assert driver.find_element(By.CSS_SELECTOR, "div.alert.alert-danger").is_displayed()
        except NoSuchElementException as e:
            print("Invalid authentication banner did not pop up.")
            print(e)

        assert driver.title == "Login - My Store"
