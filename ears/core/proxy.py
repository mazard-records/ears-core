from typing import Any, Generic

from httpx import AsyncClient, Client

from .types import ModelClass, TransportClass


class BaseProxy(Generic[TransportClass, ModelClass]):
    """Base proxy class for client extension object."""

    def __init__(
        self,
        transport: TransportClass,
        model: ModelClass,
    ) -> None:
        self.model = model
        self.transport = transport

    def __getattr__(self, attr: str) -> Any:
        # TODO: check if exist first.
        return getattr(self.model, attr)


class BaseClientProxy(BaseProxy[Client, ModelClass]):
    pass


class BaseAsyncClientProxy(BaseProxy[AsyncClient, ModelClass]):
    pass
