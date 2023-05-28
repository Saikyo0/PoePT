# PoePT
PoePT is a Selenium Python package that provides a simple interface for interacting with the Poe chatbot.
Giving you access to multiple chatbots like:
- ChatGPT-3
- ChatGPT-4
- Claude-Instant 

### Installation
You can install PoePT using pip:
```
pip install poept
```

### Requirements:
- a POE account
- Chrome

### Usage
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
- When you're donewith your session, be sure to close the connection:

```python
bot.close()
```
- status of client

```python
status = bot.status()
```
| Status | Meanings                                 |
|--------|------------------------------------------|
| false  | the bot isn't connected and cant answer  |
| ready  | the bot is connected and ready to answer |
| wait   | the bot is generating an answer          |

### Plans
Adding config option to make elements selectable for filtering, so that the package avoids death making new features like voice input work

### Contributing 
If you encounter a bug or would like to suggest a new feature, please open an issue on the GitHub repository. Pull requests are also welcome!