# Main entry point for useget
from config.config_loader import load_config
from clients.nzbgeek_client import NZBGeekClient
from clients.sabnzbd_client import SABnzbdClient
from clients.jellyfin_client import JellyfinClient
from filters.scene_parser import SceneNameParser
from filters.filter_engine import FilterEngine
from postprocess.post_processor import PostProcessor
from notify.notifier import Notifier
import time


def main():
    config = load_config()
    nzbgeek = NZBGeekClient(config['nzbgeek'])
    sab = SABnzbdClient(config['sabnzbd'])
  #  jellyfin = JellyfinClient(config['jellyfin'])
    scene_parser = SceneNameParser()
    filter_engine = FilterEngine(config['filters'], scene_parser)
    post_processor = PostProcessor(config['postprocess'])
    notifier = Notifier(config['notify'])

    # Example workflow loop
    while True:
        for search in config['searches']:
            results = nzbgeek.search(search)
            filtered = filter_engine.apply(results)
            for nzb in filtered:
                if not sab.is_already_queued(nzb):
                    sab.add_nzb(nzb)
                    notifier.notify(f"Added NZB: {nzb['title']}")
        sab.monitor_downloads(post_processor, notifier)
#        jellyfin.refresh_library()
        time.sleep(config.get('interval', 3600))

if __name__ == "__main__":
    main()
