import unittest
from useget.postprocess.post_processor import PostProcessor

class TestPostProcessor(unittest.TestCase):
	def setUp(self):
		self.processor = PostProcessor({'fix_permissions': False})

	def test_process(self):
		try:
			self.processor.process('/tmp/testfile')
		except Exception as e:
			self.fail(f"process() raised {e}")

if __name__ == "__main__":
	unittest.main()
