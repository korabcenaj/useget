import unittest
from clients.sabnzbd_client import SABnzbdClient
from clients.test_sabnzbd_history import example_history
from notify.notifier import Notifier
from postprocess.post_processor import PostProcessor

class DummyNotifier:
    def notify(self, message):
        print(message)

class DummyPostProcessor:
    def process(self, file_path):
        print(f"Processed: {file_path}")

class TestSABnzbdClient(unittest.TestCase):
    def setUp(self):
        self.client = SABnzbdClient({'url': 'http://localhost', 'api_key': 'dummy', 'test_mode': True})
        self.notifier = DummyNotifier()
        self.post_processor = DummyPostProcessor()

    def test_monitor_downloads(self):
        self.client.monitor_downloads(self.post_processor, self.notifier)
        for slot in example_history:
            self.assertTrue(slot['post_processed'])

if __name__ == "__main__":
    unittest.main()
