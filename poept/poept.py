import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from typing import Optional
from .tools import click, enter, speech, record
import time
import logging
import json

logger = logging.getLogger(__name__)

default_bot = "Assistant"
website = "https://poe.com/"
letters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"]
email_area='input[type="email"]'
code_area="input[class*=CodeInput"
go_key='//button[text()="Go"]'
log_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'log')]"
send_key="button[class*=SendButton]"
clear_key="button[class*=ChatBreak]"
msg_element="div[class*=Message_botMessageBubble]"
stop_button_selector="button[class*=ChatStopMessageButton]"

class PoePT:
    cookies_file_path: str = os.path.expanduser("~/.cache/poept.cookies.json")

    def __init__(self, cookies: list = [], email: Optional[str] = os.environ.get("POE_EMAIL"), headless: bool = os.environ.get("POE_HEADLESS", "true") == "true"):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")   
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-logging")
        chrome_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.stat = "false"

        self.cookies = cookies
        if len(self.cookies) < 1:
            self.cookies = self.read_cookies()


        if len(self.cookies) < 1:
            if email is None:
                raise Exception("no cookies and email are set")
            else:
                self.login(email)

        self.apply_cookies()

    def read_cookies(self):

        if os.path.exists(self.cookies_file_path):
            print(f"loading cookies from {self.cookies_file_path}")
            with open(self.cookies_file_path, 'rb') as f:
                return json.load(f)

        return []

    def apply_cookies(self):
        if len(self.cookies) < 1:
            return False
        
        self.driver.get(website)
        self.driver.delete_all_cookies()
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        return True
    
    def get_message(self):
        for i in range(30):
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, "div[class*=ChatMessage_chatMessage]")
                chatMessage_element = elements[-1]

                actionBar_bar = self.driver.find_element(By.CSS_SELECTOR, "section[class*='ChatMessageActionBar_actionBar']")
                next_element = chatMessage_element.find_element(By.XPATH, "following-sibling::*[1]")              

                if next_element == actionBar_bar:
                    return chatMessage_element.find_element(By.CSS_SELECTOR, "div[class*=Markdown_markdownContainer]").text
                else:
                    logger.info("waiting for the complete response...")
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"failed to find {msg_element}: {e}")
                time.sleep(1 * i)
        else:
            raise Exception("failed to extract the response message")
    
    def clearchat(self):
        click(self.driver, By.CSS_SELECTOR, clear_key)
        print("cookies cleared")

    def login(self, email: str):
        self.driver.get(website)    
        self.driver.execute_script('window.scrollBy(0, 5);')
        
        enter(self.driver, By.CSS_SELECTOR, email_area, email)
        click(self.driver, By.XPATH, go_key)
        
        code = input("Enter code: ")
        enter(self.driver, By.CSS_SELECTOR, code_area, code)
        click(self.driver, By.XPATH, log_key)

        self.cookies = self.driver.get_cookies()
        
        with open(self.cookies_file_path, "wb") as f:
            json.dump(self.cookies, f)

    def start_dialog(self, prompt="hello", bot=default_bot):
        self.stat = "wait"
        self.driver.execute_script(f"window.location.href = '{website}{bot}/';")
        enter(self.driver, By.CSS_SELECTOR, text_area, prompt)
        click(self.driver, By.CSS_SELECTOR, send_key)
        text = self.get_message()
        self.stat = "ready"
        return text
    
    def ask(self, prompt="hello", bot=default_bot):
        if not str(self.driver.current_url).endswith("/" + bot):
            self.driver.execute_script(f"window.location.href = '{website}{bot}/';")
        
        self.stat = "wait"

        input_area_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[class*=TextArea]"))
        )
        self.driver.execute_script("arguments[0].value = arguments[1];", input_area_element, prompt)

        click(self.driver, By.CSS_SELECTOR, send_key)
        text = self.get_message()
        self.stat = "ready"
        return text
    
    def attach(self, file_path: str, bot=default_bot):
        if not str(self.driver.current_url).endswith("/" + bot):
            self.driver.execute_script(f"window.location.href = '{website}{bot}/';")
        
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[class*=ChatMessageFileInputButton]"))
        )
        
        logger.info("attached file %s", file_path)
        file_input.send_keys(file_path)
    
    def livevoice(self, timeout, fs=44100, micindex=2, file="audio.wav", chunk=1024):
        prompt = speech(record(timeout, fs, micindex, file, chunk))
        return prompt
    
    def filevoice(self, file="audio.wav"):
        prompt = speech(file)
        return prompt

    def close(self):
        self.stat = "false"
        self.driver.quit()
