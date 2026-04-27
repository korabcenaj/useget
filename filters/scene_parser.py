import re

class SceneNameParser:
    def parse(self, title):
        # Try TV pattern first: Show.Name.S01E01.1080p
        tv_pattern = r"(?P<show>.+?)\.S(?P<season>\d{2})E(?P<episode>\d{2})\.(?P<quality>\d{3,4}p)"
        match = re.search(tv_pattern, title, re.IGNORECASE)
        if match:
            return match.groupdict()

        # Try movie pattern: Movie.Name.2022.1080p
        movie_pattern = r"(?P<show>.+?)\.(?P<year>\d{4})\.(?P<quality>\d{3,4}p)"
        match = re.search(movie_pattern, title, re.IGNORECASE)
        if match:
            return match.groupdict()

        return {}
