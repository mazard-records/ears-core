from ears.core.models import (
    MusicResource,
    MusicResourceType,
    Track,
    TrackMatching,
    TrackMetadata,
    TrackSearchQuery,
)
from ears.types import Event

TEST_DESTINATION = "heaven"
TEST_EVENT: Event = dict()

TEST_INVALID_URNS = (None, "a:b:c:d:e", "ftp:a:b:c")
TEST_INVALID_PROVIDER_URNS = ("urn:apple:track:12", "urn:deezer:movie:23")

TEST_VALID_PLAYLIST_URN = "urn:spotify:playlist:51"
TEST_VALID_TRACK_URN = "urn:spotify:track:69"
TEST_VALID_TRACK_URN_ID = "69"
TEST_VALID_TRACK_URN_PROVIDER = "spotify"
TEST_VALID_TRACK_URN_TYPE = MusicResourceType.track

TEST_TRACK_METADATA = TrackMetadata(
    album="Hidden Paradise",
    artist="Demuja",
    title="Mr Jazzy Wung",
    cover="https://a/cover/url.jpg",
    preview="https://a/preview/url.mp3",
)

TEST_TRACK_RESOURCE = MusicResource(
    id=69,
    provider=TEST_VALID_TRACK_URN_PROVIDER,
    type=MusicResourceType.track,
)

TEST_TRACK_SEARCH_QUERY = TrackSearchQuery(
    album=TEST_TRACK_METADATA.album,
    artist=TEST_TRACK_METADATA.artist,
    title=TEST_TRACK_METADATA.title,
)

TEST_TRACK = Track(
    metadata=TEST_TRACK_METADATA,
    resource=TEST_TRACK_RESOURCE,
)

TEST_TRACK_MATCHING = TrackMatching(
    origin=TEST_TRACK_RESOURCE,
    destination=TEST_TRACK_RESOURCE,
    metadata=TEST_TRACK_METADATA,
)
