from ears.core.client import BaseClient
from ears.core.proxy import BaseClientProxy

from .models import BeatportPlaylist, BeatportSearchQuery, BeatportSearchResults


class BeatportPlaylistProxy(BaseClientProxy[BeatportPlaylist]):
    """ """

    def add(self, track_ids: int | list[int]) -> None:
        endpoint = f"/api/v4/my/playlists/{self.model.id}/tracks/bulk"
        if isinstance(track_ids, int):
            track_ids = [track_ids]
        payload = {"track_ids": track_ids}
        response = self.transport.post(endpoint, json=payload)
        response.raise_for_status()

    def remove(self, track_id: int) -> None:
        endpoint = f"/api/v4/my/playlists/{self.model.id}/tracks/{track_id}"
        response = self.transport.delete(endpoint)
        response.raise_for_status()


class BeatportClient(BaseClient):
    """ """

    def playlist(self, playlist_id: int) -> BeatportPlaylistProxy:
        endpoint = f"/api/v4/my/playlists/{playlist_id}"
        response = self.transport.get(endpoint)
        response.raise_for_status()
        playlist = BeatportPlaylist(**response.json())
        return BeatportPlaylistProxy(
            model=playlist,
            transport=self.transport,
        )

    def search(self, query: BeatportSearchQuery) -> BeatportSearchResults:
        endpoint = f"/api/v4/catalog/search?{query}"
        response = self.transport.get(endpoint)
        response.raise_for_status()
        return BeatportSearchResults(**response.json())
