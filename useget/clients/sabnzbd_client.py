"""
sabnzbd_client.py
-----------------
Client for interacting with SABnzbd for NZB queueing and monitoring.
"""
import requests
import time
from useget.clients.test_sabnzbd_history import example_history

class SABnzbdClient:
	"""
	Client for interacting with SABnzbd for NZB downloads and monitoring.
	"""
	def __init__(self, config):
		# config: dict with 'url', 'api_key', and optional 'test_mode'
		self.url = config['url']
		self.api_key = config['api_key']
		self.test_mode = config.get('test_mode', False)

	def add_nzb(self, nzb):
		"""
		Add an NZB to SABnzbd queue. In test mode, just print.
		"""
		if self.test_mode:
			print(f"[TEST MODE] Would add NZB: {nzb['title']}")
			return
		files = {'nzbfile': requests.get(nzb['nzb_url']).content}
		params = {
			'apikey': self.api_key,
			'mode': 'addurl',
			'name': nzb['nzb_url'],
			'output': 'json'
		}
		requests.post(f"{self.url}/api", params=params, files=files)

	def is_already_queued(self, nzb):
		"""
		Check if an NZB is already in the SABnzbd queue.
		"""
		if self.test_mode:
			return False
		params = {
			'apikey': self.api_key,
			'mode': 'queue',
			'output': 'json'
		}
		resp = requests.get(f"{self.url}/api", params=params)
		if resp.status_code != 200:
			return False
		queue = resp.json().get('queue', {}).get('slots', [])
		return any(nzb['title'] in slot.get('filename', '') for slot in queue)

	def monitor_downloads(self, post_processor, notifier):
		"""
		Monitor SABnzbd history for completed downloads and trigger post-processing.
		In test mode, uses example_history.
		"""
		if self.test_mode:
			history = example_history
			for slot in history:
				if slot.get('status') == 'Completed' and not slot.get('post_processed'):
					post_processor.process(slot['filename'])
					notifier.notify(f"[TEST MODE] Post-processed: {slot['filename']}")
					slot['post_processed'] = True
			return
		params = {
			'apikey': self.api_key,
			'mode': 'history',
			'output': 'json'
		}
		while True:
			resp = requests.get(f"{self.url}/api", params=params)
			if resp.status_code != 200:
				time.sleep(30)
				continue
			history = resp.json().get('history', {}).get('slots', [])
			for slot in history:
				if slot.get('status') == 'Completed' and not slot.get('post_processed'):
					post_processor.process(slot.get('name', slot.get('filename')))
