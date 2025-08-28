import config.config as cfg
from selenium.webdriver.common.by import By

class LoginPage:
    """Page Object cho màn hình đăng nhập"""

    def __init__(self, driver):
        self.driver = driver

        self.email_input = (By.ID, "phone_number")
        self.password_input = (By.ID, "password")
        self.login_button = (By.XPATH, "//span[contains(text(),'Đăng nhập')]")

    def login(self, username=cfg.USERNAME, password=cfg.PASSWORD):
        """Thực hiện đăng nhập"""
        self.driver.find_element(*self.email_input).send_keys("huynk.software@gmail.com")
        self.driver.find_element(*self.password_input).send_keys("111111a@A")
        self.driver.find_element(*self.login_button).click()