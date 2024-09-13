from typing import Generator
from unittest import mock

from pytest import fixture
from pytest_mock import MockerFixture

from .const import (
    TEST_TRACK,
    TEST_VALID_TRACK_URN_PROVIDER,
)

MockGenerator = Generator[mock.Mock, None, None]


@fixture(scope="function")
def event_publisher_mock(
    mocker: MockerFixture,
) -> MockGenerator:
    yield mocker.Mock()


@fixture(scope="function")
def event_publisher_factory_mock(
    event_publisher_mock: mock.Mock,
    mocker: MockerFixture,
) -> MockGenerator:
    event_publisher_factory = mocker.Mock()
    event_publisher_factory.create.return_value = event_publisher_mock
    yield event_publisher_factory


@fixture(scope="function")
def music_provider_mock(
    mocker: MockerFixture,
) -> MockGenerator:
    music_provider = mocker.Mock()
    music_provider.name = TEST_VALID_TRACK_URN_PROVIDER
    music_provider.get_playlist.return_value = (TEST_TRACK,)
    music_provider.search_track.return_value = (TEST_TRACK,)
    yield music_provider
