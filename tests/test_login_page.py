from time import sleep

from pages.login_page import LoginPage


def test_e2e(browser_example):
    driver = browser_example
    sleep(3)
    login_page = LoginPage(driver)
    login_page.login("henoda9754@qvmao.com", "1q2w3e4!")