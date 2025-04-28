from selenium_driver import SeleniumDriver
from csv_manager import CSVManager
from emulation import UserEmulator
from link_processor import LinkProcessor
from parser import DataParser


def main():
    selenium_driver = SeleniumDriver()
    driver = selenium_driver.driver # Инициализируем драйвера
    try:
        csv_manager = CSVManager(out_file='csv/out/test.csv', in_file='csv/in/properties_urls.csv') # Считываем ссылки
        user_emulator = UserEmulator(driver) # Эмуляция действий человека
        data_parser = DataParser()  # Парсер данных

        link_processor = LinkProcessor(driver, user_emulator, data_parser, csv_manager, 3)

        links = csv_manager.read_links()
        for link in links:
            link_processor.process_link(driver, link)



    finally:
        driver.quit()


if __name__ == '__main__':
    while True:
        main()
