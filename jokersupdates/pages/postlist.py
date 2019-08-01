from selenium.common.exceptions import NoSuchElementException

from jokersupdates.elements.base import BasePageFindElement, BaseSoupFindElements
from jokersupdates.elements.postlist import PostElement
from jokersupdates.locators import PostList
from jokersupdates.schema import DataValidator
from jokersupdates.schema.pages import PostData

from .base import BasePage


class NextButtonElement(BasePageFindElement):
    locator = PostList.NEXT_BUTTON


class PreviousButtonElement(BasePageFindElement):
    locator = PostList.PREVIOUS_BUTTON


class PostRowElements(BaseSoupFindElements):
    locator = PostList.POST_ROWS


class PostListPage(BasePage):

    _next_button = NextButtonElement()
    _previous_button = PreviousButtonElement()
    post_row_elements = PostRowElements()

    def __init__(self, browser):
        super().__init__(browser)
        self._postlist = None

    @property
    def data(self):
        postlist_data = [self._normalize_post_data(x) for x in self.postlist]
        return postlist_data

    @property
    def next_button(self):
        try:
            next_button = self._next_button

            return next_button

        except NoSuchElementException:
            return None

    @property
    def previous_button(self):
        try:
            previous_button = self._previous_button

            return previous_button

        except NoSuchElementException:
            return None

    @property
    def postlist(self):
        if self._postlist is not None:
            return self._postlist

        self._cache_postlist()

        return self._postlist

    def clear_cache(self):
        super().clear_cache()
        self._postlist = None

    def click_next_button(self):
        next_button = self.next_button

        if next_button:
            self.clear_cache()
            next_button.click()

    def click_previous_button(self):
        previous_button = self.previous_button

        if previous_button:
            self.clear_cache()
            previous_button.click()

    def _cache_postlist(self):
        self._postlist = [
            PostElement(x, self.url_query_string) for x in self.post_row_elements
        ]

    def _normalize_post_data(self, post):
        data = self._post_data_factory(post)
        validator = DataValidator(data)

        return validator.normalize(strict=True)

    @staticmethod
    def _post_data_factory(post):
        post_data = PostData(
            post_id=post.post_id,
            board=post.board,
            number=post.number,
            subject=post.subject,
            author=post.author,
            views=post.views,
            replies=post.replies,
            posted_on=post.posted_on,
            indent_width=post.indent_width,
        )

        return post_data
