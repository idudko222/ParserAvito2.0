import undetected_chromedriver as uc
import random
import requests
from config import config


class SeleniumDriver:
    def __init__(self):
        options = uc.ChromeOptions()
        options.headless = config.get("selenium.headless")
        options.add_argument(f"user-agent={config.get('selenium.user_agent')}")

        # Настройка прокси
        proxy_config = config.get("selenium.proxy")
        if proxy_config and proxy_config.get("enabled"):
            self._setup_proxy(options, proxy_config)

        self.driver = uc.Chrome(
            options=options,
            version_main=135,
            suppress_connection_errors=True,
            headless=config.get("selenium.headless")
        )
        self.driver.set_page_load_timeout(config.get("selenium.page_load_timeout"))

    def _test_proxy(self, proxy_url, test_url, timeout):
        """Проверяет работоспособность прокси"""
        try:
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            response = requests.get(
                test_url,
                proxies=proxies,
                timeout=timeout,
                verify=True
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Прокси {proxy_url} не работает: {str(e)}")
            return False

    def _setup_proxy(self, options, proxy_config):
        """Выбирает случайный рабочий прокси"""
        proxies = proxy_config.get("proxies", [])
        test_url = proxy_config.get("test_url", "https://api.ipify.org?format=json")
        timeout = proxy_config.get("timeout", 10)

        if not proxies:
            print("Список прокси не указан в конфиге")
            return

        # Перемешиваем для случайного выбора
        random.shuffle(proxies)

        for proxy in proxies:
            if self._test_proxy(proxy, test_url, timeout):
                print(f"Используется прокси: {proxy}")
                options.add_argument(f"--proxy-server={proxy}")

                # Дополнительные настройки для SOCKS
                if proxy.startswith("socks5://"):
                    options.add_argument("--proxy-type=socks5")
                break
        else:
            print("Не найдено рабочих прокси. Работа без прокси.")

        # Настройки SSL
        if proxy_config.get("ssl_verify") is False:
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--allow-running-insecure-content")

    def quit(self):
        self.driver.quit()