from poept import PoePT

#setup needed everytime
bot = PoePT()
bot.login("<email>")

#basic prompt and answer
prompt = input("> ")
result = bot.ask(bot="Assistant", prompt=prompt)
print("Response:", result)

#basic prompt and answer in the same chat
prompt = input("> ")
result = bot.ask(newchat=False, bot="Assistant", prompt=prompt)
print("Response:", result)

#asking prompt and print while generating answer
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
response = bot.ask(bot="Assistant", prompt=prompt, attach_file=file)
print(response)
