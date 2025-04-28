import undetected_chromedriver as uc
import time


class SeleniumDriver:
    def __init__(self, headless=False):
        options = uc.ChromeOptions()
        options.headless = headless
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = uc.Chrome(options=options)

    # def get_html(self, url):
    #     self.driver.get(url)
    #     time.sleep(5)
    #     return self.driver.page_source


    def quit(self):
        self.driver.quit()
