#!/usr/bin/env python3

import argparse
import asyncio
from aiohttp import web
import logging
import concurrent.futures
from poept import PoePT

logger = logging.getLogger(__name__)

# POST /completions HTTP/1.1
# Host: localhost:8080
# Accept-Encoding: gzip, deflate, br
# Connection: keep-alive
# Accept: application/json
# Content-Type: application/json
# User-Agent: OpenAI/Python 1.35.12
# X-Stainless-Lang: python
# X-Stainless-Package-Version: 1.35.12
# X-Stainless-OS: MacOS
# X-Stainless-Arch: x64
# X-Stainless-Runtime: CPython
# X-Stainless-Runtime-Version: 3.12.4
# Authorization: Bearer no
# X-Stainless-Async: false
# Content-Length: 180

# {"model": "gpt-3.5-turbo-instruct", "prompt": ["hello"], "frequency_penalty": 0, "logit_bias": {}, "max_tokens": 256, "n": 1, "presence_penalty": 0, "temperature": 0.7, "top_p": 1}HTTP/1.1 404 Not Found
# Content-Type: text/plain; charset=utf-8
# Content-Length: 14
# Date: Sun, 28 Jul 2024 11:19:36 GMT
# Server: Python/3.12 aiohttp/3.9.5

# or
# POST /chat/completions HTTP/1.1

# {"messages": [{"content": "hello", "role": "user"}], "model": "gpt-3.5-turbo", "n": 1, "stream": false, "temperature": 0.7}HTTP/1.1 404 Not Found
# Content-Type: text/plain; charset=utf-8
# Content-Length: 14
# Date: Sun, 28 Jul 2024 11:12:56 GMT
# Server: Python/3.12 aiohttp/3.9.5


async def handle_chat_completions(request):
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        return web.json_response({"error": "Invalid JSON"}, status=400)

    model = data.get('model', 'gpt4o')

    messages = data.get('messages', [])
    if not messages:
        return web.json_response({"error": "Messages are required"}, status=400)

    prompt = " ".join([message["content"] for message in messages if message["role"] == "user"])

    if not prompt:
        return web.json_response({"error": "User message is required"}, status=400)

    # max_tokens = data.get('max_tokens', 100)
    # temperature = data.get('temperature', 1.0)
    # n = data.get('n', 1)

    llm = request.app['llm']
    executor = request.app['thread_executor']

    try:
        response_text = await asyncio.get_event_loop().run_in_executor(
            executor, llm.ask, prompt, model
        )
    except Exception as e:
        logger.error(f"LLM execution error: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)

    # https://platform.openai.com/docs/api-reference/chat/create
    return web.json_response({
        "id": llm.get_chat_id(),
        "object": "chat.completion",
        "created": int(asyncio.get_event_loop().time()),
        "model": model,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response_text,
                },
                "index": 0,
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    })

async def handle_completions(request):
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        return web.json_response({"error": "Invalid JSON"}, status=400)

    model = data.get('model', 'gpt4o')
    prompt = data.get('prompt', [])
    if not prompt:
        return web.json_response({"error": "Prompt is required"}, status=400)

    prompt = " ".join(prompt)

    # max_tokens = data.get('max_tokens', 100)
    # temperature = data.get('temperature', 1.0)
    # n = data.get('n', 1)

    llm = request.app['llm']
    executor = request.app['thread_executor']

    try:
        response_text = await asyncio.get_event_loop().run_in_executor(
            executor, llm.ask, prompt, model
        )
    except Exception as e:
        logger.error(f"LLM execution error: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)

    # https://platform.openai.com/docs/api-reference/completions/create?lang=curl
    return web.json_response({
        "id": llm.get_chat_id(),
        "object": "text_completion",
        "created": int(asyncio.get_event_loop().time()),
        "model": model,
        "choices": [
            {
                "text": response_text,
                "index": 0,
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    })

async def serve():
    app = web.Application(client_max_size=1024**4)
    app.router.add_post('/chat/completions', handle_chat_completions)
    app.router.add_post('/completions', handle_completions)
    app['llm'] = PoePT()
    app['thread_executor'] = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    return app

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(serve())
    web.run_app(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()