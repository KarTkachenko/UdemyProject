import pytest

from pages.header import Header

@pytest.mark.smoke
def test_header(browser_example):
    driver = browser_example
    header = Header(driver)
    header.verify_categories()
    header.verify_url()
    header.verify_titles()
    pass