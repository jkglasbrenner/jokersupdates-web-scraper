from uuid import NAMESPACE_URL

from jokersupdates.elements.base import BasePageGetQueryParameter, BaseSoupFindElement
from jokersupdates.elements.showthreaded import (
    ShowThreadedBodyElement,
    ShowThreadedSubjectElement,
)
from jokersupdates.locators import BaseUrl, ShowThreaded
from jokersupdates.schema import DataValidator
from jokersupdates.schema.pages import ShowThreadedData
from jokersupdates.transformers import (
    DataTransformer,
    PostNumberNormalizer,
    UrlBuilder,
    UUIDBuilder,
)

from .base import BasePage


class SubjectTableElement(BaseSoupFindElement):
    locator = ShowThreaded.SUBJECT_TABLE


class TextElement(BaseSoupFindElement):
    locator = ShowThreaded.TEXT


class BoardParameter(BasePageGetQueryParameter):
    qs_parameter = ShowThreaded.QS_BOARD


class NumberParameter(BasePageGetQueryParameter):
    qs_parameter = ShowThreaded.QS_NUMBER


class ShowThreadedPage(BasePage):

    _text = TextElement()
    _subject_table = SubjectTableElement()
    _board = BoardParameter()
    _number = NumberParameter()
    _post_number_normalizer = DataTransformer(PostNumberNormalizer())
    _uuid_builder = DataTransformer(UUIDBuilder(NAMESPACE_URL))

    def __init__(self, browser):
        super().__init__(browser)
        self.showthreaded_body = None
        self.showthreaded_subject = None

    @property
    def board(self):
        if self._board:
            return self._board.pop()

        return None

    @property
    def data(self):
        data = self._showthreaded_data_factory(
            post_id=self.post_id,
            subject=self.subject,
            text=self.text,
            posted_on=self.posted_on,
            edited_on=self.edited_on,
        )
        validator = DataValidator(data)

        return validator.normalize(strict=True)

    @property
    def edited_on(self):
        if self.showthreaded_body is not None:
            return self.showthreaded_body.edited_on

        self._cache_showthreaded_body()

        return self.showthreaded_body.edited_on

    @property
    def number(self):
        if self._number:
            number_string = self._number.pop()
            return self._post_number_normalizer.transform(number_string)

        return None

    @property
    def post_id(self):
        url_builder = self._url_builder_factory()
        post_url = url_builder.transform(self.number)
        return self._uuid_builder.transform(post_url)

    @property
    def posted_on(self):
        if self.showthreaded_subject is not None:
            return self.showthreaded_subject.posted_on

        self._cache_showthreaded_subject()

        return self.showthreaded_subject.posted_on

    @property
    def signature(self):
        if self.showthreaded_body is not None:
            return self.showthreaded_body.signature

        self._cache_showthreaded_body()

        return self.showthreaded_body.signature

    @property
    def subject(self):
        if self.showthreaded_subject is not None:
            return self.showthreaded_subject.subject

        self._cache_showthreaded_subject()

        return self.showthreaded_subject.subject

    @property
    def text(self):
        if self.showthreaded_body is not None:
            return self.showthreaded_body.text

        self._cache_showthreaded_body()

        return self.showthreaded_body.text

    def clear_cache(self):
        super().clear_cache()
        self.showthreaded_body = None
        self.showthreaded_subject = None

    def _cache_showthreaded_body(self):
        self.showthreaded_body = ShowThreadedBodyElement(self._text)

    def _cache_showthreaded_subject(self):
        self.showthreaded_subject = ShowThreadedSubjectElement(self._subject_table)

    def _url_builder_factory(self):
        return DataTransformer(UrlBuilder(BaseUrl.SHOWTHREADED, self.board))

    @staticmethod
    def _showthreaded_data_factory(post_id, subject, text, posted_on, edited_on):
        return ShowThreadedData(
            post_id=post_id,
            subject=subject,
            text=text,
            posted_on=posted_on,
            edited_on=edited_on,
        )
