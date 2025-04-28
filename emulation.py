import random
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from config import config


class UserEmulator:
    def __init__(self, driver):
        self.driver = driver

    def emulate_reading(self):
        """Эмулирует прокрутку страницы с настройками из config.py"""
        scroll_cfg = config.get("emulation.scroll")
        pause_time = random.uniform(*scroll_cfg["pause_time_range"])
        scroll_count = random.randint(*scroll_cfg["count_range"])

        for _ in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)

        if random.random() < scroll_cfg["scroll_back_chance"]:
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_cfg['scroll_back_pixels']});")
            time.sleep(scroll_cfg["scroll_back_delay"])

    def emulate_mouse_movement(self):
        """Эмулирует движение мыши с настройками из config.py"""
        mouse_cfg = config.get("emulation.mouse")
        actions = ActionChains(self.driver)
        body = self.driver.find_element(By.TAG_NAME, 'body')

        for _ in range(random.randint(*mouse_cfg["move_count_range"])):
            x_offset = random.uniform(*mouse_cfg["offset_range"])
            y_offset = random.uniform(*mouse_cfg["offset_range"])

            actions.move_to_element_with_offset(body, x_offset, y_offset)
            actions.pause(random.uniform(*mouse_cfg["pause_time_range"]))
            actions.perform()

            if random.random() < mouse_cfg["click_chance"]:
                actions.click()
                actions.pause(random.uniform(*mouse_cfg["click_delay_range"]))
                actions.perform()

    def random_delay(self):
        """Случайная задержка на основе настроек"""
        delay_cfg = config.get("emulation.delay")
        time.sleep(random.uniform(delay_cfg["min"], delay_cfg["max"]))