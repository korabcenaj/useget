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
    filtered_results = []
    import re
    # Ask user if searching for movie or TV show
    media_type = ''
    while media_type not in ['movie', 'tv']:
        media_type = input("Is this a movie or tv show? (movie/tv): ").strip().lower()
    # Ask user for the original search text
    search_text = input("Enter the exact title (or leave blank to use previous search): ").strip()
    if not search_text:
        search_text = None
    import difflib
    for item in results:
        # No quality filter: include all
        # Movie: look for year pattern, TV: look for SxxExx pattern
        if media_type == 'movie':
            if not re.search(r'\.(19|20)\d{2}\.', item['title']):
                continue
        elif media_type == 'tv':
            if not re.search(r'\.S\d{2}E\d{2}\.', item['title'], re.IGNORECASE):
                continue
        # Strict base title match for single-word searches
        # Extract base title up to year or first dot
        import re
        base_title = item['title']
        # Remove year and everything after
        base_title = re.split(r'\.(19|20)\d{2}\.', base_title)[0]
        # Or just take up to first dot if no year
        base_title = base_title.split('.')[0]
        base_title = base_title.replace('_', ' ').replace('-', ' ').strip().lower()
        if search_text:
            if len(search_text.split()) == 1:
                # Single-word search: require exact match
                if base_title == search_text.lower():
                    filtered_results.append(item)
                continue
            else:
                # Multi-word: fallback to previous fuzzy logic
                import difflib
                ratio = difflib.SequenceMatcher(None, base_title, search_text.lower()).ratio()
                if ratio >= 0.85:
                    filtered_results.append(item)
                    continue
                if f" {search_text.lower()} " in f" {base_title} ":
                    filtered_results.append(item)
                    continue
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
        print("\n[DEBUG] Raw NZBGeek search results:")
        for item in results:
            print("  ", item['title'])
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
