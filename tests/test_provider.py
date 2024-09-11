import pytest

from ears.core.exceptions import NotSupportedError
from ears.core.models import TrackSearchQuery
from ears.core.provider import BaseMusicProvider

from .const import (
    TEST_INVALID_PROVIDER_URNS,
    TEST_INVALID_URNS,
    TEST_VALID_URN,
    TEST_VALID_URN_ID,
    TEST_VALID_URN_PROVIDER,
    TEST_VALID_URN_TYPE,
)


class MusicProviderMock(BaseMusicProvider):
    def __init__(self) -> None:
        self.name = TEST_VALID_URN_PROVIDER


def test_base_music_provider_not_supported_methods() -> None:
    provider = MusicProviderMock()
    with pytest.raises(NotSupportedError):
        provider.get_playlist("playlist")
    with pytest.raises(NotSupportedError):
        provider.add_to_playlist("playlist", "track")
    with pytest.raises(NotSupportedError):
        provider.remove_from_playlist("playlist", "track")
    with pytest.raises(NotSupportedError):
        query = TrackSearchQuery(
            album="Hidden Paradise",
            artist="Demuja",
            title="Jazzy man",
        )
        provider.search_track(query)


def test_base_music_provider_parse_urn() -> None:
    provider = MusicProviderMock()
    for urn in TEST_INVALID_URNS + TEST_INVALID_PROVIDER_URNS:
        with pytest.raises(ValueError):
            provider.parse_urn(urn)
    resource = provider.parse_urn(TEST_VALID_URN)
    assert resource.id == TEST_VALID_URN_ID
    assert resource.provider == TEST_VALID_URN_PROVIDER
    assert resource.type == TEST_VALID_URN_TYPE
    assert resource.url is None
