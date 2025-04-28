import random, time
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import MaxRetryError, NewConnectionError


class LinkProcessor:
    def __init__(self, driver, user_emulation, data_parser, csv_manager, max_retries=3):
        self.driver = driver
        self.user_emulation = user_emulation
        self.data_parser = data_parser
        self.csv_manager = csv_manager
        self.max_retries = max_retries

    def process_link(self, driver, link):
        for attempt in range(self.max_retries):
            try:
                print(f'Попытка {attempt + 1}/{self.max_retries}: {link}')

                self.driver.get(link)
                self.user_emulation.random_delay(2,5)
                self.user_emulation.emulate_reading()
                self.user_emulation.emulate_mouse_movement()

                html = self.driver.page_source

                if html:
                    parsed_data = self.data_parser.parse_listing_data(driver, html)
                    if parsed_data:
                        self.csv_manager.save_row(parsed_data)
                        return True

            except (WebDriverException, MaxRetryError, NewConnectionError) as e:
                print(f"Ошибка: {e}")
                if attempt == self.max_retries - 1:
                    return False
                time.sleep(random.uniform(2, 5))  # Пауза перед повторной попыткой

        return False


