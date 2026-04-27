import requests

class JellyfinClient:
    def __init__(self, config):
        self.url = config['url']
        self.api_key = config['api_key']

    def refresh_library(self):
        headers = {'X-Emby-Token': self.api_key}
        # This endpoint may need to be adjusted for your Jellyfin version
        requests.post(f"{self.url}/Library/Refresh", headers=headers)
