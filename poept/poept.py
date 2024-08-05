import time
import os
import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import markdownify

from typing import Optional
from .tools import click, enter, speech, record
import logging
import json
import base64
from urllib.parse import urlparse

class BotNotFound(Exception):
    pass

class AuthenticationFailure(Exception):
    pass

class EmptyResponse(Exception):
    pass

logger = logging.getLogger(__name__)

default_bot = "Assistant"
website = "https://poe.com/"
letters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"]
email_area='input[type="email"]'
code_area="input[class*=CodeInput"
go_key='//button[text()="Go"]'
log_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'log')]"
clear_key="button[class*=ChatBreak]"
stop_button_selector="button[class*=ChatStopMessageButton]"
button_css_selector = "button[class*=SendButton]"


def to_markdown(element: WebElement) -> str:
    html = element.get_attribute('innerHTML')
    text =  markdownify.markdownify(html, escape_underscores=False, escape_asterisks=False)
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\s+([\.,!?])', r'\1', text)
    return text

class PoePT:
    cookies_file_path: str = os.path.expanduser("~/.cache/poept.cookies.json")
    alternative_cookies_file_path: str = os.path.realpath("./poept.cookies.json")

    def __init__(self,
            cookies: Optional[str] = os.environ.get("POE_COOKIES"),
            email: Optional[str] = os.environ.get("POE_EMAIL"),
            headless: bool = os.environ.get("POE_HEADLESS", "true") == "true",
        ):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-logging")
        # chrome_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        chrome_service = webdriver.chrome.service.Service()
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.stat = "false"

        self.cookies = None

        if cookies is not None:
            self.cookies = json.loads(base64.decodebytes(cookies.encode('utf8')))
            logger.info("Using passed cookies")

        if self.cookies is None:
            self.cookies = self.read_cookies()

        if self.cookies is None:
            if email is None:
                raise AuthenticationFailure("no cookies and email are set")
            else:
                self.login(email)
        else:
            # i noticed that sometimes cookies are not applied from first run :facepalm:
            # workaround
            for _ in range(3):
                if self.apply_cookies():
                    break
            else:
                raise AuthenticationFailure("cookies wasn't applied after a few attempts")

    def read_cookies(self):
        for cookies_file in [self.cookies_file_path, self.alternative_cookies_file_path]:
            if os.path.exists(cookies_file):
                logger.info(f"loading cookies from {self.cookies_file_path}")
                with open(cookies_file, 'rb') as f:
                    return json.load(f)

        return []

    def apply_cookies(self):
        if self.cookies is None:
            return False

        logger.info("Applying cookies...")
        self.driver.get(website)

        self.driver.delete_all_cookies()
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()

        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button[class*=ChatMessageSendButton_sendButton]')
            logger.info("Cookies were applied")
        except selenium.common.exceptions.NoSuchElementException as err:
            self.driver.save_screenshot(f"{__name__}-apply_cookies_failed.png")
            logger.exception("Failed to apply cookies: %s", err)
            return False

        return True

    def _web_element_to_markdown(self, element: WebElement) -> str:
        result = []

        def process_element(element: WebElement):
            # Check if the element is a code block
            elementClass = element.get_attribute('class')

            if any(cls.startswith('MarkdownCodeBlock_codeBlock') for cls in elementClass.split()):
                lang_element = element.find_element(By.CSS_SELECTOR, 'div[class*=MarkdownCodeBlock_languageName]')
                code_element = element.find_element(By.CSS_SELECTOR, 'code[class*=MarkdownCodeBlock_codeTag]')

                if lang_element and code_element:
                    lang_text = lang_element.text.strip()
                    code_text = code_element.text.strip()
                    result.append(f"```{lang_text}\n{code_text}\n```")
            elif elementClass and elementClass.startswith('PreviewFrame_container'):
                return
            elif element.tag_name == 'p':
                result.append(to_markdown(element))

            # Check if the element is a link
            elif element.tag_name == 'a':
                link_text = element.text.strip()
                url = element.get_attribute('href')
                if url is not None:
                    result.append(f"[{link_text}]({url})")

            # Check if the element is an image
            elif element.tag_name == 'img':
                alt = element.get_attribute('alt') or ''
                src = element.get_attribute('src') or ''
                result.append(f"![{alt}]({src})")

            # Check if the element is a list
            elif element.tag_name == 'ul':
                for li in element.find_elements(By.CSS_SELECTOR, 'li'):
                    result.append(f"- {to_markdown(li)}")
            elif element.tag_name == 'ol':
                for idx, li in enumerate(element.find_elements(By.CSS_SELECTOR, 'li'), start=1):
                    result.append(f"{idx}. {to_markdown(li)}")

            # For any other elements, recursively process children
            else:
                children = element.find_elements(By.XPATH, "./*")
                for child in children:
                    try:
                        process_element(child)
                    except selenium.common.exceptions.NoSuchElementException as err:
                        logger.error("failed to process the following element (%r): %s", element, err)

                if (not children or len(children) == 0) and element.text:
                    result.append(to_markdown(element))

        process_element(element)
        return '\n'.join(result)


    def get_message(self):
        actionBar_bar = WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section[class*='ChatMessageActionBar_actionBar']"))
        )

        elements = self.driver.find_elements(By.CSS_SELECTOR, "div[class*=ChatMessage_chatMessage]")
        chatMessage_element = elements[-1]

        next_element = chatMessage_element.find_element(By.XPATH, "following-sibling::*[1]")
        if next_element == actionBar_bar:
            bot_message = chatMessage_element.find_element(By.CSS_SELECTOR, "div[class*=Markdown_markdownContainer]")
            return self._web_element_to_markdown(bot_message)

        raise Exception("Message is not ready...")

    def clearchat(self):
        click(self.driver, By.CSS_SELECTOR, clear_key)

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


    def _typein(self, element, text):
        js_code = """
const element = arguments[0];
element.value = arguments[1];
element.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true }));
element.dispatchEvent(new KeyboardEvent('keypress', { bubbles: true }));
element.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
"""
        self.driver.execute_script(js_code, element, text)
        element.send_keys(' ')

    def goto(self, chat_id: str) -> Optional[str]:
        self.driver.execute_script(f"window.location.href = '{website}{chat_id}';")
        element = WebDriverWait(self.driver, 60).until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, button_css_selector)),
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class*=StatusCodeError_statusCode]"))
            )
        )

        if element.tag_name == 'h1':
            return element.text


    def ask(self, prompt="hello", bot=default_bot, chat_id: Optional[str] = None):
        start_ts = time.time()
        err = None
        for e in [chat_id, bot]:
            if e is None:
                continue

            err = self.goto(e)
            if err is None:
                break

        if err:
            logger.error("failed to open bot %s, %s", bot, chat_id)
            raise BotNotFound(bot)

        self.stat = "wait"

        input_area_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[class*=TextArea]"))
        )

        self._typein(input_area_element, prompt)

        for _ in range(5):
            send_button_element = self.driver.find_element(By.CSS_SELECTOR, button_css_selector)
            button_is_disabled = send_button_element.get_attribute("disabled") is not None

            if not button_is_disabled:
                break

            time.sleep(1)
            continue

        send_button_element.click()

        for _ in range(3):
            text = self.get_message()
            if text and len(text) > 0:
                break
        else:
            raise EmptyResponse(text)

        self.stat = "ready"

        t = time.time() - start_ts
        logger.info("%s %ds %s-> %s", bot, t, prompt, text)
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

    def get_chat_id(self) -> Optional[str]:
        # Get the current URL from the Selenium WebDriver
        current_url = self.driver.current_url

        # Parse the URL to extract the path
        parsed_url = urlparse(current_url)

        # Extract the part of the path starting with 'chat/'
        if 'chat/' in parsed_url.path:
            chat_part = parsed_url.path.split('chat/')[1]
            return f'chat/{chat_part}'
        else:
            return None