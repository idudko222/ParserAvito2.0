import undetected_chromedriver as uc
import time
from config import config


class SeleniumDriver:
    def __init__(self, headless=False):
        options = uc.ChromeOptions()
        options.headless = config.get("selenium.headless")
        options.add_argument(f"user-agent={config.get('selenium.user_agent')}")
        self.driver = uc.Chrome(options=options, version_main=135)
        self.driver.set_page_load_timeout(config.get("selenium.page_load_timeout"))

    def quit(self):
        self.driver.quit()
