from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from property_extractor import PropertyExtractor


class DataParser:

    def get_html(self, driver, link):
        """Загружает HTML страницы и ждёт появления ключевых элементов."""
        try:
            driver.get(link)
            WebDriverWait(driver, 5).until(
                lambda x: x.find_element(By.XPATH, "//h1 | //div[@data-marker='item-view/item']")
            )
            return driver.page_source
        except Exception as e:
            print(f"Ошибка загрузки страницы {link}: {e}")
            return None

    def parse_listing_data(self, html, link):
        """Парсит данные из HTML, полученного от LinkProcessor."""
        try:
            if not html:
                return None

            extractor = PropertyExtractor(html)
            extra_info = extractor.get_extra_info() or {}
            coordinates = extractor.get_coordinates() or {}

            data = {
                "price": extractor.get_price(),
                "date": extractor.get_date(),
                "geo_lat": coordinates.get("lat"),
                "geo_lon": coordinates.get("lon"),
                "region": extractor.get_region(),
                "building_type": extra_info.get("building_type"),
                "level": extra_info.get("level"),
                "levels": extra_info.get("levels"),
                "rooms": extra_info.get("rooms"),
                "area": extra_info.get("area"),
                "kitchen_area": extra_info.get("kitchen_area"),
                "object_type": extractor.get_object_type(),
            }

            # Проверка обязательных полей
            required_fields = ["price", "date", "region", "geo_lat", "geo_lon"]
            if any(data.get(field) in (None, "") for field in required_fields):
                print(f"Пропуск записи: не хватает данных для {link}")
                return None
            if data:
                print("Успешно обработана")
            return data

        except Exception as e:
            print(f"Ошибка парсинга {link}: {str(e)}")
            return None
