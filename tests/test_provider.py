import pytest

from ears.core.exceptions import NotSupportedError
from ears.core.provider import BaseMusicProvider

from .const import (
    TEST_INVALID_PROVIDER_URNS,
    TEST_INVALID_URNS,
    TEST_TRACK_SEARCH_QUERY,
    TEST_VALID_TRACK_URN,
    TEST_VALID_TRACK_URN_ID,
    TEST_VALID_TRACK_URN_PROVIDER,
    TEST_VALID_TRACK_URN_TYPE,
)


class NoOpMusicProvider(BaseMusicProvider):
    def __init__(self) -> None:
        self.name = TEST_VALID_TRACK_URN_PROVIDER


def test_base_music_provider_not_supported_methods() -> None:
    music_provider = NoOpMusicProvider()
    with pytest.raises(NotSupportedError):
        music_provider.get_playlist("playlist")
    with pytest.raises(NotSupportedError):
        music_provider.add_to_playlist("playlist", "track")
    with pytest.raises(NotSupportedError):
        music_provider.remove_from_playlist("playlist", "track")
    with pytest.raises(NotSupportedError):
        music_provider.search_track(TEST_TRACK_SEARCH_QUERY)


def test_base_music_provider_parse_urn() -> None:
    music_provider = NoOpMusicProvider()
    for urn in TEST_INVALID_URNS + TEST_INVALID_PROVIDER_URNS:
        with pytest.raises(ValueError):
            music_provider.parse_urn(urn)
    resource = music_provider.parse_urn(TEST_VALID_TRACK_URN)
    assert resource.id == TEST_VALID_TRACK_URN_ID
    assert resource.provider == TEST_VALID_TRACK_URN_PROVIDER
    assert resource.type == TEST_VALID_TRACK_URN_TYPE
    assert resource.url is None
