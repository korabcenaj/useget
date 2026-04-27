from config.config_loader import load_config
from clients.nzbgeek_client import NZBGeekClient
from filters.scene_parser import SceneNameParser
from filters.filter_engine import FilterEngine

def debug():
    config = load_config()
    nzbgeek = NZBGeekClient(config['nzbgeek'])
    scene_parser = SceneNameParser()
    filter_engine = FilterEngine(config['filters'], scene_parser)

    for search in config['searches']:
        print(f"Searching for: {search}")
        results = nzbgeek.search(search)
        print(f"Found {len(results)} raw results.")
        for item in results:
            title = item['title']
            meta = scene_parser.parse(title)
            print(f"Title: {title}")
            print(f"Parsed meta: {meta}")
            if not meta:
                print("Skipping: meta is empty (likely regex mismatch)")
                continue
            quality = meta.get('quality')
            allowed_qualities = config['filters'].get('quality', [])
            if quality not in allowed_qualities:
                print(f"Skipping: quality {quality} not in {allowed_qualities}")
                continue
            print("KEEPING this result!")

if __name__ == '__main__':
    debug()
