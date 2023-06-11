import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from .tools import find, click, enter, speech, record

letters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"]


class PoePT:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-logging")
        chrome_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.stat = "false"
        self.prompt = ""
        self.response = ""
        self.config()

    def config(self, 
            website="https://poe.com/",
            email_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'email')]",
            email_area="input[class*=EmailInput]", 
            code_area="input[class*=CodeInput",
            go_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'go')]",
            log_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'log')]",
            talk_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'talk')]",
            send_key="button[class*=SendButton]",
            text_area="textarea[class*=TextArea]", 
            clear_key="button[class*=ChatBreak]",
            msg_element="ChatMessage_messageRow__7yIr2"):
        self.website = website
        self.clear_key = clear_key
        self.code_area = code_area
        self.talk_key = talk_key
        self.email_area = email_area
        self.email_key = email_key
        self.go_key = go_key
        self.log_key = log_key
        self.text_area = text_area
        self.send_key = send_key
        self.msg_element = msg_element

    def getMessage(self, chat_id):
        self.response = ""

        while True:
            try:
                msg = find(self.driver, By.XPATH, f"(//div[@class='{chat_id}'])[last()]")
                if msg.get_attribute("data-complete") == "false": break
            except:
                pass
    
        while True:
            msg = find(self.driver, By.XPATH, f"(//div[@class='{chat_id}'])[last()]")
            if msg.get_attribute("data-complete") == "true": break
            self.response = msg.text
        
        return self.response
    
    def clearcookies(self):
        os.remove("cookies.pkl")
        print("cookies cleared")
    
    def clearchat(self):
        click(self.driver, By.CSS_SELECTOR, self.clear_key)
        print("cookies cleared")

    def login(self, email):
        try:
            self.driver.get(self.website)
            self.driver.delete_all_cookies()
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()

        except (FileNotFoundError, pickle.UnpicklingError):
            self.driver.get(self.website)    
            self.driver.execute_script('window.scrollBy(0, 5);')
            
            click(self.driver, By.XPATH, self.email_key)
            enter(self.driver, By.CSS_SELECTOR, self.email_area, email)
            click(self.driver, By.XPATH, self.go_key)
            
            code = input("Enter code: ")
            enter(self.driver, By.CSS_SELECTOR, self.code_area, code)
            click(self.driver, By.XPATH, self.log_key)

            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def ask(self, bot="sage", prompt="hello"):
        self.stat = "wait"
        self.prompt = prompt
        
        self.driver.execute_script(f"window.location.href = '{self.website}{bot}/';")
        
        click(self.driver, By.CSS_SELECTOR, self.talk_key)
        enter(self.driver, By.CSS_SELECTOR, self.text_area, prompt)
        click(self.driver, By.CSS_SELECTOR, self.send_key)

        text = self.getMessage(self.msg_element)
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
