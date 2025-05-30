from bs4 import BeautifulSoup
from const.locator import LocatorAvito as loc
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium_driver import SeleniumDriver
from selenium.webdriver.support import expected_conditions as EC


class PropertyExtractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_price(self):
        try:
            price_element = self.soup.select_one(loc.PRICE[1])
            if price_element:
                return price_element.text.strip().replace("\xa0", "").replace("₽", "")

        except AttributeError as e:
            print(f'Цена не найдена: {e}')
            return None

    def get_date(self):
        try:
            date_element = self.soup.select_one(loc.DATE_PUBLIC[1])
            if date_element:
                date_text = date_element.text.strip()
                if 'вчера' in date_text:
                    return (datetime.today().date() - timedelta(days=1)).strftime("%Y-%m-%d")
                elif 'сегодня' in date_text:
                    return datetime.today().date()
                else:
                    month_replace = {
                        "января": "01", "февраля": "02", "марта": "03", "апреля": "04",
                        "мая": "05", "июня": "06", "июля": "07", "августа": "08",
                        "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"
                    }
                    date_text = date_text.replace("·", "").strip()
                    date_text = date_text.split(" в ")[0].strip()
                    parts = date_text.split()
                    if len(parts) == 2:
                        day, month = parts
                        month = month_replace.get(month.lower())
                        if month:
                            return f"{datetime.today().year}-{month}-{day}"
        except Exception as e:
            print(f"Ошибка при парсинге даты: {e}")
        return None

    def get_coordinates(self):
        """Извлекает координаты (широту и долготу) из блока с картой."""
        coordinates = {"lat": None, "lon": None}
        try:
            # Ищем блок с картой
            map_block = self.soup.find("div", {"class": "style-item-map-wrapper-ElFsX"})
            if map_block:
                # Извлекаем широту и долготу из атрибутов
                lat = map_block.get("data-map-lat")
                lon = map_block.get("data-map-lon")

                # Проверяем, что координаты не None
                if lat and lon:
                    coordinates["lat"] = float(lat)  # Преобразуем в float
                    coordinates["lon"] = float(lon)  # Преобразуем в float
        except Exception as e:
            print(f"Ошибка парсинга координат: {e}")

        return coordinates

    def get_region(self):
        try:
            region_element = self.soup.select_one(loc.GEO[1])
            if region_element:
                region_text = region_element.text.strip().split(",")[0].strip()

                replacements = {
                    "обл.": "область",
                    "Обл.": "область",
                    "АО": "автономный округ",
                    "Республика Северная Осетия — Владикавказ": "Республика Северная Осетия — Алания",
                    "Севастополь": "Республика Крым",
                    "Республика Татарстан (Татарстан)": "Республика Татарстан",
                }

                for old, new in replacements.items():
                    if old in region_text:
                        region_text = region_text.replace(old, new)

                return region_text

            else:
                print("Элемент с регионом не найден.")

        except Exception as e:
            print(f"Ошибка парсинга региона: {e}")

        return None

    def get_extra_info(self):
        try:
            params_blocks = self.soup.find_all("div", {"data-marker": "item-view/item-params"})

            extracted_data = {
                "level": None,  # Этаж (например, "2")
                "levels": None,  # Всего этажей в доме (например, "5")
                "rooms": None,  # Количество комнат (например, "1")
                "area": None,  # Общая площадь (например, "30.5")
                "kitchen_area": None,  # Площадь кухни (например, "5.5")
                "building_type": None,  # Тип дома
            }

            for block in params_blocks:
                for item in block.find_all("li"):
                    key_tag = item.find("span", class_="styles-module-noAccent-l9CMS")
                    if key_tag:
                        key = key_tag.text.replace(":", "").strip()
                        value = (key_tag.next_sibling.strip().replace("\xa0м²", "")
                                 .replace("\xa0эт.", ""))

                        # Сопоставляем ключи с нужными параметрами
                        if key == "Количество комнат":
                            extracted_data["rooms"] = -1 if value.lower() == "студия" else value
                        elif key == "Общая площадь":
                            extracted_data["area"] = value
                        elif key == "Площадь кухни":
                            extracted_data["kitchen_area"] = value
                        elif key == "Этаж":
                            # Парсим "2 из 5" → level=2, levels=5
                            parts = value.split(" из ")
                            if len(parts) == 2:
                                extracted_data["level"] = parts[0]
                                extracted_data["levels"] = parts[1]
                            else:
                                extracted_data["level"] = value  # На случай, если формат другой
                        elif key == "Тип дома":
                            type_replace = {
                                'другой': '0',
                                'панельный': '1',
                                'монолитный': '2',
                                'кирпичный': '3',
                                'блочный': '4',
                                'деревянный': '5',
                            }

                            extracted_data["building_type"] = type_replace.get(value)

            return extracted_data  # Возвращаем итоговый словарь

        except AttributeError as e:
            print(f"Ошибка парсинга доп данных: {e}")
            return None

    def get_object_type(self):
        """Извлекает тип объекта (Новостройки/Вторичка) из блока навигации."""
        try:
            # Ищем блок навигации
            nav_block = self.soup.find("div", {"data-marker": "item-navigation"})
            if nav_block:
                # Ищем все ссылки внутри блока
                links = nav_block.find_all("a", class_="breadcrumbs-link-Vr4Nc")

                # Проверяем, что есть хотя бы 5 элементов
                if len(links) >= 5:
                    # Пятый элемент — это тип объекта (Новостройки/Вторичка)
                    object_type = links[4].text.strip()
                    if object_type == 'Вторичка':
                        return 1
                    else:
                        return 2
        except Exception as e:
            print(f"Ошибка парсинга типа объекта: {e}")
        return None

    def get_new_link_data(self):
        ads = self.soup.select(loc.TITLES[1])
        data_list = []
        for ad in ads:
            try:
                title = ad.select_one(loc.NAME[1]).text.strip().replace("\xa0м²", "").replace("\xa0эт.", "")
                price = ad.select_one(loc.PRICE[1]).get("content", "0")
                link = "https://www.avito.ru" + ad.select_one(loc.URL[1]).get("href", "")

                data_list.append({"title": title, "price": price, "link": link})
            except Exception as e:
                print(f"Ошибка парсинга: {e}")

        return data_list

    @staticmethod
    def get_next_page_url(driver):
        """Находит URL следующей страницы"""
        try:
            # Ждем, пока кнопка "Следующая страница" станет кликабельной
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(loc.NEXT_BUTTON)
            )

            # Проверяем, не заблокирована ли кнопка
            if "disabled" in next_button.get_attribute("class"):
                return None  # Если кнопка неактивна, значит, это последняя страница

            # Запоминаем текущий URL
            current_url = driver.current_url

            # Кликаем на кнопку
            next_button.click()

            # Ждем, пока URL изменится (новая страница загрузится)
            WebDriverWait(driver, 10).until(
                EC.url_changes(current_url)
            )

            # Возвращаем новый URL
            return driver.current_url
        except Exception as e:
            print(f"Не удалось найти кнопку перехода на следующую страницу: {e}")
            return None
