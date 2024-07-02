#!/usr/bin/env python3
# pip install SpeechRecognition poept


from poept import PoePT
import os

bot = PoePT()
bot.login(os.environ.get("POE_EMAIL"))

while True:
    prompt=input("> ")
    print(bot.ask(prompt, "gpt-4o"))



