#!/usr/bin/env python3
# pip install SpeechRecognition poept


from poept import PoePT
import os

bot = PoePT(email=os.environ.get("POE_EMAIL"))
prompt = """
The odd numbers in this group add up to an even number: 17,  9, 10, 12, 13, 4, 2.
A: Adding all the odd numbers (17, 9, 13) gives 39. The answer is False.

The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. 
A:
"""

print(bot.ask(prompt, "GPT-4o"))
print(bot.get_chat_id())




