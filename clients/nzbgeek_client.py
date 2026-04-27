import requests
import xml.etree.ElementTree as ET

class NZBGeekClient:
    def __init__(self, config):
        self.api_key = config['api_key']
        self.username = config.get('username')
        self.base_url = 'https://api.nzbgeek.info'

    def search(self, query):
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
            title = item.find('title').text if item.find('title') is not None else ''
            nzb_url = item.find('link').text if item.find('link') is not None else ''
            results.append({'title': title, 'nzb_url': nzb_url})
        return results
