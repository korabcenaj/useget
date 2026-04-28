import unittest
from useget.filters.scene_parser import SceneNameParser

class TestSceneNameParser(unittest.TestCase):
    def setUp(self):
        self.parser = SceneNameParser()

    def test_parse(self):
        title = "Show.Name.S01E01.1080p.WEB-DL.DD5.1.H.264-TEST"
        meta = self.parser.parse(title)
        self.assertIn('show', meta)
        self.assertIn('season', meta)
        self.assertIn('episode', meta)
        self.assertIn('quality', meta)

if __name__ == "__main__":
    unittest.main()
