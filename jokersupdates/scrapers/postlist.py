from jokersupdates.locators import BaseUrl
from jokersupdates.schema import DataValidator
from jokersupdates.schema.scrapers import PostListScrapedData

from .base import BaseScraper
from .showthreaded import ShowThreadedScraper


class PostListScraper(BaseScraper):

    base_url = BaseUrl.POSTLIST

    def __init__(self, board, headless=True):
        super().__init__(headless=headless)
        self.board = board
        self._data = PostListScrapedData()
        self._page = self.postlist_page_factory(self.browser_factory())

    @property
    def data(self):
        data = self._data
        validator = DataValidator(data)

        return validator.normalize(strict=True)

    def parse(self):
        data = self.parse_single_page()
        self._data.postlist.extend(data)

        while self._page.next_button:
            self.wait(0.90, 6.0, 2.0)
            self._page.click_next_button()
            self.parse_single_page()
            self._data.postlist.extend(data)

    def parse_single_page(self):
        data = self._page.data
        self._process_scraped_posts(data)

        return data

    def open(self):
        url = self.build_url(board=self.board, number=None)
        self._page.open_url(url)

    def _process_scraped_posts(self, data):
        for postrow in data:
            self._fetch_posted_on_if_missing(postrow)

    def _fetch_posted_on_if_missing(self, postrow):
        if postrow.posted_on is None:
            showthreaded_scraper = ShowThreadedScraper()
            data = showthreaded_scraper.parse_single_page(postrow.board, postrow.number)
            postrow.posted_on = data.posted_on
