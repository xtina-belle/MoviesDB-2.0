import typing
import http

import requests

from omdb.omdb_movie_dto import OMDBMovieDto

API_KEY = "5ab0386"
BASE_URL = "http://www.omdbapi.com/"
DEFAULT_TIMEOUT = 10


class OMDBAPIClient:
    """A class representing a client that interacts with OMDB API."""
    @staticmethod
    def get_omdb_movie(name: str) -> typing.Optional[OMDBMovieDto]:
        """
        Gets data from API
        :param name: string, name of movie
        :return: OMDBMovieDto
        """
        response = requests.get(BASE_URL, params={"apikey": API_KEY, "t": name},
                                timeout=DEFAULT_TIMEOUT)
        if response.status_code != http.HTTPStatus.OK:
            print(f"Failed to load data from API. Status code: {response.status_code}")
            return None

        data = response.json()
        try:
            return OMDBMovieDto(
                name=data["Title"],
                rating=float(data["Ratings"][0]["Value"].strip("/10")),
                year=int(data["Year"].split("–")[0]),
                poster=data["Poster"],
            )
        except KeyError:
            print(f"Movie {name} not found!")
            return None
