# useget

A full-featured Python Usenet automation app that searches NZBGeek, filters results with smart scene name parsing, sends NZBs to SABnzbd, monitors downloads, post-processes files, triggers Jellyfin scans, and sends notifications.

## Features
- NZBGeek search and filtering
- Smart scene name parsing
- SABnzbd integration
- Download monitoring
- Post-processing and permission fixing
- Jellyfin library refresh
- Notification system
- Modular, extensible architecture

## Getting Started
1. Clone the repository or copy the files to your workspace.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your settings in `config.yaml`.
4. Run the main script: `python main.py`

## Configuration
Edit `config/config.yaml` with your real API keys, URLs, and preferences. Example:

```yaml
nzbgeek:
	api_key: "YOUR_NZBGEEK_API_KEY"
	username: "YOUR_NZBGEEK_USERNAME"
sabnzbd:
	url: "http://YOUR_SABNZBD_HOST:PORT"
	api_key: "YOUR_SABNZBD_API_KEY"
jellyfin:
	url: "http://YOUR_JELLYFIN_HOST:PORT"
	api_key: "YOUR_JELLYFIN_API_KEY"
filters:
	quality: ["1080p", "720p"]
	min_size_mb: 200
	max_size_mb: 10000
postprocess:
	fix_permissions: true
	target_uid: 1000
	target_gid: 1000
notify:
	email: null
	discord_webhook: null
searches:
	- "Example Show S01E01"
interval: 3600
```

## How It Works
1. The app loads your configuration from `config.yaml`.
2. For each search term in `searches`, it queries NZBGeek for matching releases.
3. Results are filtered by quality and scene name using the filter engine.
4. New NZBs are sent to SABnzbd for downloading.
5. Downloads are monitored; after completion, post-processing (e.g., permission fixing) is applied.
6. Jellyfin library is refreshed to pick up new media.
7. Notifications are sent via Discord, email, or printed to console.
8. The process repeats every `interval` seconds (default: 3600).

## Extending
- Add new filters in `filters/filter_engine.py`.
- Customize post-processing in `postprocess/post_processor.py`.
- Add notification methods in `notify/notifier.py`.

## Requirements
* Python 3.7+
* See `requirements.txt` for dependencies: requests, PyYAML, apscheduler

## Troubleshooting
- Ensure all API keys and URLs are correct in your config.
- Add `__init__.py` files to all folders if tests are not discovered.
- Run tests with: `python3 -m unittest discover -s . -p 'test_*.py'`

## Project Structure
- `main.py` — Entry point and scheduler
- `config/` — Configuration files
- `clients/` — API clients (NZBGeek, SABnzbd, Jellyfin)
- `filters/` — Filtering and scene name parsing
- `postprocess/` — Post-processing logic
- `notify/` — Notification system
- `utils/` — Utilities and helpers

## License
MIT
