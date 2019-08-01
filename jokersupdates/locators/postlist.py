import re

from selenium.webdriver.common.by import By

POST_ROWS = {"name": "tr", "id": re.compile(r"postrow\d+")}
REPLY_INDENT = {"name": "img", "alt": "x"}
NEXT_BUTTON = (
    By.XPATH,
    "//tr/td/font[contains(@class, 'onbody')]/a//*[text()[contains(., 'Next')]]",
)
PREVIOUS_BUTTON = (
    By.XPATH,
    "//tr/td/font[contains(@class, 'onbody')]/a//*[text()[contains(., 'Previous')]]",
)
QS_BOARD = "Board"
