import unittest
from clients.nzbgeek_client import NZBGeekClient

class TestNZBGeekClient(unittest.TestCase):
    def setUp(self):
        self.client = NZBGeekClient({'api_key': 'dummy'})

    def test_search_returns_list(self):
        # This will not hit the real API
        results = self.client.search('test')
        self.assertIsInstance(results, list)

if __name__ == "__main__":
    unittest.main()
