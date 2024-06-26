from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


class HTTPGetter:
    url = 'https://istudent.urfu.ru/s/servis-informirovaniya-studenta-o-ballah-brs'

    def get_data(self, username, password):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(options=options)
        self.register(browser, username, password)
        browser.get(self.url)
        self.open_blocks(browser)
        return browser.page_source

    def register(self, browser, username, password):
        browser.get(self.url)
        WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID,
                                                            'userNameInput')))

        browser.find_element("id", "userNameInput").send_keys(username)
        browser.find_element("id", "passwordInput").send_keys(password)
        browser.find_element("id", "submitButton").click()
        WebDriverWait(browser, 3)

    @staticmethod
    def open_blocks(browser):
        WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.ID, 'disciplines')))

        subjects = browser.find_element(By.ID, 'disciplines') \
            .find_elements(By.CLASS_NAME, "rating-discipline  ")

        for subject in subjects:
            actions = ActionChains(browser)
            actions.move_to_element(subject).click().perform()
            time.sleep(0.55)
