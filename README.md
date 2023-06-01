# PoePT
PoePT is a Selenium Python package that provides a simple interface for interacting with the Poe chatbot.
Giving you access to multiple chatbots like:
- ChatGPT-3
- ChatGPT-4
- Claude-Instant  
 <br />


## Installation
You can install PoePT using pip:
```
pip install poept
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
- Once you're logged in, you can ask a question to the chatbot of your choice and retrieve the response:

```python
response = bot.ask(bot="sage", prompt="hello")
print(response)
```
- When you're done with your session, be sure to close the connection:

```python
bot.close()
```


  
<br />

## Extra

- status of client

```python
status = bot.status()
```
| Status | Meanings                                 |
|--------|------------------------------------------|
| false  | the bot isn't connected and cant answer  |
| ready  | the bot is connected and ready to answer |
| wait   | the bot is generating an answer          |
  
<br />

- Live voice Input

```python
print("Listening...") 
question = poept.livevoice(timeout=2)
print("Recording complete.")
result = poept.ask(bot="sage", prompt=question)
print("\nresponse:", result)
```
  
<br />

- File voice Input
```python
question = poept.filevoice("audio.wav")
result = poept.ask(bot="sage", prompt=question)
print("\nresponse:", result)
```
  
<br />

- clear cookies

```python
status = bot.status()
```
  
<br />

- configure classes and keys
```python
    bot.config(
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
        msg_element="ChatMessage_messageRow__7yIr2"
    )
```

| KEY           | Value                                                     |
|---------------|-----------------------------------------------------------|
| website       | "https://poe.com/"                                        |
| clear_key     | "ChatMessageInputFooter_chatBreakButton__hqJ3v"           |
| code_area     | "input.VerificationCodeInput_verificationCodeInput__YD3KV"|
| talk_key      | "//button[contains(., 'Talk')]"                           |
| email_area    | "input[type='email']"                                     |
| email_key     | "//button[contains(., 'Email')]"                          |
| go_key        | "//button[contains(., 'Go')]"                             |
| log_key       | "//button[contains(., 'Log')]"                            |
| text_area     | "GrowingTextArea_textArea__eadlu"                         |
| send_key      | "button.ChatMessageSendButton_sendButton__OMyK1"          |
| chat_element  | "ChatMessagesView_infiniteScroll__K_SeP"                  |
| msg_element   | "ChatMessage_messageRow__7yIr2"                           |
  
<br />

## Contributing 
If you encounter a bug or would like to suggest a new feature, please open an issue on the GitHub repository. Pull requests are also welcome! 

<a href=https://github.com/saikyo0>saikyo0</a>
