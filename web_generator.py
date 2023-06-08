import typing

from db.movie_dto import MovieDto

YOUTUBE_TRAILER_URL = "https://www.youtube.com/embed/"
TEMPLATE_HTML = "MoviesDB/_static/index_template.html"
DIV_HTML = '<div class="slider-container">'
FRAME_HTML = '<div class="container">\n\
<iframe \
src="https://www.pngitem.com/pimgs/m/387-3870252_background-filmstrip-transparent-film-tape-png-png-download.png" \
width="720" height="380" name="trailer"></iframe></div></body>'
NEW_HTML = "MoviesDB/_static/index.html"


class WebGenerator:
    """creates a new html file with movie app info"""
    @staticmethod
    def get_html_content(title_to_movie_dto: typing.Dict[str, MovieDto]):
        """Generate a string with the movie's data, converting a data into HTML format"""
        content = ""
        for movie_dto in title_to_movie_dto.values():
            note = movie_dto.note
            content += f'<li>\n\
                <div class="movie slider">\n\
                <a href="{YOUTUBE_TRAILER_URL}{movie_dto.trailer_id}" target="trailer">\n\
                <img class="movie-poster" src="{movie_dto.poster}" {"title=" + chr(34) + note + chr(34) if note else chr(0)}">\n\
                </a>\n<div class="movie-title slider">{movie_dto.name}</div>\n\
                <div class="movie-year">{movie_dto.year}</div>\n\
                </div>\n\
                </li>\n'
        return content

    @staticmethod
    def fill_template_html(content):
        """writing a new html file with our html template and the given content"""
        with open(TEMPLATE_HTML, "r", encoding="utf-8") as template:
            template_content = template.read()

        template_content = template_content.replace("__TEMPLATE_TITLE__", "Movie Trailer Base")
        edited_html = template_content.replace("__TEMPLATE_MOVIE_GRID__", content)
        edited_html = edited_html.replace("<div>", DIV_HTML)
        new_html = edited_html.replace("</body>", FRAME_HTML)

        with open(NEW_HTML, "w", encoding="utf-8") as file:
            file.write(new_html)
