from selenium.webdriver.common.by import By


class SignInPage:
    email_input = (By.ID, "email")
    password_input = (By.ID, "passwd")
    sign_in_button = (By.ID, "SubmitLogin")

    def __init__(self, driver):
        self.driver = driver

    def enter_email(self, email):
        self.driver.find_element(*self.email_input).clear()
        self.driver.find_element(*self.email_input).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_sign_in_button(self):
        self.driver.find_element(*self.sign_in_button).click()
