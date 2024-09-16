from ears.core.models import MusicResource, MusicResourceType
from pytest import raises

from .const import (
    TEST_INVALID_URNS,
    TEST_VALID_TRACK_URN,
    TEST_VALID_TRACK_URN_ID,
    TEST_VALID_TRACK_URN_PROVIDER,
    TEST_VALID_TRACK_URN_TYPE,
)


def test_music_resource_from_urn() -> None:
    for urn in TEST_INVALID_URNS:
        with raises(ValueError):
            MusicResource.from_urn(urn)
    resource = MusicResource.from_urn(TEST_VALID_TRACK_URN)
    assert resource.id == TEST_VALID_TRACK_URN_ID
    assert resource.provider == TEST_VALID_TRACK_URN_PROVIDER
    assert resource.type == TEST_VALID_TRACK_URN_TYPE
    assert resource.url is None


def test_music_resource_to_urn() -> None:
    resource = MusicResource(
        id=69,
        provider="qobuz",
        type=MusicResourceType.track,
    )
    urn = resource.to_urn()
    assert urn == "urn:qobuz:track:69"
