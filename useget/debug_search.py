
from config.config_loader import load_config
from clients.nzbgeek_client import NZBGeekClient
from filters.scene_parser import SceneNameParser
from filters.filter_engine import FilterEngine
import logging

logging.basicConfig(level=logging.INFO)

def debug() -> None:
    """
    Debug utility to run searches and print parsed/filtered results for inspection.
    """
    config = load_config()
    nzbgeek = NZBGeekClient(config['nzbgeek'])
    scene_parser = SceneNameParser()
    filter_engine = FilterEngine(config['filters'], scene_parser)

    for search in config['searches']:
        logging.info(f"Searching for: {search}")
        results = nzbgeek.search(search)
        logging.info(f"Found {len(results)} raw results.")
        for item in results:
            title = item['title']
            meta = scene_parser.parse(title)
            logging.info(f"Title: {title}")
            logging.info(f"Parsed meta: {meta}")
            if not meta:
                logging.warning("Skipping: meta is empty (likely regex mismatch)")
                continue
            quality = meta.get('quality')
            allowed_qualities = config['filters'].get('quality', [])
            if quality not in allowed_qualities:
                logging.warning(f"Skipping: quality {quality} not in {allowed_qualities}")
                continue
            logging.info("KEEPING this result!")

if __name__ == '__main__':
    debug()
