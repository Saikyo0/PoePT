#!/usr/bin/env python3

import argparse
import asyncio
import logging
import os
from aiohttp import web
import concurrent.futures
from poept import PoePT

logger = logging.getLogger(__name__)

# Authentication middleware
async def auth_middleware(app, handler):
    async def middleware_handler(request):
        auth_header = request.headers.get('Authorization', None)
        if auth_header is None or not auth_header.startswith('Bearer '):
            return web.json_response({"error": "Unauthorized"}, status=401)

        token = auth_header[7:]
        if token not in app['auth_tokens']:
            logger.warning("Rejected the user authentication token: %s", token)
            return web.json_response({"error": "Forbidden"}, status=403)

        return await handler(request)

    return middleware_handler

# Handlers
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

    llm = request.app['llm']
    executor = request.app['thread_executor']

    try:
        response_text = await asyncio.get_event_loop().run_in_executor(
            executor, llm.ask, prompt, model
        )
    except Exception as e:
        logger.error(f"LLM execution error: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)
    # https://platform.openai.com/docs/api-reference/completions/create?lang=curls
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

async def handle_health(request):
    return web.json_response({"status": "ok"})

# Setup and run the server
async def serve():
    auth_tokens = os.getenv('POE_AUTH_TOKENS')

    middlewares=[auth_middleware] if auth_tokens else []
    app = web.Application(middlewares=middlewares, client_max_size=1024**4)
    if auth_tokens:
        app['auth_tokens'] = {token.strip() for token in auth_tokens.split(',') if token.strip()}
        logger.info("Using authentication tokens: %r", app['auth_tokens'])

    app.router.add_post('/chat/completions', handle_chat_completions)
    app.router.add_post('/completions', handle_completions)
    app.router.add_get("/health", handle_health)
    app['llm'] = PoePT()
    app['thread_executor'] = concurrent.futures.ThreadPoolExecutor(max_workers=1)


    return app

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, default="127.0.0.1", help='listening hostname')
    parser.add_argument("--port", type=int, default=8080, help='listening port')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(serve())
    logger.info("Starting API server on %s:%d", args.hostname, args.port)
    web.run_app(app, host=args.hostname, port=args.port)

if __name__ == "__main__":
    main()