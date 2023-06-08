import statistics
import typing
from abc import ABC, abstractmethod

from db.movie_dto import MovieDto


class MovieDB(ABC):
    """
    A class representing a database.
    """

    def __init__(self, movie_db):
        self._movie_db = movie_db
        self._title_to_movie_dto = {}

    @abstractmethod
    def setup(self):
        """Loading the DB data to memory"""
        pass

    def delete(self, name):
        """Deletes a movie from the movie's database by name if exists"""
        self._title_to_movie_dto.pop(name, 0)
        self._flush_data()

    def get_movie(self, name) -> typing.Optional[MovieDto]:
        """Returns the MovieDto of the name given"""
        return self._title_to_movie_dto.get(name)

    def get_movies(self) -> typing.Dict[str, MovieDto]:
        """Returns a mapping between movie name to it's MovieDto"""
        return self._title_to_movie_dto

    def upsert(self, movie_dto: MovieDto):
        """Upserts a movie"""
        self._title_to_movie_dto[movie_dto.name] = movie_dto
        self._flush_data()

    def is_movie_exist(self, name) -> bool:
        """returns a boolean describing if movie exists"""
        return name.title() in self._title_to_movie_dto

    def search_movie(self, name) -> typing.List[MovieDto]:
        """
        returns all MovieDto for given name
        :param name: movie's name or a part of it
        :return: list of MovieDto
        """
        found_movies = []
        for title, movie_dto in self._title_to_movie_dto.items():
            if name.lower() in title.lower():
                found_movies.append(movie_dto)
        return found_movies

    def sort_by_rating(self) -> typing.Dict[str, MovieDto]:
        """Returns a sorted mapping between movie name to it's MovieDto by movie's rating"""
        return dict(sorted(self._title_to_movie_dto.items(),
                           key=lambda title_and_movie_dto: title_and_movie_dto[1].rating,
                           reverse=True))

    def get_list_of_rates(self) -> typing.List[float]:
        """:return: a list of movie ratings: float"""
        return [movie_dto.rating for movie_dto in self._title_to_movie_dto.values()]

    def get_best_movies(self) -> typing.List[str]:
        """:return: a list of movies with the max rating"""
        return [name for name, movie_dto in self._title_to_movie_dto.items()
                if movie_dto.rating == max(self.get_list_of_rates())]

    def get_worst_movies(self) -> typing.List[str]:
        """:return: a list of movies with the min rating"""
        return [name for name, movie_dto in self._title_to_movie_dto.items()
                if movie_dto.rating == min(self.get_list_of_rates())]

    def get_average_rating(self) -> float:
        """calculates an average rating of all movies"""
        return statistics.mean(self.get_list_of_rates())

    def get_median_rating(self) -> float:
        """calculates a median rating of all movies"""
        return statistics.median(self.get_list_of_rates())

    @abstractmethod
    def _flush_data(self):
        """Flush self._title_to_movie_dto to the *type* file"""
        pass

    def __str__(self):
        films = "\n".join([str(movie_dto) for movie_dto in self._title_to_movie_dto.values()])
        return f"{len(self._title_to_movie_dto)} movies in total\n{films}"
