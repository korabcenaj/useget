import unittest
from clients.jellyfin_client import JellyfinClient

class TestJellyfinClient(unittest.TestCase):
    def setUp(self):
        # Use real values from config.yaml
        self.client = JellyfinClient({'url': 'http://192.168.1.208:8096', 'api_key': '8749830ecac34d0e91fe09f8e47d0c9a'})

    def test_refresh_library(self):
        # This will not hit the real API
        try:
            self.client.refresh_library()
        except Exception as e:
            self.fail(f"refresh_library() raised {e}")

if __name__ == "__main__":
    unittest.main()
