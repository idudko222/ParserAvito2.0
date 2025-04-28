import os
from typing import Dict, Any


class Config:
    """Singleton-класс для хранения всех настроек проекта."""

    _instance = None

    DEFAULT_SETTINGS = {
        # Настройки Selenium WebDriver
        "selenium": {
            "headless": False,  # Режим без графического интерфейса (True/False)
            "user_agent": "Mozilla/5.0...",  # Заголовок User-Agent для имитации браузера
            "page_load_timeout": 30,  # Макс. время загрузки страницы (сек)
            "implicit_wait": 10,  # Неявное ожидание элементов (сек)
        },

        # Настройки парсинга
        "scraping": {
            "max_retries": 3,  # Кол-во попыток перезагрузки страницы при ошибке
            "delay_between_attempts": (2, 5),  # Случайная задержка между попытками (мин, макс)
            "required_fields": [  # Обязательные поля. Если их нет, данные не сохраняются.
                "price",
                "date",
                "region",
                "geo_lat",
                "geo_lon"
            ],
        },

        # Пути к файлам
        "files": {
            "input_csv": "csv/in/properties_urls.csv",  # Файл с исходными ссылками
            "output_csv": "csv/out/results.csv",  # Файл для сохранения результатов
        },

        # Настройки эмуляции пользователя
        "emulation": {
            "scroll_delay_range": (0.5, 1.5),  # Задержка между прокрутками (сек)
            "mouse_move_delay_range": (0.2, 1.5),  # Задержка между движениями мыши (сек)
        },
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = cls.DEFAULT_SETTINGS.copy()
        return cls._instance

    def get(self, key: str, default=None) -> Any:
        """Получает значение настройки по ключу (например, 'selenium.headless')."""
        keys = key.split(".")
        value = self.settings
        for k in keys:
            value = value.get(k, {})
            if not value:
                return default
        return value or default

    def update(self, new_settings: Dict) -> None:
        """Обновляет настройки (сливает с текущими)."""
        self._merge_dicts(self.settings, new_settings)

    @staticmethod
    def _merge_dicts(original: Dict, new: Dict) -> None:
        """Рекурсивно обновляет словарь."""
        for key, value in new.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                Config._merge_dicts(original[key], value)
            else:
                original[key] = value


# Создаём глобальный экземпляр конфига
config = Config()