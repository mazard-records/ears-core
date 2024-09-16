from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, Field, SecretStr

from ears.adapters.google import (
    GoogleEventReceiver,
    GoogleEventPublisherFactory,
)
from ears.handlers import playlist
from ears.handlers import search
from ears.providers.beatport import (
    BeatportClient,
    BeatportCredentials,
    BeatportProvider as BeatportProviderClass,
    BeatportTransportFactory,
)
from ears.types import Event


class BeatportSettings(BaseSettings):
    BEATPORT_USERNAME: SecretStr
    BEATPORT_PASSWORD: SecretStr

    def to_credentials(self) -> BeatportCredentials:
        return BeatportCredentials(
            username=self.BEATPORT_USERNAME,
            password=self.BEATPORT_PASSWORD,
        )


class Destinations(BaseSettings):
    search: str = Field(..., env="DESTINATION_SEARCH")


@lru_cache(maxsize=1)
def BeatportProvider() -> BeatportProviderClass:
    beatport_settings = BeatportSettings()
    beatport_credentials = beatport_settings.to_credentials()
    beatport_transport_factory = BeatportTransportFactory(beatport_credentials)
    beatport_client = BeatportClient(beatport_transport_factory)
    beatport_provider = BeatportProvider(beatport_client)
    return beatport_provider


def on_update_playlist_event(event: Event, _: Any) -> None:
    playlist.on_update_playlist_event(
        event,
        BeatportProvider(),
        GoogleEventReceiver(),
    )


def on_search_event(event: Event, _: Any) -> None:
    destinations = Destinations()
    search.on_search_track_event(
        event,
        BeatportProvider(),
        GoogleEventPublisherFactory(),
        GoogleEventReceiver(),
        destinations.search,
    )
