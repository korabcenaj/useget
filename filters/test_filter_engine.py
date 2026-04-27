import unittest
from filters.filter_engine import FilterEngine
from filters.scene_parser import SceneNameParser

class TestFilterEngine(unittest.TestCase):
    def setUp(self):
        config = {'quality': ['1080p']}
        self.engine = FilterEngine(config, SceneNameParser())

    def test_apply(self):
        results = [{'title': 'Show.Name.S01E01.1080p.WEB-DL.DD5.1.H.264-TEST'}]
        filtered = self.engine.apply(results)
        self.assertEqual(len(filtered), 1)

if __name__ == "__main__":
    unittest.main()
