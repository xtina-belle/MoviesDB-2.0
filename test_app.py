import random

import pytest

from movie_app_client import MovieAppClient
from db.movie_storage_json import MovieDBJson
from db.movie_storage_csv import MovieDBCsv
from db.movie_dto import MovieDto
from omdb.omdb_api_client import OMDBAPIClient
from youtube.youtube_api_client import YoutubeAPIClient


db = MovieDBJson("db/moviesDB.json")
db.setup()


def test_setup():
    client = MovieAppClient(MovieDBCsv("db/moviesDB.csv"))
    client.setup()
    assert client._movie_db._title_to_movie_dto


def test_delete():
    movie = "You"
    db.delete(movie)
    assert movie not in db._title_to_movie_dto


def test_get_movie():
    movies = list(db.get_movies().keys())
    movie = movies[random.choice(range(len(movies)))]
    assert isinstance(db.get_movie(movie), MovieDto)


def test_upsert():
    name = "You"
    if not db.is_movie_exist(name):
        omdb_movie_dto = OMDBAPIClient.get_omdb_movie(name)
        trailer_dto = YoutubeAPIClient.get_trailer(name)
        if omdb_movie_dto and trailer_dto:
            db.upsert(MovieDto(
                name=omdb_movie_dto.name,
                rating=omdb_movie_dto.rating,
                year=omdb_movie_dto.year,
                poster=omdb_movie_dto.poster,
                trailer_id=trailer_dto.trailer_id,
            ))
            assert name in db._title_to_movie_dto


def test_is_movie_exist():
    movie = "dfghjk"
    assert not db.is_movie_exist(movie)


def test_search_movie():
    name = "Godfather"
    found_movies = []
    for movie in db.search_movie(name):
        found_movies.append(movie.name)
    assert found_movies == ["The Godfather", "The Godfather: Part 2"]


def test_sort_by_rating():
    rating = 10
    for title, movie in db.sort_by_rating().items():
        assert rating >= movie.rating
        rating = movie.rating


def test_get_best_movies():
    rates = [movie_dto.rating for movie_dto in db._title_to_movie_dto.values()]
    for best in db.get_best_movies():
        for rate in rates:
            assert db._title_to_movie_dto[best].rating >= rate


def test_get_worst_movies():
    rates = [movie_dto.rating for movie_dto in db._title_to_movie_dto.values()]
    for best in db.get_worst_movies():
        for rate in rates:
            assert db._title_to_movie_dto[best].rating <= rate


#def test_

pytest.main()
