from time import sleep, time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.browser_utils import BrowserUtils


class Header(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        # locators
        self.logo = (By.XPATH, '//a[@aria-label="Target home"][1]')

    def aria_label_locator(self, value):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, f'//a[@aria-label="{value}"]')))

    def categories_locator(self, value):
        return self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f'//div[contains(@class, "menuBody")]//span[text()="{value}"]')))

    def url_checking(self, url):
        return self.wait.until(EC.url_contains(url), message=f"URL не содержит {url}")

    def title_checking(self, expected_title):
        try:
            self.wait.until(EC.title_is(expected_title))
            return True
        except TimeoutException:
            actual_title = self.driver.title
            raise AssertionError(
                f"Title mismatch!\n"
                f"Expected: '{expected_title}'\n"
                f"Actual:   '{actual_title}'"
            )

    def all_categories(self):
        return ['New Arrivals', 'Easter', 'Clothing, Shoes & Accessories',
                'Home', 'Kitchen & Dining', 'Outdoor Living & Garden', 'Furniture',
                'Grocery', 'Household Essentials', 'Baby', 'Beauty', 'Personal Care',
                'Health', 'Wellness', 'Backpacks & Luggage', 'Sports & Outdoors',
                'Toys', 'Electronics', 'Video Games', 'Movies, Music & Books',
                'School & Office Supplies', 'Party Supplies', 'Gift Ideas',
                'Gift Cards', 'Pets', 'Ulta Beauty at Target', 'Shop by Community',
                'Target Optical', 'Deals', 'Clearance']

    def urls_categories(self):
        return {
            'New Arrivals': 'https://www.target.com/c/what-s-new',
            'Wellness': 'https://www.target.com/c/health-wellbeing',
            'Backpacks & Luggage': 'https://www.target.com/c/luggage',
            'Gift Ideas': 'https://www.target.com/c/gift-ideas',
            'Ulta Beauty at Target': 'https://www.target.com/c/ulta-beauty-at-target',
            'Shop by Community': 'https://www.target.com/c/shop-by-community',
            'Target Optical': 'https://www.target.com/c/target-optical',
            'Deals': 'https://www.target.com/c/top-deals',
            'Clearance': 'https://www.target.com/c/clearance'

        }

    def titles_categories(self):
        return {
            'New Arrivals': 'New Arrivals at Target',
            'Wellness': 'Health & Wellness Essentials : Target',
            'Backpacks & Luggage': 'Luggage : Target',
            'Gift Ideas': 'Gift Ideas - Target',
            'Ulta Beauty at Target': 'Ulta Beauty at Target : Target',
            'Shop by Community': 'Shop by Community : Target',
            'Target Optical': 'Target Optical : Target',
            'Deals': 'Top Deals at Target',
            'Clearance': 'Clearance : Save on Thousands of Clearance Items : Target'

        }

    def verify_categories(self):
        header_locators = ['Categories', 'Deals', 'pickup and delivery']
        for locator in header_locators:
            self.aria_label_locator(locator).is_displayed()
            self.aria_label_locator(locator).is_enabled()
        self.aria_label_locator('Categories').click()
        sleep(2)
        for category in self.all_categories():
            assert self.categories_locator(category).is_displayed(), f"{category} is not displayed!"
            assert self.categories_locator(category).is_enabled(), f"{category} is not enabled!"

        # logo assertion
        assert self.wait.until(EC.presence_of_element_located(self.logo), message="Logo is not displayed!")
        assert self.wait.until(EC.element_to_be_clickable(self.logo), message="Logo is not enabled!")
        self.aria_label_locator('Categories').click()

    def verify_url(self):
        for category, url in self.urls_categories().items():
            self.aria_label_locator('Categories').click()
            scroll_container = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="styles_menuBody___b7tb"]'))
            )
            # scroll container to the category
            self.driver.execute_script("""
                    var container = arguments[0];
                    var element = arguments[1];
                    container.scrollTop = element.offsetTop - container.offsetTop - 50;
                """, scroll_container, self.categories_locator(category))
            sleep(0.5)
            print(f'The category: {category}')
            self.driver.execute_script("arguments[0].click();", self.categories_locator(category))
            self.url_checking(url)

    def verify_titles(self):
        for category, title in self.titles_categories().items():
            self.aria_label_locator('Categories').click()
            scroll_container = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="styles_menuBody___b7tb"]'))
            )
            # scroll container to the category
            self.driver.execute_script("""
                    var container = arguments[0];
                    var element = arguments[1];
                    container.scrollTop = element.offsetTop - container.offsetTop - 50;
                """, scroll_container, self.categories_locator(category))
            sleep(0.5)
            self.driver.execute_script("arguments[0].click();", self.categories_locator(category))
            sleep(0.5)
            print(f'The title: {self.get_title()}')
            self.title_checking(title)

    def verify_searching(self):
        pass
