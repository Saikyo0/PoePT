from poept import PoePT

bot = PoePT()
bot.login("mohammedaminsultan01@gmail.com")

#asking simple text
result = bot.ask("MongoT", "Hello!")
print("Answer:", result)

#asking simple text and print while generating answer
import threading
def ask_bot():
    bot.ask("Sage", "Write A Lorem Ipsum")
threading.Thread(target=ask_bot).start()
while bot.stat == "wait":
    print(bot.stat)
    print('\r' + bot.response, end='')
