"""
scene_parser.py
---------------
Scene release title parsing for extracting show/movie metadata.
"""
import re

class SceneNameParser:
    """
    Parses scene release titles for TV and movie metadata.
    """
    def parse(self, title):
        """
        Extracts metadata from a release title string.
        Returns a dict with keys like show, season, episode, year, quality.
        """
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

        # Return empty dict if no match
        return {}
