"""
jellyfin_client.py
------------------
Client for interacting with Jellyfin server (e.g., library refresh).
"""
import requests

class JellyfinClient:
	"""
	Client for interacting with Jellyfin server (e.g., to refresh library).
	"""
	def __init__(self, config):
		# config: dict with 'url' and 'api_key'
		self.url = config['url']
		self.api_key = config['api_key']

	def refresh_library(self):
		"""
		Trigger a library refresh in Jellyfin.
		"""
		headers = {'X-Emby-Token': self.api_key}
		# This endpoint may need to be adjusted for your Jellyfin version
		requests.post(f"{self.url}/Library/Refresh", headers=headers)
