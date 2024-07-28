#!/usr/bin/env python3

import argparse
import asyncio
from aiohttp import web
import logging
import concurrent.futures
from . import PoePT

logger = logging.getLogger(__name__)

# Updated handle_completion function
async def handle_completion(request):
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        return web.json_response({"error": "Invalid JSON"}, status=400)

    model = data.get('model', 'gpt4o')
    prompt = data.get('prompt')
    if not prompt:
        return web.json_response({"error": "Prompt is required"}, status=400)

    # Optional parameters
    max_tokens = data.get('max_tokens', 100)
    temperature = data.get('temperature', 1.0)
    # Add other parameters as needed

    llm = request.app['llm']
    executor = request.app['thread_executor']

    try:
        # Assuming llm.ask takes these parameters and returns a response
        response = await asyncio.get_event_loop().run_in_executor(
            executor, llm.ask, bot=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature
        )
    except Exception as e:
        logger.error(f"LLM execution error: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)

    # Format the response to be OpenAI-compatible
    return web.json_response({
        "id": "completion-id",
        "object": "text_completion",
        "created": int(asyncio.get_event_loop().time()),
        "model": model,
        "choices": [
            {
                "text": response,
                "index": 0,
                "logprobs": None,
                "finish_reason": "stop"
            }
        ]
    })

async def serve():
    app = web.Application(client_max_size=1024**4)
    app.router.add_post('/completition', handle_completion)
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