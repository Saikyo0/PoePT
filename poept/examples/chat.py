#!/usr/bin/env python3
# pip install SpeechRecognition poept


from poept import PoePT

bot = PoePT()

while True:
    prompt=input("> ")
    print(bot.ask(prompt, "gpt-4o"))



