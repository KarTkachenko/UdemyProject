from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        self.input_username = (By.XPATH, '//input[@id="username"]')
        self.click_password = (By.XPATH, '//div[@id="password"]')
        self.sign_in_button = (By.XPATH, '//button[text()="Sign in or create account"]')
        self.continue_button = (By.XPATH, '//button[text()="Continue"]')
        self.issue_message = (By.XPATH, '//div[contains(text(), "Something went wrong on our end")]')
        self.keep_sign = (By.XPATH, '//input[@id="keepMeSignedIn"]')
        self.input_password = (By.XPATH, '//input[@id="password"]')
        self.sign_in_password = (By.XPATH, '//button[text()="Sign in with password"]')
        self.skip = (By.XPATH, '//a[text()="Skip"]')
        self.mobile_phone = (By.XPATH, '//label[text()="Mobile phone number (optional)"]')
        self.circle = (By.XPATH, '//span[text()="Maybe later"]')

    def login(self, username, password):
        self.wait.until(EC.presence_of_element_located(self.sign_in_button)).click()
        self.wait.until(EC.presence_of_element_located(self.input_username)).send_keys(username)
        continue_button = self.driver.find_element(*self.continue_button)
        continue_button.click()

        issue_message = self.driver.find_elements(*self.issue_message)
        if issue_message:
            continue_button.click()

        self.driver.find_element(*self.keep_sign).click()
        click_password =  self.wait.until(EC.presence_of_element_located(self.click_password))
        click_password.click()

        self.wait.until(EC.presence_of_element_located(self.input_password)).send_keys(password)
        sign_in_button = self.driver.find_element(*self.sign_in_password)
        sign_in_button.click()

        sleep(2)
        mobile_phone = self.driver.find_elements(*self.mobile_phone)
        issue_message = self.driver.find_elements(*self.issue_message)
        if issue_message:
            sign_in_button.click()
        if mobile_phone:
            self.driver.find_element(*self.skip).click()

        sleep(2)
        circle = self.driver.find_elements(*self.circle)
        if circle:
            circle[0].click()
        # checkin_account
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Hi, Cari"]')),
                   message="No Cari, login is not successfully!!")
