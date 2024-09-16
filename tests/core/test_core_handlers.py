from typing import cast
from unittest import mock

from pytest import raises
from pytest_mock import MockerFixture

from ears.core.events import PlaylistAction, PlaylistEvent
from ears.core.handlers import (
    on_broadcast_playlist_event,
    on_search_track_event,
    on_update_playlist_event,
)
from ears.core.models import Track
from ears.core.provider import BaseMusicProvider

from ears.protocols.messaging import (
    EventPublisherFactory,
    EventReceiver,
)

from ..const import (
    TEST_DESTINATION,
    TEST_EVENT,
    TEST_TRACK,
    TEST_TRACK_MATCHING,
    TEST_TRACK_METADATA,
    TEST_VALID_PLAYLIST_URN,
    TEST_VALID_TRACK_URN,
)


def test_on_broadcast_playlist_event(
    event_publisher_mock: mock.Mock,
    event_publisher_factory_mock: mock.Mock,
    mocker: MockerFixture,
    music_provider_mock: mock.Mock,
) -> None:
    event_receiver_mock = mocker.Mock()
    event_receiver_mock.receive.return_value = PlaylistEvent(
        action=PlaylistAction.broadcast,
        playlist=TEST_VALID_PLAYLIST_URN,
    )
    on_broadcast_playlist_event(
        cast(BaseMusicProvider, music_provider_mock),
        TEST_EVENT,
        cast(EventPublisherFactory, event_publisher_factory_mock),
        cast(EventReceiver, event_receiver_mock),
        TEST_DESTINATION,
    )
    event_publisher_factory_mock.create.assert_called_once_with(
        TEST_DESTINATION
    )
    event_receiver_mock.receive.assert_called_once_with(
        TEST_EVENT, PlaylistEvent
    )
    music_provider_mock.get_playlist.assert_called_once_with(
        TEST_VALID_PLAYLIST_URN
    )
    event_publisher_mock.publish.assert_called_once_with(TEST_TRACK)


def test_on_broadcast_playlist_event_with_invalid_action_type(
    event_publisher_factory_mock: mock.MagicMock,
    mocker: MockerFixture,
    music_provider_mock: mock.MagicMock,
) -> None:
    event_receiver_mock = mocker.Mock()
    event_receiver_mock.receive.return_value = PlaylistEvent(
        action=PlaylistAction.add,
        playlist=TEST_VALID_PLAYLIST_URN,
    )
    with raises(ValueError):
        on_broadcast_playlist_event(
            cast(BaseMusicProvider, music_provider_mock),
            TEST_EVENT,
            cast(EventPublisherFactory, event_publisher_factory_mock),
            cast(EventReceiver, event_receiver_mock),
            TEST_DESTINATION,
        )


def test_on_update_playlist_event_with_add_event(
    mocker: MockerFixture,
    music_provider_mock: mock.Mock,
) -> None:
    event_receiver_mock = mocker.Mock()
    event_receiver_mock.receive.return_value = PlaylistEvent(
        action=PlaylistAction.add,
        playlist=TEST_VALID_PLAYLIST_URN,
        track=TEST_VALID_TRACK_URN,
    )
    on_update_playlist_event(
        cast(BaseMusicProvider, music_provider_mock),
        TEST_EVENT,
        event_receiver_mock,
    )
    event_receiver_mock.receive.assert_called_once_with(
        TEST_EVENT, PlaylistEvent
    )
    music_provider_mock.add_to_playlist.assert_called_once_with(
        TEST_VALID_PLAYLIST_URN,
        TEST_VALID_TRACK_URN,
    )


def test_on_update_playlist_event_with_invalid_add_event(
    mocker: MockerFixture,
    music_provider_mock: mock.Mock,
) -> None:
    event_receiver_mock = mocker.Mock()
    event_receiver_mock.receive.return_value = PlaylistEvent(
        action=PlaylistAction.add,
        playlist=TEST_VALID_PLAYLIST_URN,
    )
    with raises(ValueError):
        on_update_playlist_event(
            cast(BaseMusicProvider, music_provider_mock),
            TEST_EVENT,
            event_receiver_mock,
        )


def test_on_update_playlist_event_with_remove_event(
    mocker: MockerFixture,
    music_provider_mock: mock.Mock,
) -> None:
    event_receiver_mock = mocker.Mock()
    event_receiver_mock.receive.return_value = PlaylistEvent(
        action=PlaylistAction.remove,
        playlist=TEST_VALID_PLAYLIST_URN,
        track=TEST_VALID_TRACK_URN,
    )
    on_update_playlist_event(
        cast(BaseMusicProvider, music_provider_mock),
        TEST_EVENT,
        event_receiver_mock,
    )
    event_receiver_mock.receive.assert_called_once_with(
        TEST_EVENT, PlaylistEvent
    )
    music_provider_mock.remove_from_playlist.assert_called_once_with(
        TEST_VALID_PLAYLIST_URN,
        TEST_VALID_TRACK_URN,
    )


def test_on_update_playlist_event_with_invalid_remove_event(
    mocker: MockerFixture,
    music_provider_mock: mock.Mock,
) -> None:
    event_receiver_mock = mocker.Mock()
    event_receiver_mock.receive.return_value = PlaylistEvent(
        action=PlaylistAction.remove,
        playlist=TEST_VALID_PLAYLIST_URN,
    )
    with raises(ValueError):
        on_update_playlist_event(
            cast(BaseMusicProvider, music_provider_mock),
            TEST_EVENT,
            event_receiver_mock,
        )


def test_on_update_playlist_event_with_invalid_event(
    mocker: MockerFixture,
    music_provider_mock: mock.Mock,
) -> None:
    event_receiver_mock = mocker.Mock()
    event_receiver_mock.receive.return_value = PlaylistEvent(
        action=PlaylistAction.broadcast,
        playlist=TEST_VALID_PLAYLIST_URN,
    )
    with raises(ValueError):
        on_update_playlist_event(
            cast(BaseMusicProvider, music_provider_mock),
            TEST_EVENT,
            event_receiver_mock,
        )


def test_on_search_track_event(
    event_publisher_mock: mock.Mock,
    event_publisher_factory_mock: mock.Mock,
    mocker: MockerFixture,
    music_provider_mock: mock.Mock,
) -> None:
    event_receiver_mock = mocker.Mock()
    event_receiver_mock.receive.return_value = TEST_TRACK
    on_search_track_event(
        cast(BaseMusicProvider, music_provider_mock),
        TEST_EVENT,
        cast(EventPublisherFactory, event_publisher_factory_mock),
        event_receiver_mock,
        TEST_DESTINATION,
    )
    event_publisher_factory_mock.create.assert_called_once_with(
        TEST_DESTINATION
    )
    event_receiver_mock.receive.assert_called_once_with(
        TEST_EVENT,
        Track,
    )
    music_provider_mock.search_track.assert_called_once_with(
        TEST_TRACK_METADATA,
    )
    event_publisher_mock.publish.assert_called_once_with(
        TEST_TRACK_MATCHING,
    )
