import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from .tools import click, enter, speech, record
import time
import logging

logger = logging.getLogger(__name__)

default_bot = "Assistant"
website = "https://poe.com/"
letters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"]
email_area='input[type="email"]'
code_area="input[class*=CodeInput"
go_key='//button[text()="Go"]'
log_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'log')]"
send_key="button[class*=SendButton]"
text_area="textarea[class*=TextArea]" 
clear_key="button[class*=ChatBreak]"
msg_element="div[class*=Message_botMessageBubble]"
stop_button_selector="button[class*=ChatStopMessageButton]"

class PoePT:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-logging")
        chrome_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.stat = "false"

    def get_message(self):
        for i in range(10):
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, "div[class*=ChatMessage_chatMessage]")
                element = elements[-1]
                next_element = element.find_element(By.XPATH, "following-sibling::*[1]")
                chat_message_action_bar = self.driver.find_element(By.CSS_SELECTOR, "section[class*='ChatMessageActionBar_actionBar']")
                if next_element == chat_message_action_bar:
                    return elements[-1].text
                else:
                    logger.info("waiting for the complete response...")
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"failed to find {msg_element}: {e}")
                time.sleep(1 * i)
        else:
            raise Exception("failed to extract the response message")
    
    def clearcookies(self):
        os.remove("cookies.pkl")
        print("cookies cleared")
    
    def clearchat(self):
        click(self.driver, By.CSS_SELECTOR, clear_key)
        print("cookies cleared")

    def login(self, email):
        try:
            self.driver.get(website)
            self.driver.delete_all_cookies()
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()

        except (FileNotFoundError, pickle.UnpicklingError):
            self.driver.get(website)    
            self.driver.execute_script('window.scrollBy(0, 5);')
            
            enter(self.driver, By.CSS_SELECTOR, email_area, email)
            click(self.driver, By.XPATH, go_key)
            
            code = input("Enter code: ")
            enter(self.driver, By.CSS_SELECTOR, code_area, code)
            click(self.driver, By.XPATH, log_key)

            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

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
        enter(self.driver, By.CSS_SELECTOR, text_area, prompt)
        click(self.driver, By.CSS_SELECTOR, send_key)
        text = self.get_message()
        self.stat = "ready"
        return text
    
    def livevoice(self, timeout, fs=44100, micindex=2, file="audio.wav", chunk=1024):
        prompt = speech(record(timeout, fs, micindex, file, chunk))
        return prompt
    
    def filevoice(self, file="audio.wav"):
        prompt = speech(file)
        return prompt

    def close(self):
        self.stat = "false"
        self.driver.quit()
