# PoePT

<img src="https://psc2.cf2.poecdn.net/assets/_next/static/media/poeFullWhiteMultibot.e2e2745a.svg" width="100" />


PoePT is a simple Selenium Python package that provides automation for interacting with the Poe chatbots.
Giving you access to multiple chatbots like:
- Assistant
- ChatGPT-3
- ChatGPT-4
- Gemini
- Bard
- Claude-Instant  
 <br />


## Installation
You can install PoePT using pip:
```
py -m pip install poept -U
```
or
```
py -m pip install git+https://github.com/Saikyo0/poept@main
```  
<br />


## Requirements:
- a POE account (make one at poe.com) 
- Chrome

  
<br />

## Usage
Here's an example of how to use PoePT to log in to the Poe chatbot and ask a question:

- create connection with bot
- login is ***needed*** every time but will only ask for code if you havent logged in before
```python
from poept import PoePT

bot = PoePT()
bot.login("your_email@example.com") 
```
- Once you're logged in, you can ask a question to the chatbot of your choice and retrieve the result

```python
result = bot.ask(newchat=False, bot="Assistant", prompt="hello")
print(result)
```
- the `newchat` parameter is used for either staying in the same chat for upcoming prompts or making new chat, but its ignored on the first question
- When you're done with your session, be sure to close the connection:

```python
bot.close()
```

<br />

<h2> Examples: <a href="https://github.com/Saikyo0/PoePT/blob/main/poept/examples"> link </a></h2>

<br />

## Extra

- status of client

```python
status = bot.status
```
| Status | Meanings                                 |
|--------|------------------------------------------|
| false  | the bot isn't connected and cant answer  |
| ready  | the bot is connected and ready to answer |
| wait   | the bot is generating an answer          |
  
<br />

- Get Live Updating Result

```python
from poept import PoePT
import threading

bot = PoePT()
bot.login("<email>@gmail.com") 

prompt = "Write A Lorem Ipsum"

def ask_bot():
    print("> "+prompt)
    bot.ask(bot="Assistant", prompt=prompt)

threading.Thread(target=ask_bot).start()
while True:
    if bot.prompt == prompt:
        if bot.status == "wait":
            print(bot.status)
            print('\r' + bot.response, end='')
        elif bot.status == "ready":
            break
```

<br />

- Image Response

```python
prompt = "An Apple"
result = bot.ask(bot="StableDiffusion3-2B", prompt=prompt, img_output=True)
print(result)
```

<br />

- Live voice Input
```python
print("Listening...") 
prompt = bot.live_voice(timeout=4)
print("Recording complete.")
result = bot.ask(bot="Assistant", prompt=prompt)
print("\nresponse:", result)
```

- File voice Input
```python
audio_file = os.path.abspath("audio.wav")
prompt = bot.file_voice(audio_file)
result = bot.ask(newchat=False, bot="Assistant", prompt=prompt)
print("\nresponse:", result)
```
  
<br />

- Cookie control
- default cookies path: `./saved_cookies/cookies.txt`

```python
bot.clear_cookies()
bot.load_cookies("path")
```
  
<br />

- configure classes and keys
```python
bot.config(self, website="https://poe.com/", #Base URL of POE.
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
            ):
```
<br />

## Contributing 
If you encounter a bug open an issue on the GitHub repository. Pull requests are also welcome! 

<a href=https://github.com/saikyo0>saikyo0</a>
