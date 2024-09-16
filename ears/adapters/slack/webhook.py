from functools import lru_cache
from typing import Any, Callable, Coroutine
from httpx import AsyncClient, Client

from .blocks import Blocks

AsyncWebhook = Callable[[Blocks], Coroutine[Any, Any, None]]
Webhook = Callable[[Blocks], None]


@lru_cache(maxsize=10)
def SlackWebhook(url: str) -> Webhook:
    client = Client()

    def webhook(blocks: Blocks) -> None:
        response = client.post(url, json=blocks.model_dump())
        response.raise_for_status()

    return webhook


@lru_cache(maxsize=10)
def AsyncSlackWebhook(url: str) -> AsyncWebhook:
    client = AsyncClient()

    async def webhook(blocks: Blocks) -> None:
        response = await client.post(url, json=blocks.model_dump())
        response.raise_for_status()

    return webhook
