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



def display_and_select(results):
    if not results:
        print("No results found.")
        return None
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for idx, item in enumerate(results):
        label = letters[idx % len(letters)]
        print(f"[{label}] {item['title']}")
    choice = input("Select a result by letter: ").strip().lower()
    if choice in letters[:len(results)]:
        return results[letters.index(choice)]
    print("Invalid selection.")
    return None

def main():
    config = load_config()
    nzbgeek = NZBGeekClient(config['nzbgeek'])
    sab = SABnzbdClient(config['sabnzbd'])
    # jellyfin = JellyfinClient(config['jellyfin'])
    scene_parser = SceneNameParser()
    filter_engine = FilterEngine(config['filters'], scene_parser)
    post_processor = PostProcessor(config['postprocess'])
    notifier = Notifier(config['notify'])

    while True:
        search = prompt_for_search()
        if not search:
            print("No search entered. Exiting.")
            break
        results = nzbgeek.search(search)
        selected = display_and_select(results)
        if selected and not sab.is_already_queued(selected):
            sab.add_nzb(selected)
            notifier.notify(f"Added NZB: {selected['title']}")
        again = input("Search for another title? (y/n): ").strip().lower()
        if again != 'y':
            break


def prompt_for_search():
    return input("Enter the title of the movie/TV show to search for: ").strip()

if __name__ == "__main__":
    main()
