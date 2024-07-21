from poept import PoePT

bot = PoePT()
bot.login("<email>")

#asking live voice prompt
while (True):
    print("Listening...")
    prompt = bot.live_voice(timeout=4)
    if(prompt):
        print("> "+prompt)
        result = bot.ask(newchat=False, bot="Assistant", prompt=prompt)
        print(result)
        if(prompt.__contains__("bye")): break

#asking file voice prompt
import os
audio_file = os.path.abspath("audio.wav")
prompt = bot.file_voice(audio_file)
if(prompt):
    print("> "+prompt)
    result = bot.ask(bot="Assistant", prompt=prompt)
    print(result)

bot.close()
