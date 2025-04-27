import requests
from bs4 import BeautifulSoup
from locator import LocatorAvito as loc
from datetime import datetime, timedelta

class PropertyExtractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html,'html.parser')

    def get_price(self, html):
        soup = BeautifulSoup(html, "html.parser")
        price = 0

        try:
            price_element = soup.select_one(loc.PRICE[1])
            if price_element:
                price_text = price_element.text.strip()
                price_text = price_text.replace("\xa0", "").replace("₽", "")
                price = price_text

            return price

        except AttributeError as e:
            print(f'Цена не найдена {html}: {e}')



