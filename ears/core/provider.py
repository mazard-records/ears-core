from typing import Optional, Protocol, Sequence

from .models import MusicResource, Track, TrackSearchQuery
from ..exceptions import NotSupportedError
from ..types import URN


class BaseMusicProvider(Protocol):
    """ """

    name: str

    def get_playlist(self, playlist_urn: URN) -> Sequence[Track]:
        raise NotSupportedError()

    def add_to_playlist(self, playlist_urn: URN, track_urn: URN) -> None:
        raise NotSupportedError()

    def remove_from_playlist(self, playlist_urn: URN, track_urn: URN) -> None:
        raise NotSupportedError()

    def search_track(self, query: TrackSearchQuery) -> Sequence[Track]:
        raise NotSupportedError()

    def parse_urn(self, urn: Optional[str]) -> MusicResource:
        resource = MusicResource.from_urn(urn)
        if resource.provider != self.name:
            raise ValueError(
                f"Provider mismatch, expected {self.name},"
                f" got {resource.provider}"
            )
        return resource
