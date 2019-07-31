from urllib.parse import urlsplit, urlunsplit

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from .settings import CHROMEDRIVER


class ChromeBrowser(object):
    def __init__(self, headless=False):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("headless")

        self.driver = webdriver.Chrome(
            chrome_options=options, executable_path=CHROMEDRIVER
        )

    @property
    def base_url(self):
        parsed_url = urlsplit(self.driver.current_url)
        base_url = (parsed_url.scheme, parsed_url.netloc, "", "", "")

        return urlunsplit(base_url)

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def page_source(self):
        return self.driver.page_source

    @property
    def url_query_string(self):
        parsed_url = urlsplit(self.driver.current_url)

        return parsed_url.query

    def open_url(self, url):
        self.driver.get(url)

    def wait_factory(self, timeout):
        return WebDriverWait(self.driver, timeout)
