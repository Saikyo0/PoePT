import os
import argparse
from langchain_openai import OpenAI

def get_api_client(api_base=os.environ.get("API_BASE", "http://localhost:8080"), model='gpt4o'):
    return OpenAI(
            openai_api_base=api_base,
            openai_api_key="no",
            model=model
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=False)
    parser.add_argument("--model", default='gpt4o', type=str, help="Poe bot")
    args = parser.parse_args()

    llm = get_api_client(model=args.model)

    if args.prompt:
        print(llm.invoke(args.prompt))
    else:
        while True:
            prompt = input("> ")
            response = llm.invoke(prompt)
            print(response)

if __name__ == "__main__":
        main()