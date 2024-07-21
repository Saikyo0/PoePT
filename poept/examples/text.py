from poept import PoePT

#setup needed everytime
bot = PoePT()
bot.login("<email>")

#basic prompt and answer
prompt = input("> ")
result = bot.ask("Assistant", prompt)
print("Response:", result)

#asking prompt and print while generating answer
import threading
def ask_bot():
    bot.ask("Assistant", "Write A Lorem Ipsum")
threading.Thread(target=ask_bot).start()
while bot.stat == "wait":
    print('\r' + bot.response, end='')

#asking prompt in a loop
while (True):
    prompt = input("> ")
    response = bot.ask(bot="Assistant", prompt=prompt)
    print(response)
    if(prompt=="exit"): break

#asking prompt with attached file
import os
prompt = input("> ")
file = os.path.abspath("test.jpg")
response = bot.ask(newchat=False, bot="Assistant", prompt=prompt, attach_file=file)
print(response)
