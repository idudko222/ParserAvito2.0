import random
import time
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import MaxRetryError, NewConnectionError
from config import config


class LinkProcessor:
    def __init__(self, driver, user_emulation, data_parser, csv_manager):
        self.driver = driver
        self.user_emulation = user_emulation
        self.data_parser = data_parser
        self.csv_manager = csv_manager
        self.max_retries = config.get("scraping.max_retries")

    def process_link(self, link):
        """Обрабатывает одну ссылку: загружает страницу, эмулирует поведение пользователя, парсит и сохраняет данные."""
        for attempt in range(self.max_retries):
            try:
                print(f'Обработка ссылки (попытка {attempt + 1}/{self.max_retries}): {link}')

                # Загрузка страницы
                self.driver.get(link)

                # Эмуляция поведения пользователя
                self.user_emulation.random_delay()
                self.user_emulation.emulate_reading()
                self.user_emulation.emulate_mouse_movement()

                # Получение и обработка HTML
                html = self.driver.page_source
                if not html:
                    print(f"Пустой HTML для ссылки: {link}")
                    continue

                # Парсинг данных
                parsed_data = self.data_parser.parse_listing_data(html, link)
                if not parsed_data:
                    print(f"Не удалось распарсить данные для ссылки: {link}")
                    continue

                # Сохранение данных
                self.csv_manager.save_row(parsed_data)
                return True

            except (WebDriverException, MaxRetryError, NewConnectionError) as e:
                print(f"Ошибка при обработке ссылки {link}: {str(e)}")
                if attempt == self.max_retries - 1:
                    return False

                # Случайная задержка перед повторной попыткой
                delay = random.uniform(2, 5)
                print(f"Повторная попытка через {delay:.1f} сек...")
                time.sleep(delay)

        return False