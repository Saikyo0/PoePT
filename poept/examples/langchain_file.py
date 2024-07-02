#!/usr/bin/env python3

from poept.langchain import PoeLLM
import logging

logging.basicConfig(level=logging.INFO)

poe_llm = PoeLLM()

content = """
The GPT (Generative Pre-trained Transformer) language model was invented by researchers at OpenAI, a leading artificial intelligence research company. The first version, GPT-1, was introduced in 2018. Since then, OpenAI has developed more advanced versions of the GPT model, with GPT-3 being the latest and most powerful iteration as of August 2023.
The key researchers behind the development of the GPT models include:
Alec Radford: A senior research scientist at OpenAI who was a lead author on the original GPT paper.
Jeffrey Wu: Another senior research scientist at OpenAI and a co-author on the GPT papers.
Ilya Sutskever: The co-founder and chief scientist at OpenAI, who provided high-level guidance and supervision for the GPT research.
The GPT models have been groundbreaking in the field of natural language processing, demonstrating impressive capabilities in tasks like language generation, question answering, and text summarization. The models have been widely adopted and built upon by the broader AI research community.
"""

response = poe_llm.invoke(f"Make it shorter. One sentence.<<<{content}>>>")
print(response)
input()
