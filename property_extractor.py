import requests
from bs4 import BeautifulSoup
from locator import LocatorAvito as loc
from datetime import datetime, timedelta

class PropertyExtractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html,'html.parser')

    def get_price(self):
        try:
            price_element = self.soup.select_one(loc.PRICE[1])
            if price_element:
                price_text = price_element.text.strip().replace("\xa0", "").replace("₽", "")

            return price_text

        except AttributeError as e:
            print(f'Цена не найдена: {e}')

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



