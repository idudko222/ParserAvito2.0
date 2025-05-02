from property_extractor import PropertyExtractor
from selenium_driver import SeleniumDriver
from csv_manager import CSVManager
from emulation import UserEmulator
from link_processor import LinkProcessor
from parser import DataParser
from config import config
import pandas as pd
import time  # Добавляем для замера времени

# URL поиска по квартирам
BASE_URL = "https://www.avito.ru/all/kvartiry/prodam"


def parse_properties():
    selenium_driver = SeleniumDriver()
    driver = selenium_driver.driver  # Инициализируем драйвера
    try:
        start_time = time.time()  # Замер времени старта

        input_file = config.get("files.input_csv")
        output_file = config.get("files.output_csv")
        csv_manager = CSVManager(input_file, output_file)  # Считываем ссылки
        user_emulator = UserEmulator(driver)  # Эмуляция действий человека
        data_parser = DataParser()  # Парсер данных

        link_processor = LinkProcessor(driver, user_emulator, data_parser, csv_manager)

        links = csv_manager.read_links()
        total_links = len(links)

        if not links:
            print("Нет ссылок для обработки. Завершаем работу.")
            return

        for i, link in enumerate(links, 1):
            print(f"\nОбработка {i}/{total_links}: {link}")
            link_processor.process_link(link)

        # Когда все ссылки обработаны — выводим время
        end_time = time.time()
        execution_time = end_time - start_time
        hours = int(execution_time / 3600)
        minutes = int((execution_time - hours * 3600) / 60)
        print(f"\nВсе ссылки обработаны. Время выполнения: {hours} часов, {minutes} минут.")

    finally:
        driver.quit()


def parse_links():
    url = BASE_URL
    selenium_driver = SeleniumDriver()
    driver = selenium_driver.driver  # Инициализируем драйвера
    number_of_links = 2000
    counter = int(number_of_links / 50)  # Количество ссылок, которое необходимо собрать

    try:
        start_time = time.time()  # Замер времени старта

        file = config.get("files.input_csv")  # Файл, в который будут сохранятся ссылки
        csv_manager = CSVManager(file, None)
        user_emulator = UserEmulator(driver)  # Эмуляция действий человека
        data_parser = DataParser()
        link_processor = LinkProcessor(driver, user_emulator, data_parser, csv_manager)

        while url and counter > 0:
            link_processor.process_new_links(url)
            counter -= 1
            url = PropertyExtractor.get_next_page_url(driver)

        # Когда все ссылки обработаны — выводим время
        end_time = time.time()
        execution_time = end_time - start_time
        hours = int(execution_time / 3600)
        minutes = int((execution_time - hours * 3600) / 60)
        print(f"\nВсе ссылки обработаны. Время выполнения: {hours} часов, {minutes} минут.")

    finally:
        driver.quit()  # Закрываем браузер


if __name__ == '__main__':
    parse_links()
