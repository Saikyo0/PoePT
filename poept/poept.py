import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import speech_recognition as sr

class PoePT:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-logging")
        chrome_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.stat = "false"
        self.email = ""
        self.prompt = ""
        self.response = ""
        self.config()

    def config(self, 
            website="https://poe.com/",
            clear_key="ChatMessageInputFooter_chatBreakButton__hqJ3v", 
            code_area="input.VerificationCodeInput_verificationCodeInput__YD3KV", 
            talk_key="//button[contains(., 'Talk')]", 
            email_area="input[type='email']", 
            email_key="//button[contains(., 'Email')]", 
            go_key="//button[contains(., 'Go')]", 
            log_key="//button[contains(., 'Log')]", 
            text_area="GrowingTextArea_textArea__eadlu", 
            send_key="button.ChatMessageSendButton_sendButton__OMyK1", 
            chat_element="ChatMessagesView_infiniteScroll__K_SeP", 
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
        self.chat_element = chat_element
        self.msg_element = msg_element

    def click(self, by, id):
        count = 0
        while True:
            count+=1
            if (count>5): return False
            try:
                button = self.driver.find_element(by, id)
                button.click()
                return button
            except:
                pass

    def input(self, by, id, data):
        count = 0
        while True:
            count+=1
            if (count>5): return False
            try:
                area = self.driver.find_element(by, id)
                area.send_keys(data)
                break
            except:
                pass

    def find(self, by, id):
        count = 0
        while True:
            count+=1
            try:
                element = self.driver.find_element(by, id)
                return element
            except:
                pass
            if (count>5): return False

    def getMessage(self, chat_id):
        self.response = ""
        while True:
            try:
                time.sleep(0.1)
                chat = self.find(By.XPATH, f"(//div[@class='{chat_id}'])[last()]")
                if not chat: continue
                if self.prompt in chat.text: continue
                self.response = chat.text
                if chat.get_attribute("data-complete") == "true": break
            except:
                continue
        text = self.response
        return text
    
    def clearcookies(self):
        os.remove("cookies.pkl")
        print("cookies cleared")
    
    def clearchat(self):
        self.click(By.CLASS_NAME, self.clear_key)
        print("cookies cleared")

    def login(self, email):
        self.email = email
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
            time.sleep(0.1)

            while True:
                if (self.input(By.CSS_SELECTOR, self.email_area ,email)!=False): 
                    break
                self.click(By.XPATH, self.email_key)

            self.click(By.XPATH, self.go_key)
            code = input("Enter code: ")
            self.input(By.CSS_SELECTOR, self.code_area, code)
            self.click(By.XPATH, self.log_key)
            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def ask(self, bot="sage", prompt="hello"):
        self.stat = "wait"
        self.prompt = prompt
        self.driver.get(self.website + bot)
        self.click(By.XPATH, self.talk_key)
        self.input(By.CLASS_NAME, self.text_area, prompt)
        self.click(By.CSS_SELECTOR, self.send_key)
        self.find(By.CLASS_NAME, self.chat_element)
        text = self.getMessage(self.msg_element)
        self.stat = "ready"
        return text

    def livevoice(self, timeout, fs=44100, micindex=2, file="audio.wav", chunk=1024):
        r = sr.Recognizer()
        mic = sr.Microphone(
            device_index=micindex, 
            sample_rate=fs, 
            chunk_size=chunk
        )
        with mic as source:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=timeout)
        with open(file, "wb") as f:
            f.write(audio.get_wav_data())
        prompt = self.filevoice(file)
        return prompt

    def filevoice(self, file="audio.wav"):
        recognizer = sr.Recognizer()
        with sr.AudioFile(file) as source:
            audio = recognizer.record(source)
        prompt = recognizer.recognize_google(audio)
        return prompt
    
    def close(self):
        self.stat = "false"
        self.driver.quit()
