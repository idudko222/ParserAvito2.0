from selenium_driver import SeleniumDriver
from csv_manager import CSVManager
from emulation import UserEmulator
from link_processor import LinkProcessor
from parser import DataParser
from config import config


def main():
    selenium_driver = SeleniumDriver()
    driver = selenium_driver.driver # Инициализируем драйвера
    try:
        input_file = config.get("files.input_csv")
        output_file = config.get("files.output_csv")
        csv_manager = CSVManager(input_file, output_file) # Считываем ссылки
        user_emulator = UserEmulator(driver) # Эмуляция действий человека
        data_parser = DataParser()  # Парсер данных

        link_processor = LinkProcessor(driver, user_emulator, data_parser, csv_manager)

        links = csv_manager.read_links()
        total_links = len(links)

        for i, link in enumerate(links, 1):
            print(f"\nОбработка {i}/{total_links}: {link}")
            link_processor.process_link(link)



    finally:
        driver.quit()


if __name__ == '__main__':
    while True:
        main()
