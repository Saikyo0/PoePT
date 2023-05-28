import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class PoePT:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")
        chrome_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    def clearcookies():
        os.remove("cookies.pkl")

    def login(self, email):
        try:
            self.driver.get("https://poe.com/")
            self.driver.delete_all_cookies()
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()

        except (FileNotFoundError, pickle.UnpicklingError):
            self.driver.get("https://poe.com/")
            self.driver.execute_script('window.scrollBy(0, 5);')
            time.sleep(0.1)
        
            while True:
                try:
                    time.sleep(0.1)
                    email_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                    email_input.send_keys(email)
                    break
                except:
                    try:
                        use_email_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Use email')]")
                        use_email_button.click()
                    except:
                        time.sleep(0.1)
        
            while True:
                try:
                    time.sleep(0.1)
                    go_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Go')]")
                    go_button.click()
                    break
                except:
                    time.sleep(0.1)
            
            code = input("Enter code: ")
            
            while True:
                try:
                    time.sleep(0.1)
                    code_input = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "input.VerificationCodeInput_verificationCodeInput__YD3KV"
                    )
                    code_input.send_keys(code)
                    break
                except:
                    time.sleep(0.1)
            
            while True:
                try:
                    time.sleep(0.1)
                    login_button = self.driver.find_element(
                        By.XPATH,
                        "//button[contains(text(), 'Log In')]"
                    )
                    login_button.click()
                    break
                except:
                    time.sleep(0.1)
            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def ask(self, bot="sage", prompt="hello"):
        self.driver.get("https://poe.com/"+bot)
        while True:
            try:
                time.sleep(0.1)
                textarea = self.driver.find_element(
                    By.CLASS_NAME,
                    "GrowingTextArea_textArea__eadlu"
                )
                textarea.send_keys(prompt)
                break
            except:
                time.sleep(0.1)
        while True:
            try:
                time.sleep(0.1)
                send_button = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button.ChatMessageSendButton_sendButton__OMyK1"
                )
                send_button.click()
                break
            except:
                time.sleep(0.1)
        while True:
            try:
                self.driver.find_element(
                    By.CLASS_NAME,
                    "ChatMessagesView_infiniteScroll__K_SeP"
                )
                break
            except:
                time.sleep(0.1)
        time.sleep(2)
        last_message = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located(
                (By.XPATH, "(//div[@class='ChatMessage_messageRow__7yIr2'])[last()][@data-complete='true']")
            )
        )
        responses = last_message.find_elements(
            By.XPATH, ".//div[contains(@class, 'Markdown_markdownContainer__UyYrv')]"
        )
        
        text = ""
        for response in responses:
            text += response.text+"\n"

        return text

    def close(self):
        self.driver.quit()
