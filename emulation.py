import random
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class UserEmulator:
    def __init__(self, driver):
        self.driver = driver

    def emulate_reading(self):
        """Эмулирует прокрутку страницы"""
        scroll_pause_time = random.uniform(0.5, 1.5)
        scroll_count = random.randint(2, 5)

        for _ in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

        # Иногда возвращаемся немного назад (30% случаев)
        if random.random() < 0.3:
            self.driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(0.5)

    def emulate_mouse_movement(self):
        """Эмулирует случайное передвижение мыши"""
        actions = ActionChains(self.driver)
        body = self.driver.find_element(By.TAG_NAME, 'body')

        for _ in range(random.randint(1, 3)):
            x_offset = random.random(50, 300)
            y_offset = random.random(50, 300)

            actions.move_to_element_with_offset(body, x_offset, y_offset)
            actions.pause(random.uniform(0.2, 1.5))
            actions.perform()

            if random.random() < 0.3:
                actions.click()
                actions.pause(random.uniform(0.2, 1.5))
                actions.perform()

        def random_delay(self, min_delay, max_delay):
            """Случайная задержка"""
            time.sleep(random.uniform(min_delay, max_delay))