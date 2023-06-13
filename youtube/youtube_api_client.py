import http
import typing

import requests

from youtube.youtube_trailer_dto import YoutubeTrailerDto

BASE_URL = "https://www.googleapis.com/youtube/v3"
DEFAULT_TIMEOUT = 10
GOOGLE_API_KEY = "AIzaSyC3oMSPDxIH-JYAnoryumyebMWNb7nnY6Y"


class YoutubeAPIClient:
    """A class representing a client that interact with youtube API."""
    @staticmethod
    def get_trailer(name: str) -> typing.Optional[YoutubeTrailerDto]:
        """
        Gets data from API
        :param name: string, name of movie
        :return: YoutubeTrailerDto
        """
        params = {
            "key": GOOGLE_API_KEY,
            "part": "snippet",
            "q": f"{name} trailer",
            "maxResults": "1",
        }
        response = requests.get(f"{BASE_URL}/search", params=params, timeout=DEFAULT_TIMEOUT)
        if response.status_code != http.HTTPStatus.OK:
            print(f"Failed to load data from Google API. Status code: {response.status_code}")
            return None

        trailer_data = response.json()
        return YoutubeTrailerDto(
            trailer_id=trailer_data["items"][0]["id"]["videoId"],
        )
