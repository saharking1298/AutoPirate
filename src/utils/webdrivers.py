from utils.logger import Logger
from typing import Union
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from enum import Enum


class Browser(Enum):
    CHROME = "chrome",
    FIREFOX = "firefox"


def initialize_browser(browser: Browser, headless: bool = True):
    if browser == Browser.CHROME:
        return ChromeDriver(headless)
    else:
        return FirefoxDriver(headless)


def _get_page_content(driver: Union[webdriver.Chrome, webdriver.Firefox], url: str, load_selector: str) -> str:
    driver.get(url)
    delay = 10  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, load_selector)))
        return driver.page_source
    except TimeoutException:
        raise TimeoutException("Page timed out. Check your internet connection.")


class ChromeDriver(webdriver.Chrome):
    def __init__(self, headless: bool = True):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if headless:
            options.add_argument("headless")
        super().__init__(options)
        Logger.log("Initialized Chrome!")

    def get_page_content(self, url: str, load_selector: str) -> str:
        return _get_page_content(self, url, load_selector)


class FirefoxDriver(webdriver.Firefox):
    def __init__(self, headless: bool = True):
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        super().__init__(options)
        Logger.log("Initialized Firefox!")

    def get_page_content(self, url: str, load_selector: str) -> str:
        return _get_page_content(self, url, load_selector)