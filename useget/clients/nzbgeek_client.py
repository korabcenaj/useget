"""
nzbgeek_client.py
-----------------
Client for searching NZB files via the NZBGeek API.
"""
import requests
import xml.etree.ElementTree as ET

class NZBGeekClient:
	"""
	Client for NZBGeek API to search for NZB files.
	"""
	def __init__(self, config):
		# config: dict with 'api_key' and optional 'username'
		self.api_key = config['api_key']
		self.username = config.get('username')
		self.base_url = 'https://api.nzbgeek.info'

	def search(self, query):
		"""
		Search NZBGeek for a query string.
		Returns a list of dicts with 'title' and 'nzb_url'.
		"""
		url = f"{self.base_url}/api"
		params = {
			't': 'search',
			'apikey': self.api_key,
			'q': query,
			'o': 'xml'
		}
		response = requests.get(url, params=params)
		if response.status_code != 200:
			return []
		root = ET.fromstring(response.content)
		results = []
		for item in root.findall('.//item'):
			# Extract title and NZB URL from XML
			title = item.find('title').text if item.find('title') is not None else ''
			nzb_url = item.find('link').text if item.find('link') is not None else ''
			results.append({'title': title, 'nzb_url': nzb_url})
		return results
