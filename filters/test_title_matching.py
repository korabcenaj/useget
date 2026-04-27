import unittest
from filters.filter_engine import FilterEngine
from filters.scene_parser import SceneNameParser

class TestTitleMatching(unittest.TestCase):
    def setUp(self):
        self.config = {'quality': ['1080p', '720p']}
        self.scene_parser = SceneNameParser()
        self.engine = FilterEngine(self.config, self.scene_parser)
        self.sample_results = [
            {'title': 'Stalker.1979.1080p.BluRay.x264', 'nzb_url': 'url1'},
            {'title': 'Deathstalker.1983.1080p.BluRay.x264', 'nzb_url': 'url2'},
            {'title': 'Sleepstalker.1995.1080p.WEBRip.x264', 'nzb_url': 'url3'},
            {'title': 'Stalker.1979.720p.BluRay.x264', 'nzb_url': 'url4'},
            {'title': 'Stalkers.2025.1080p.WEBRip.x264', 'nzb_url': 'url5'},
        ]

    def test_single_word_exact(self):
        # Simulate display_and_select logic for single-word search 'stalker'
        search_text = 'stalker'
        filtered = []
        for item in self.sample_results:
            import re
            match = re.search(r'(\d{3,4}p)', item['title'])
            quality = match.group(1) if match else ''
            if quality not in self.config['quality']:
                continue
            base_title = item['title']
            base_title = re.split(r'\.(19|20)\d{2}\.', base_title)[0]
            base_title = base_title.split('.')[0]
            base_title = base_title.replace('_', ' ').replace('-', ' ').strip().lower()
            if base_title == search_text.lower():
                filtered.append(item)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(any('url1' in x['nzb_url'] for x in filtered))
        self.assertTrue(any('url4' in x['nzb_url'] for x in filtered))
        self.assertFalse(any('url2' in x['nzb_url'] for x in filtered))
        self.assertFalse(any('url3' in x['nzb_url'] for x in filtered))
        self.assertFalse(any('url5' in x['nzb_url'] for x in filtered))

if __name__ == '__main__':
    unittest.main()
