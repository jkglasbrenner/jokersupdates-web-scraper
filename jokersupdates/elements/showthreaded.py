from jokersupdates.locators import ShowThreaded
from jokersupdates.transformers import (
    DataTransformer,
    DateTimeNormalizer,
    StringNormalizer,
)

from .base import BaseElementListIndexElement


class SubjectElement(BaseElementListIndexElement):
    index = 0


class PostedOnElement(BaseElementListIndexElement):
    index = 1


class ShowThreadedSubjectElement(object):

    _subject = SubjectElement()
    _posted_on = PostedOnElement()
    _datetime_normalizer = DataTransformer(DateTimeNormalizer())
    _string_normalizer = DataTransformer(StringNormalizer())

    def __init__(self, element):
        self.element = element

        self._process_element()

        self.element_list = [x for x in self.element.contents if not isinstance(x, str)]

    @property
    def subject(self):
        subject_string = self._subject.get_text().strip()
        return self._string_normalizer.transform(subject_string)

    @property
    def posted_on(self):
        posted_on_string = self._posted_on.get_text().strip()
        return self._datetime_normalizer.transform(posted_on_string)

    def _process_element(self):
        for img in self.element.find_all("img"):
            img.decompose()

        for br in self.element.find_all("br"):
            br.decompose()


class ShowThreadedBodyElement(object):

    _datetime_normalizer = DataTransformer(DateTimeNormalizer())
    _string_normalizer = DataTransformer(StringNormalizer())

    def __init__(self, element):
        self._element = element
        self._signature = None
        self._edited_on = None

        self._process_element()

    @property
    def text(self):
        text_string = self._element.get_text().strip()
        return self._string_normalizer.transform(text_string)

    @property
    def edited_on(self):
        if self._edited_on:
            edited_on_string = self._edited_on.get_text().strip()
            return self._datetime_normalizer.transform(edited_on_string)

        return None

    @property
    def signature(self):
        if self._signature:
            signature_string = self._signature.get_text().strip()
            return self._string_normalizer.transform(signature_string)

        return None

    def _process_element(self):
        for script in self._element.find_all("script"):
            script.decompose()

        for br in self._element.find_all("br"):
            br.replace_with("\n")

        signature = self._element.find(**ShowThreaded.SIGNATURE)
        edited_on = self._element.find(**ShowThreaded.EDITED_ON)

        if signature:
            self._signature = signature.extract()

        if edited_on:
            self._edited_on = edited_on.extract()
