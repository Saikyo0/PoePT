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
- Once you're logged in, you can ask a question to the chatbot of your choice and retrieve the result:

```python
result = bot.ask(bot="sage", prompt="hello")
print(result)
```
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
status = bot.stat
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

bot = PoePT()
bot.login("mohammedaminsultan01@gmail.com") 
result = bot.ask(bot="sage", prompt="hello")

while(bot.stat == "wait"):
    print(bot.response)

#run the while loop by threading
```

- Live voice Input

```python
print("Listening...") 
question = bot.livevoice(timeout=2)
print("Recording complete.")
result = bot.ask(bot="sage", prompt=question)
print("\nresponse:", result)
```
  
<br />

- File voice Input
```python
question = bot.filevoice("audio.wav")
result = bot.ask(bot="sage", prompt=question)
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
    email_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'email')]",
    email_area="input[class*=EmailInput]", 
    code_area="input[class*=CodeInput",
    go_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'go')]",
    log_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'log')]",
    talk_key=f"//button[contains(translate(., '{letters[0]}', '{letters[-1]}' ), 'talk')]",
    send_key="button[class*=SendButton]",
    text_area="textarea[class*=TextArea]", 
    clear_key="button[class*=ChatBreak]",
    msg_element="ChatMessage_messageRow__7yIr2"
)
```
Here's the updated table:

| KEY           | Value                                                     |
|---------------|-----------------------------------------------------------|
| website       | "https://poe.com/"                                        |
| clear_key     | "button[class*=ChatBreak]"                                |
| code_area     | "input[class*=VerificationCodeInput]"                     |
| talk_key      | "//button[contains(translate(., 'a', 'A'), 'talk')]"       |
| email_area    | "input[class*=EmailInput]"                                |
| email_key     | "//button[contains(translate(., 'a', 'A'), 'email')]"      |
| go_key        | "//button[contains(translate(., 'a', 'A'), 'go')]"         |
| log_key       | "//button[contains(translate(., 'a', 'A'), 'log')]"        |
| text_area     | "textarea[class*=TextArea]"                               |
| send_key      | "button[class*=SendButton]"                               |
| chat_element  | "div[class*=ChatMessagesView_infiniteScroll]"             |
| msg_element   | "div[class*=ChatMessage_messageRow]"                       |
<br />

## Contributing 
If you encounter a bug open an issue on the GitHub repository. Pull requests are also welcome! 

<a href=https://github.com/saikyo0>saikyo0</a>