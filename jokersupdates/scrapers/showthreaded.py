from jokersupdates.locators import BaseUrl
from jokersupdates.schema import DataValidator
from jokersupdates.schema.scrapers import ShowThreadedScrapedData

from .base import BaseScraper


class ShowThreadedScraper(BaseScraper):

    base_url = BaseUrl.SHOWTHREADED

    def __init__(self, headless=True):
        super().__init__(headless=headless)
        self._queue = []
        self._scraped_pages = set()
        self._data = ShowThreadedScrapedData()
        self._page = self.showthreaded_page_factory(self.browser_factory())

    @property
    def data(self):
        data = self._data
        validator = DataValidator(data)

        return validator.normalize(strict=True)

    def add_to_queue(self, board, number):
        if not self._was_page_scraped(board, number):
            self._queue.append({"board": board, "number": number})

    def parse(self):
        while self._stack:
            parameters = self._queue.pop(0)

            if not self._was_page_scraped(**parameters):
                data = self.parse_single_page(**parameters)
                self._data.showthreaded.extend(data)
                self._add_to_scraped_pages(**parameters)
                self.wait(0.95, 5.0, 1.0)

    def parse_single_page(self, board, number):
        url = self.build_url(board=board, number=number)
        self._page.open_url(url)

        return self._page.data

    def _add_to_scraped_pages(self, board, number):
        parameters = self._page_parameters_factory(board, number)
        self._scraped_pages.add(parameters)

    def _was_page_scraped(self, board, number):
        parameters = self._page_parameters_factory(board, number)
        return parameters in self._scraped_pages

    @staticmethod
    def _page_parameters_factory(board, number):
        return (board, number)
