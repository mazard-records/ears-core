from typing import Sequence

from ears.core.models import (
    MusicResource,
    MusicResourceType,
    Track,
    TrackMetadata,
    TrackSearchQuery,
    EMPTY_TRACK_SEQUENCE,
)
from ears.core.provider import BaseMusicProvider
from ears.core.types import URN

from .client import BeatportClient
from .models import BeatportTrack, BeatportSearchQuery
from .transport import BASE_URL


class BeatportProvider(BaseMusicProvider):
    """ """

    def __init__(self, client: BeatportClient) -> None:
        """ """
        self.name = "beatport"
        self.client = client

    def add_to_playlist(self, playlist_urn: URN, track_urn: URN) -> None:
        """ """
        track_resource = self.parse_urn(track_urn)
        playlist_resource = self.parse_urn(playlist_urn)
        playlist_proxy = self.client.playlist(playlist_resource.id)
        playlist_proxy.add(track_resource.id)

    def remove_from_playlist(self, playlist_urn: URN, track_urn: URN) -> None:
        """ """
        track_resource = self.parse_urn(track_urn)
        playlist_resource = self.parse_urn(playlist_urn)
        playlist_proxy = self.client.playlist(playlist_resource.id)
        playlist_proxy.remove(track_resource.id)

    def _to_ears_track(self, track: BeatportTrack) -> Track:
        """ """
        if len(track.artists) == 0:
            artist = "Unknown"
        else:
            artist = track.artists[0].name
        return Track(
            metadata=TrackMetadata(
                album=track.release.name,
                artist=artist,
                title=track.name,
                cover=track.image.uri,
                preview=track.sample_url,
            ),
            resource=MusicResource(
                id=track.id,
                provider=self.name,
                type=MusicResourceType.track,
                url=f"{BASE_URL}/track/{track.slug}/{track.id}",
            ),
        )

    def search_track(self, query: TrackSearchQuery) -> Sequence[Track]:
        """ """
        beatport_query = BeatportSearchQuery(
            artist=query.artist,
            title=query.title,
        )
        results = self.client.search(beatport_query)
        if results.tracks is None:
            return EMPTY_TRACK_SEQUENCE
        return [self._to_ears_track(track) for track in results.tracks]
