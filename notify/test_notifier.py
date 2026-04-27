import unittest
from notify.notifier import Notifier

class TestNotifier(unittest.TestCase):
    def setUp(self):
        self.notifier = Notifier({'discord_webhook': None, 'email': None})

    def test_notify(self):
        try:
            self.notifier.notify("Test message")
        except Exception as e:
            self.fail(f"notify() raised {e}")

if __name__ == "__main__":
    unittest.main()
