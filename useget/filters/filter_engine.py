"""
filter_engine.py
-----------------
Filtering logic for search results, using scene parsing and quality selection.
"""
from useget.filters.scene_parser import SceneNameParser

class FilterEngine:
	"""
	Filters search results based on quality and scene parsing.
	Chooses the best result by highest quality.
	"""
	def __init__(self, config, scene_parser):
		# config: dict with filter settings (e.g., allowed qualities)
		# scene_parser: instance of SceneNameParser
		self.config = config
		self.scene_parser = scene_parser

	def apply(self, results):
		"""
		Filter a list of search results, keeping only those matching allowed qualities.
		Returns a list with the single best result (highest quality), or empty if none match.
		"""
		filtered = []
		for item in results:
			# Parse scene info from title
			meta = self.scene_parser.parse(item['title'])
			if not meta:
				continue  # Skip if parsing fails
			# Only keep results with allowed quality
			if meta.get('quality') not in self.config.get('quality', []):
				continue
			item['meta'] = meta
			filtered.append(item)

		if not filtered:
			return []  # No matches

		# Choose the best link: prefer highest quality only
		def sort_key(item):
			meta = item['meta']
			# Prefer higher quality (e.g., 2160p > 1080p > 720p)
			return int(meta.get('quality', '0p').replace('p', ''))

		best = max(filtered, key=sort_key)
		return [best]
