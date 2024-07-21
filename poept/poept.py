"""
PoePT Python Library.
#########################################

Usage --> ``bot = PoePT()``

Example -->

```
from poept import PoePT

bot = PoePT(headless=True)
bot.login("<your_email>")

while (True):
    prompt = input("> ")
    response = bot.ask(bot="Assistant", prompt=prompt)
    print(response)
    if(prompt=="exit"): break

bot.close()
```

# (The PoePT object needs to call login method)

#########################################
"""

import os
import json
import pyaudio
import logging
from seleniumbase import Driver, SB
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException 
from selenium.webdriver.support import expected_conditions as EC
from .tools import speech, record

# Configure logging
logging.basicConfig(filename='poebot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class PoePT:
    def __init__(self, 
                 headless=False, #Whether to run the browser in headless mode
        ):
        """
        Initialize the PoePT class with optional headless browser mode.
        """
        if not isinstance(headless, bool):
            raise ValueError("headless must be a boolean value.")
        
        self.headless = headless
        self.driver = Driver(headless2=headless)
        self.status = "false"
        self.current_bot = ""
        self.prompt = ""
        self.response = ""
        self.config()

    def clear_cookies(self):
        """
        Clear all cookies from the current driver session.
        
        Returns:
        - bool: True if cookies were cleared successfully, False otherwise.
        """
        if self.driver:
            self.driver.delete_all_cookies()
            print("Cookies cleared.")
            return True
        return False

    def load_cookies(self):
        """
        Load cookies from a saved file and add them to the current driver session.
        
        Returns:
        - bool: True if cookies were loaded successfully, False otherwise.
        """
        if self.driver:
            with open("saved_cookies/cookies.txt", 'r') as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return True
        return False

    def config(self, website="https://poe.com/", #Base URL of POE.
               email_form=".textInput_input__9YpqY", #CSS selector for the email input form.
               go_btn=".Button_buttonBase__Bv9Vx.Button_primary__6UIn0",  #CSS selector for the 'Go' button.
               code_form=".VerificationCodeInput_verificationCodeInput__RgX85", #CSS selector for the verification code input div.
               login_btn=".Button_buttonBase__Bv9Vx.Button_primary__6UIn0",  #CSS selector for the login button.
               query_input_form=".GrowingTextArea_textArea__ZWQbP", #CSS selector for the chat input div.
               query_send_btn=".ChatMessageSendButton_sendButton__4ZyI4",  #CSS selector for the chat send button.
               clear_key_btn=".ChatBreakButton_button__zyEye", #CSS selector for the clear chat button.
               file_input_form=".ChatMessageFileInputButton_input__svNx4",  #CSS selector for the file input div.
               file_input_box=".ChatMessageInputAttachments_container__AAxGu", #CSS selector for the file input box in chat.
               voice_input_btn=".ChatMessageVoiceInputButton_button__NjXno",  #CSS selector for the voice input button.
               msg_element=".ChatMessage_chatMessage__xkgHx", #CSS selector for the response message element div.
               msg_image="MarkdownImage_image__3dBzJ"#CSS selector for the response message picture element img.
            ):
        """
        Configure the web elements' selectors for interaction.
        """
        self.website = website
        self.clear_key_btn = clear_key_btn
        self.email_form = email_form
        self.go_btn = go_btn
        self.code_form = code_form
        self.login_btn = login_btn
        self.query_input_form = query_input_form
        self.query_send_btn = query_send_btn
        self.file_input_form = file_input_form
        self.file_input_box = file_input_box
        self.voice_input_btn = voice_input_btn
        self.msg_element = msg_element
        self.msg_image = msg_image

    def login(self, 
              email #Email address used for login.
              ):
        """
        Log in to the website using the provided email. 
        If cookies are saved, load them instead.

        Returns:
        - bool: True if login successful, False otherwise.
        """
        if not isinstance(email, str):
            raise ValueError("email must be a string.")
        
        if os.path.exists("saved_cookies/cookies.txt"):
            logging.info("Existing cookies found at ./saved_cookies/cookies.txt")
            self.status = "ready"
            return True

        try:
            with SB(headless2=self.headless) as sb:
                sb.open(self.website)
                sb.type(self.email_form, email)
                sb.click(self.go_btn)
                print("Verification email sent...")
                sb.assert_element(self.code_form)

                code = input("Enter Code: ")
                sb.type(self.code_form, code)
                sb.click(self.login_btn)
                sb.assert_element(self.query_input_form)
                sb.save_cookies(name="cookies.txt")
                self.status = "ready"
                return True
            
        except Exception as e:
            logging.error("Login Error: WebDriver not initialized.")
            logging.error(e)
            return False

    def ask(self, 
            newchat=True, #Flag indicating whether to start a new chat session. ignored if its first question
            bot="Assistant", #Username of the bot to interact with.
            prompt="", #Query message to send to the bot.
            attach_file="", #Absolute path of a file to attach (if any).
            img_output=False, #If the response should contain an image.
            ):
        """
        Send a query to the chatbot and receive a response.
        
        Returns:
        - str: Response from the chatbot.
        """
        if not isinstance(newchat, bool):
            raise ValueError("newchat must be a boolean value.")
        if not isinstance(bot, str):
            raise ValueError("bot must be a string.")
        if not isinstance(prompt, str):
            raise ValueError("prompt must be a string.")
        if not isinstance(attach_file, str):
            raise ValueError("attach_file must be a string.")
        
        if not self.driver:
            logging.error("WebDriver not initialized. Please login first.")
            raise RuntimeError("WebDriver not initialized. Please login first.")

        self.status = "wait"

        if newchat or self.current_bot != bot:
            self.driver.get(f"{self.website}{bot}")
            self.current_bot = bot
            self.load_cookies()
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.query_input_form)))
        
        try:
            self.prompt = prompt
            self.driver.find_element(By.CSS_SELECTOR, self.query_input_form).send_keys(prompt)
            
            if attach_file:
                if not os.path.exists(attach_file):
                    raise FileNotFoundError(f"The file {attach_file} does not exist.")
                self.driver.find_element(By.CSS_SELECTOR, self.file_input_form).send_keys(attach_file)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.file_input_box)))

            self.driver.find_element(By.CSS_SELECTOR, self.query_send_btn).click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.msg_element)))

            msg = None
            while True:
                try:
                    msg = self.driver.find_element(By.XPATH, f"(//div[@class='{self.msg_element[1:]}'])[last()]")
                    if msg.get_attribute("data-complete") == "false": break
                except (NoSuchElementException, StaleElementReferenceException):
                    pass
    
            while True:
                self.response = msg.text
                msg = self.driver.find_element(By.XPATH, f"(//div[@class='{self.msg_element[1:]}'])[last()]")
                if msg.get_attribute("data-complete") == "true": break
            
            if img_output:
                self.response = msg.find_element(By.CSS_SELECTOR, self.msg_image).get_attribute("src")

            self.response += '\n'.join(msg.text.split('\n')[2:])
            self.status = "ready"
            return self.response
        
        except Exception as e:
            logging.error(f"Exception occurred in ask method: {e}")
            return ""

    def clear_chat(self):
        """
        Clear the current chat session.
        
        Returns:
        - bool: True if chat cleared successfully, False otherwise.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Please login first.")
        try:
            self.driver.find_element(By.CSS_SELECTOR, self.clear_key_btn).click()
            print("Chat cleared.")
            return True
        
        except Exception as e:
            logging.error(e)
            return

    def live_voice(self,
                   timeout, #Timeout in seconds for recording voice input.
                   fs=44100, #Sampling frequency for recording.
                   micindex=-1, #Index of the microphone to use. empty for default
                   file="audio.wav", #File path to save the recorded audio.
                   chunk=1024, #Size of audio chunks for processing.
                ):
        """
        Record live voice input and convert it to text.
        
        Returns:
        - str: Text transcription of the recorded voice input.
        """
        if not isinstance(timeout, int):
            raise ValueError("timeout must be an integer.")
        if not isinstance(timeout, int):
            raise ValueError("timeout must be an integer.")
        if not isinstance(fs, int):
            raise ValueError("fs must be an integer.")
        if not isinstance(micindex, int):
            raise ValueError("micindex must be an integer.")
        if not isinstance(file, str):
            raise ValueError("file must be a string.")
        if not isinstance(chunk, int):
            raise ValueError("chunk must be an integer.")
        
        try:
            p = pyaudio.PyAudio()
            if (micindex == -1):
                micindex = p.get_default_input_device_info()['index']

            prompt = speech(record(timeout, fs, micindex, file, chunk))
            return prompt
        except Exception as e:
            logging.error(e)
            return

    def file_voice(self, 
                   file="audio.wav", #Absolute path to the audio file.
                   ):
        """
        Convert a recorded audio file to text.
        
        Returns:
        - str: Text transcription of the audio file.
        """
        if not isinstance(file, str):
            raise ValueError("file must be a string.")
        if not os.path.exists(file):
            raise FileNotFoundError(f"The file {file} does not exist.")
        
        try:
            prompt = speech(file)
            return prompt
        except Exception as e:
            logging.error(e)
            return
    
    def close(self):
        """
        Close the browser session.
        """
        if self.driver:
            self.driver.quit()
