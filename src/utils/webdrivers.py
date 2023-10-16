from utils.logger import Logger
from typing import Union
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def initialize_chrome(headless: bool = True) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument("headless")
    driver = webdriver.Chrome(options)
    Logger.log("Initialized Chrome!")
    return driver


def initialize_firefox(headless: bool = True) -> webdriver.Firefox:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Firefox(options)
    Logger.log("Initialized Firefox!")
    return driver


class ExtendedWebDriver:
    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox]):
        self.driver = driver

    def get_page_content(self, url: str, load_selector: str) -> str:
        self.driver.get(url)
        delay = 10  # seconds
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, load_selector)))
            return self.driver.page_source
        except TimeoutException:
            Logger.error("Loading took too much time!")
        return ""
