import os

import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

CHROMEDRIVER = os.getenv("CHROMEDRIVER")
