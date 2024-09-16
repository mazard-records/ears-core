import json
from base64 import b64decode
from concurrent.futures import Future
from functools import partial
from typing import Any, Type, cast

from ears.protocols.messaging import (
    EventPublisher,
    EventPublisherFactory,
    EventReceiver,
)
from google.cloud.pubsub_v1 import PublisherClient  # type: ignore
from pydantic import Field
from pydantic_settings import BaseSettings

from ...types import Event, PydanticModelType


class PublisherSettings(BaseSettings):
    project: str = Field(..., alias="GOOGLE_PROJECT_ID")


class GoogleEventPublisher(EventPublisher):
    """ """

    def __init__(self, client: PublisherClient, topic: str) -> None:
        self._client = client
        self._topic = topic
        self._publish = partial(self._client.publish, self._topic)

    def publish(self, event: Event | PydanticModelType) -> None:
        payload: str
        if isinstance(event, dict):
            payload = json.dumps(event)
        else:
            payload = event.model_dump_json()
        future = cast(Future[Any], self._publish(payload.encode("utf-8")))
        future.result()


class GoogleEventPublisherFactory(EventPublisherFactory):
    """ """

    def __init__(self) -> None:
        self._client = PublisherClient()
        self._publishers: dict[str, EventPublisher] = dict()
        self._settings = PublisherSettings()

    def create(self, topic: str) -> EventPublisher:
        if topic not in self._publishers:
            self._publishers[topic] = GoogleEventPublisher(
                self._client,
                f"projects/{self._settings.project}/topics/{topic}",
            )
        return self._publishers[topic]


class GoogleEventReceiver(EventReceiver):
    """ """

    def receive(
        self, event: Event, model: Type[PydanticModelType]
    ) -> PydanticModelType:
        if "data" not in event:
            raise ValueError("Missing event data")
        payload = b64decode(event["data"]).decode("utf-8")
        return model(**json.loads(payload))
