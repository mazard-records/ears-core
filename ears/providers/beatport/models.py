from enum import Enum
from typing import Optional
from urllib.parse import urlencode

from pydantic import AnyHttpUrl, BaseModel, SecretStr


class BeatportCredentials(BaseModel):
    username: SecretStr
    password: SecretStr
    remember: bool = False


class BeatportImage(BaseModel):
    id: str
    uri: AnyHttpUrl


class BeatportArtist(BaseModel):
    id: int
    name: str
    slug: str
    url: str


class BeatportRelease(BaseModel):
    id: int
    name: str
    image: BeatportImage


class BeatportTrack(BaseModel):
    id: int
    name: str
    artists: list[BeatportArtist]
    image: BeatportImage
    mix_name: str
    release: BeatportRelease
    sample_url: AnyHttpUrl
    slug: str


class BeatportPlaylist(BaseModel):
    id: int


class BeatportSearchQueryType(str, Enum):
    tracks = "tracks"


class BeatportSearchQuery(BaseModel):
    title: str
    artist: str
    type: BeatportSearchQueryType = BeatportSearchQueryType.tracks

    def __str__(self) -> str:
        return urlencode(
            dict(
                type=self.type.value,
                q=self.title,
                artist_name=self.artist,
            ),
        )


class BeatportSearchResults(BaseModel):
    tracks: Optional[list[BeatportTrack]] = None

    # TODO: add validator ?
