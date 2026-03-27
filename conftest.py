import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

driver = None


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', help='browser selection', default='chrome')


@pytest.fixture(scope="function")
def browser_example(request):
    global driver
    service_obj_chrome = Service(ChromeDriverManager().install())
    browsers_options_chrome = Options()
    browsers_options_chrome.add_argument("--window-size=1920,1080")
    service_obj_firefox = FirefoxService(GeckoDriverManager().install())
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        driver = webdriver.Chrome(service=service_obj_chrome, options=browsers_options_chrome)
    if browser_name == "firefox":
        driver = webdriver.Firefox(service=service_obj_firefox)
    driver.implicitly_wait(5)
    driver.get("https://www.target.com/")
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
            file_name = os.path.join(reports_dir, report.nodeid.replace("::", "_").replace("/", "_") + ".png")
            print("file name is " + file_name)
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extras = extra


def _capture_screenshot(file_name):
    driver.get_screenshot_as_file(file_name)
