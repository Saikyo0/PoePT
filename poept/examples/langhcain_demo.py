#!/usr/bin/env python3

from poept.langchain import PoeLLM
import logging

logging.basicConfig(level=logging.INFO)

poe_llm = PoeLLM()
response = poe_llm.invoke("Hello, how are you?")
print(response)