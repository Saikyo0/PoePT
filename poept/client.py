#!/usr/bin/env python3

import argparse
from poept import PoePT
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot", type=str, default="Gpt4o")
    args = parser.parse_args()

    llm = PoePT()
    chat_id = None
    while True:
        prompt = input("> ")
        response = llm.ask(prompt, bot=args.bot, chat_id=chat_id)
        chat_id = llm.get_chat_id()
        print(response)

if __name__ == "__main__":
    main()