import re
from uuid import NAMESPACE_URL

from jokersupdates.locators import BaseUrl, PostList
from jokersupdates.transformers import (
    DataTransformer,
    DateTimeNormalizer,
    IndentWidthNormalizer,
    IntegerNormalizer,
    PostNumberNormalizer,
    StringNormalizer,
    UrlBuilder,
    UUIDBuilder,
)

from .base import (
    BaseElementListFindElement,
    BaseElementListIndexElement,
    BasePageGetQueryParameter,
)


class SubjectElement(BaseElementListIndexElement):
    index = 0


class AuthorElement(BaseElementListIndexElement):
    index = 1


class ViewsElement(BaseElementListIndexElement):
    index = 2


class RepliesElement(BaseElementListIndexElement):
    index = 3


class DateTimeElement(BaseElementListIndexElement):
    index = 4


class IndentElement(BaseElementListFindElement):
    index = 0
    locator = PostList.REPLY_INDENT


class BoardParameter(BasePageGetQueryParameter):
    qs_parameter = PostList.QS_BOARD


class PostElement(object):
    _board = BoardParameter()
    _subject = SubjectElement()
    _author = AuthorElement()
    _views = ViewsElement()
    _replies = RepliesElement()
    _posted_on = DateTimeElement()
    _indent_width = IndentElement()
    _datetime_normalizer = DataTransformer(DateTimeNormalizer())
    _integer_normalizer = DataTransformer(IntegerNormalizer())
    _indent_width_normalizer = DataTransformer(IndentWidthNormalizer())
    _post_number_normalizer = DataTransformer(PostNumberNormalizer())
    _string_normalizer = DataTransformer(StringNormalizer())
    _uuid_builder = DataTransformer(UUIDBuilder(NAMESPACE_URL))

    def __init__(self, element, url_query_string):
        self.element = element
        self.element_list = [x for x in element.contents if not isinstance(x, str)]
        self.url_query_string = url_query_string
        self._nt_regexp = re.compile(r"NT\s*$")

    @property
    def post_id(self):
        url_builder = self._url_builder_factory()
        post_url = url_builder.transform(self.number)
        return self._uuid_builder.transform(post_url)

    @property
    def board(self):
        if self._board:
            board_string = self._board.pop()
            return self._string_normalizer.transform(board_string)

        return None

    @property
    def number(self):
        postrow_string = self.element["id"]
        return self._post_number_normalizer.transform(postrow_string)

    @property
    def subject(self):
        subject_string = self._subject.get_text().strip()
        return self._string_normalizer.transform(subject_string)

    @property
    def author(self):
        author_string = self._author.get_text().strip()
        return self._string_normalizer.transform(author_string)

    @property
    def views(self):
        views_string = self._views.get_text().strip()
        return self._integer_normalizer.transform(views_string)

    @property
    def replies(self):
        replies_string = self._replies.get_text().strip()
        return self._integer_normalizer.transform(replies_string)

    @property
    def posted_on(self):
        posted_on_string = self._posted_on.get_text().strip()
        return self._datetime_normalizer.transform(posted_on_string)

    @property
    def indent_width(self):
        return self._indent_width_normalizer.transform(self._indent_width)

    @property
    def more_text_in_body(self):
        if self._nt_regexp.search(self.subject):
            return False

        else:
            return True

    def _url_builder_factory(self):
        return DataTransformer(UrlBuilder(BaseUrl.SHOWTHREADED, self.board))
