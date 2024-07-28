# PoePT
PoePT is a simple Selenium Python package that provides automation for interacting with the Poe chatbots.
Giving you access to multiple chatbots like:
- gpt-4o
- gpt-4
- Assistant
- Web-Search
- Claude-3.5-Sonnet
- Claude-3-Sonnet
- Claude-3-Opus
- [Claude-3-Haiku](https://poe.com/Claude-3-Haiku)
- Gemini-1.5-Flash-128k
- Gemini-1.5-Pro
- Claude-Instant
- Mistral-Large
- Mistral-Medium
- [Gemini-1.5-Flash-1M](https://poe.com/Gemini-1.5-Flash-1M)
- [Gemini-1.5-Pro-2M](https://poe.com/Gemini-1.5-Pro-2M)

 <br />


## Installation
You can install PoePT using pip:
```
pip install git+https://github.com/dzianisv/poept
```
<br />


## Requirements:
- a POE account (make one at poe.com)
- Chrome


<br />


## Quick Start

`python3 -m poept.server` | start http OpenAI compatible API
`python3 -m poept.client` | start client with interactive prompt

## Usage
Here's an example of how to use PoePT to log in to the Poe chatbot and ask a question:

- create connection with bot
- login is ***needed*** every time but will only ask for code if you havent logged in before
```python
from poept import PoePT

bot = PoePT(email=os.environ.get("POE_EMAIL"))

```
- Once you're logged in, you can ask a question to the chatbot of your choice and retrieve the result:

```python
result = bot.ask(model="gpt-4o", prompt="Who did invent GPT model?")
print(result)
```
- When you're done with your session, be sure to close the connection:

```python
bot.close()
```

<br />

<h2> Examples: <a href="https://github.com/Saikyo0/PoePT/blob/main/poept/examples"> link </a></h2>

<br />

## Env variables

- POE_HEADLESS=true
- POE_EMAIL=<your email>

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
import threading

bot = PoePT(email=os.environ.get("POE_EMAIL"))
def ask_bot():
    bot.ask("Sage", "Write A Lorem Ipsum")

threading.Thread(target=ask_bot).start()
while bot.stat == "wait":
    print(bot.stat)
    print('\r' + bot.response, end='')
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
