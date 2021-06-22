import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


class Base:
    # Type hint so PyCharm will stop bothering me to move self.driver to the _init_ method
    driver: WebDriver

    @pytest.fixture(autouse=True)
    def set_up(self):
        url = "http://automationpractice.com/index.php"

        print("INITIATING CHROME DRIVER.")
        # Using ChromeDriverManager, which is a package that will automatically download the latest driver for me
        # Other browsers should also work. See here: https://github.com/SergeyPirogov/webdriver_manager
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(executable_path="/chromedriver.exe")
        print("TEST IS STARTING.")
        # Set timeout for Selenium to find an element
        self.driver.implicitly_wait(10)
        # Clear cookies at the start (just in case)
        self.driver.delete_all_cookies()
        # Probably not needed but doesn't hurt to check
        assert len(self.driver.get_cookies()) == 0

        self.driver.get(url)
        self.driver.maximize_window()

        yield self.driver

        if self.driver is not None:
            print("TEST HAS ENDED.")
            self.driver.close()
            self.driver.quit()
