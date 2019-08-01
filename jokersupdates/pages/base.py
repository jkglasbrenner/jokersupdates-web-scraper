from abc import ABCMeta, abstractmethod

from bs4 import BeautifulSoup


class BasePage(metaclass=ABCMeta):
    def __init__(self, browser):
        self._browser = browser
        self._page_source = None
        self._soup = None

    @property
    def base_url(self):
        return self._browser.base_url

    @property
    def current_url(self):
        return self._browser.current_url

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    def driver(self):
        return self._browser.driver

    @property
    def page_source(self):
        if self._page_source is not None:
            return self._page_source

        self._cache_page_source()

        return self._page_source

    @property
    def soup(self):
        if self._soup is not None:
            return self._soup

        self._cache_soup()

        return self._soup

    @property
    def url_query_string(self):
        return self._browser.url_query_string

    def clear_cache(self):
        self._page_source = None
        self._soup = None

    def open_url(self, url):
        self.clear_cache()
        self._browser.open_url(url)

    def wait_factory(self, timeout):
        return self._browser.wait_factory(timeout)

    def _cache_page_source(self):
        self._page_source = self._browser.page_source

    def _cache_soup(self):
        self._soup = BeautifulSoup(self.page_source, "lxml")
