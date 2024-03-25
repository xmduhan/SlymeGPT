import logging
import undetected_chromedriver as uc
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager
driver_executable_path = ChromeDriverManager().install()
browser_executable_path = '/opt/google/chrome/google-chrome'
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir=~/.config/google-chrome/Default")

class FlyGPT:
    
    def __init__(self):
        self.driver = uc.Chrome(
            driver_executable_path=driver_executable_path,
            browser_executable_path=browser_executable_path,
            use_subprocess=True,
            options=options,
        )
        self.driver.get('https://chat.openai.com/')
        self.last_text = ""

    def send(self, prompt_text):    
        prompt_input = driver.find_element(By.CLASS_NAME, 'm-0.w-full.resize-none')
        self.driver.execute_script("arguments[0].value = arguments[1]", prompt_input, prompt_text)
        prompt_input.send_keys(Keys.ENTER)
        prompt_input.send_keys(Keys.ENTER)

    def recv(self):        
        while True:
            sleep(3)
            elements = self.driver.find_elements(By.CLASS_NAME, 'markdown')
            text = elements[-1].text
            if self.last_text == text:
                break
            else:
                yield text[len(self.last_text):]:
