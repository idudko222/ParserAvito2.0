from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from property_extractor import PropertyExtractor


class DataParser:

    def get_html(self, driver, link):
        try:
            driver.get(link)
            WebDriverWait(driver, 5).until(
                lambda x: x.find_element(By.XPATH, "//h1 | //div[@data-marker='item-view/item']")
            )
            return driver.page_source
        except Exception as e:
            print(f'Вышло время загрузки страницы {link}: {e}')
            return None


    def parse_listing_data(self, driver, link):
        try:
            html = self.get_html(driver, link)

            if not html:
                return None

            extractor = PropertyExtractor(html)

            data = {
                "price": extractor.get_price(),
                "date": extractor.get_date(),
                "geo_lat": extractor.get_coordinates().get("lat", ""),
                "geo_lon": extractor.get_coordinates().get("lon", ""),
                "region": extractor.get_region(),
                "building_type": extractor.get_extra_info().get("building_type", ""),
                "level": extractor.get_extra_info().get("level", ""),
                "levels": extractor.get_extra_info().get("levels", ""),
                "rooms": extractor.get_extra_info().get("rooms", ""),
                "area": extractor.get_extra_info().get("area", ""),
                "kitchen_area": extractor.get_extra_info().get("kitchen_area", ""),
                "object_type": extractor.get_object_type()
            }

            important_fields = ['price', 'date', 'region', 'geo_lat', 'geo_lon']
            if any(data[field] in [None, ''] for field in important_fields):
                print(f"Пропуск записи: важные данные не найдены для ссылки {link}")
                return None

            return data

        except Exception as e:
            print(f"Ошибка при парсинге данных для ссылки {link}: {e}")
            return None




