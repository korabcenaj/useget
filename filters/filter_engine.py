from useget.filters.scene_parser import SceneNameParser

class FilterEngine:
    def __init__(self, config, scene_parser):
        self.config = config
        self.scene_parser = scene_parser

    def apply(self, results):
        # Filter by quality
        filtered = []
        for item in results:
            meta = self.scene_parser.parse(item['title'])
            if not meta:
                continue
            if meta.get('quality') not in self.config.get('quality', []):
                continue
            item['meta'] = meta
            filtered.append(item)

        if not filtered:
            return []

        # Choose the best link: prefer highest quality only
        def sort_key(item):
            meta = item['meta']
            # Prefer higher quality (e.g., 2160p > 1080p > 720p)
            return int(meta.get('quality', '0p').replace('p', ''))

        best = max(filtered, key=sort_key)
        return [best]
