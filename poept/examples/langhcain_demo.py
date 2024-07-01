#!/usr/bin/env python3

from poept import PoeLLM
import os

poe_llm = PoeLLM(email=os.environ.get("POE_EMAIL"))
response = poe_llm("Hello, how are you?")
print(response)