import logging
import undetected_chromedriver as uc
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

import re
import subprocess
import requests


class FlyGPTClient(object):
    def __init__(self, url='http://127.0.0.1:8000/flggpt/generate'):
        self.url = url

    def generate(self, prompt_text, retries=5):
        params = {
            'prompt_text': prompt_text,
            'retries': retries
        }
        headers = {
            'accept': 'application/json'
        }
        with requests.get(self.url, params=params, headers=headers, stream=True) as response:
            for chunk in response.iter_content(2**32):
                yield chunk.decode('utf-8')

class FlyGPTServer:

    def get_chrome_version(self):
        result = subprocess.run([self.browser_executable_path, '--version'], capture_output=True, text=True)
        version_parser = re.compile(r'\d+\.\d+\.\d+\.\d+')
        return version_parser.findall(result.stdout)[0]

    def __init__(self,
        driver_version=None,
        browser_executable_path='/opt/google/chrome/google-chrome',
        user_data_dir="~/.config/google-chrome/flygpt",
        wait_user_confirm=False,
        proxy_server=None,
    ):
        # Install driver is no exists
        self.browser_executable_path = browser_executable_path
        driver_version = driver_version if driver_version else self.get_chrome_version()
        self.driver_executable_path = ChromeDriverManager(driver_version=driver_version).install()

        # Initial chrome driver
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        options.add_argument(f"--user-data-dir={user_data_dir}")
        if proxy_server:
            options.add_argument(f'--proxy-server={ proxy_server }')

        self.driver = uc.Chrome(
            driver_executable_path=self.driver_executable_path,
            browser_executable_path=self.browser_executable_path,
            use_subprocess=True,
            options=options,
        )
        self.driver.implicitly_wait(10)
        self.driver.get('https://chat.openai.com/')

        if wait_user_confirm:
            input('Press any key to continue ...')
        print('wait_user_confirm:', wait_user_confirm)

        prompt_input = self.driver.find_element(By.CLASS_NAME, 'm-0.w-full.resize-none')

        self.elements = []

    def send_recv(self, prompt_text):
        self.elements = self.driver.find_elements(By.CLASS_NAME, 'markdown')
        prompt_input = self.driver.find_element(By.CLASS_NAME, 'm-0.w-full.resize-none')
        self.driver.execute_script("arguments[0].value = arguments[1]", prompt_input, prompt_text)
        sleep(1)
        prompt_input.send_keys(Keys.ENTER)
        prompt_input.send_keys(Keys.ENTER)

        count = 0
        while True:
            # If generating, then break
            if self.generating():
                break
            # Or generating is begin too fast
            sleep(interval)
            count += 1
            if count > 30:
                break

        self.last_text = ""
        while True:
            sleep(interval)
            elements = self.driver.find_elements(By.CLASS_NAME, 'markdown')
            if len(self.elements) == len(elements):
                continue
            if elements:
                # text = elements[-1].text
                text = elements[-1].get_attribute('innerHTML')
                if self.last_text == text:
                    if not self.generating():
                        yield f'\n{text}'
                        break
                else:
                    yield '.'
                    self.last_text = text

    def clear_session(self):
        while True:
            conversations = self.driver.find_elements(
                By.CSS_SELECTOR, 'div.relative.grow.whitespace-nowrap'
            )
            if not conversations:
                break

            conversations[0].click()
            sleep(3)

            # Click session[0] more button
            more_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                'button.items-center.text-token-text-primary[aria-haspopup="menu"]'
            )
            more_buttons[0].click()
            sleep(3)

            # Click delete menu
            delete_menu = self.driver.find_element(
                By.CSS_SELECTOR, 'div[role="menuitem"].text-red-500')
            delete_menu.click()
            sleep(3)

            # Confirm
            confirm_button = self.driver.find_element(
                By.CSS_SELECTOR, 'button.relative.btn-danger')
            confirm_button.click()
            sleep(3)

    def generating(self):
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, ".text-gray-400.flex.self-end.items-center.justify-center")

        if not elements:
            return False

        return len(elements[-1].children()) != 4

