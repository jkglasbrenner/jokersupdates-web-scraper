from urllib.parse import parse_qs


class BaseElementListIndexElement(object):
    def __get__(self, obj, owner):
        element_list = obj.element_list
        index = self.index
        element = element_list[index]

        return element


class BaseElementListFindElement(object):
    def __get__(self, obj, owner):
        element_list = obj.element_list
        index = self.index
        element = element_list[index]

        return element.find(**self.locator)


class BaseElementListSelectElement(object):
    def __get__(self, obj, owner):
        element_list = obj.element_list
        index = self.index
        element = element_list[index]

        return element.select_one(**self.locator)


class BasePageFindElement(object):
    def __get__(self, obj, owner):
        driver = obj.driver
        return driver.find_element(*self.locator)


class BasePageFindElements(object):
    def __get__(self, obj, owner):
        driver = obj.driver
        return driver.find_elements(*self.locator)


class BaseSoupFindElement(object):
    def __get__(self, obj, owner):
        soup = obj.soup
        return soup.find(**self.locator)


class BaseSoupFindElements(object):
    def __get__(self, obj, owner):
        soup = obj.soup
        return soup.find_all(**self.locator)


class BaseSoupSelectElement(object):
    def __get__(self, obj, owner):
        soup = obj.soup
        return soup.select_one(**self.locator)


class BaseSoupSelectElements(object):
    def __get__(self, obj, owner):
        soup = obj.soup
        return soup.select(**self.locator)


class BasePageGetQueryParameter(object):
    def __get__(self, obj, owner):
        parsed_query_string = parse_qs(obj.url_query_string)
        return parsed_query_string.get(self.qs_parameter)
