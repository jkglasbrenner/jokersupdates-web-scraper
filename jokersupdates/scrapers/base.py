import random
import time
from abc import ABCMeta, abstractmethod

from jokersupdates import ChromeBrowser
from jokersupdates.pages import PostListPage, ShowThreadedPage
from jokersupdates.transformers import DataTransformer, UrlBuilder


class BaseScraper(metaclass=ABCMeta):

    base_url = None

    def __init__(self, headless=True):
        self.headless = headless

    def build_url(self, board, number):
        url_builder = self.url_builder_factory(base_url=self.base_url, board=board)

        return url_builder.transform(number)

    def browser_factory(self):
        return ChromeBrowser(self.headless)

    @abstractmethod
    def parse(self):
        pass

    @staticmethod
    def postlist_page_factory(browser):
        return PostListPage(browser=browser)

    @staticmethod
    def showthreaded_page_factory(browser):
        return ShowThreadedPage(browser=browser)

    @staticmethod
    def url_builder_factory(base_url, board):
        return DataTransformer(UrlBuilder(base_url, board))

    @staticmethod
    def wait(wait_probability, mu, sigma):
        if random.random() < wait_probability:
            seconds = random.gauss(mu=mu, sigma=sigma)

            if seconds > 0:
                time.sleep(seconds)
