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
    # Step 1: Filter out 4k (2160p) results
    allowed_qualities = {'1080p', '720p'}
    filtered_results = []
    import re
    # Ask user if searching for movie or TV show
    media_type = ''
    while media_type not in ['movie', 'tv']:
        media_type = input("Is this a movie or tv show? (movie/tv): ").strip().lower()
    for item in results:
        match = re.search(r'(\d{3,4}p)', item['title'])
        quality = match.group(1) if match else ''
        if quality not in allowed_qualities:
            continue
        # Movie: look for year pattern, TV: look for SxxExx pattern
        if media_type == 'movie':
            if not re.search(r'\.(19|20)\d{2}\.', item['title']):
                continue
        elif media_type == 'tv':
            if not re.search(r'\.S\d{2}E\d{2}\.', item['title'], re.IGNORECASE):
                continue
        filtered_results.append(item)
    # Step 2: Show unique titles
    unique_titles = []
    seen = set()
    for item in filtered_results:
        if item['title'] not in seen:
            unique_titles.append(item['title'])
            seen.add(item['title'])
    for idx, title in enumerate(unique_titles):
        label = letters[idx % len(letters)]
        print(f"[{label}] {title}")
    choice = input("Select the correct title by letter: ").strip().lower()
    if choice not in letters[:len(unique_titles)]:
        print("Invalid selection.")
        return None
    selected_title = unique_titles[letters.index(choice)]
    # Step 2: Show all links for the selected title
    links = [item for item in filtered_results if item['title'] == selected_title]
    if len(links) == 1:
        return links[0]
    print(f"Multiple links found for '{selected_title}':")
    for idx, item in enumerate(links):
        label = letters[idx % len(letters)]
        print(f"  [{label}] {item['nzb_url']}")
    choice2 = input("Select the link to download by letter: ").strip().lower()
    if choice2 in letters[:len(links)]:
        return links[letters.index(choice2)]
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
