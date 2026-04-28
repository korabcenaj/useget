# CLI entrypoint for useget
from config.config_loader import load_config
from useget.clients.nzbgeek_client import NZBGeekClient
from useget.clients.sabnzbd_client import SABnzbdClient
from useget.clients.jellyfin_client import JellyfinClient
from useget.filters.scene_parser import SceneNameParser
from useget.filters.filter_engine import FilterEngine
from useget.postprocess.post_processor import PostProcessor
from useget.notify.notifier import Notifier
import sys
import time
import argparse
import os
try:
    import readchar
except ImportError:
    readchar = None

def display_and_select(results, auto=False):
    if not results:
        print("No results found.")
        return None
    letters = 'abcdefghijklmnopqrstuvwxyz'
    filtered_results = results
    unique_titles = []
    seen = set()
    for item in filtered_results:
        if item['title'] not in seen:
            unique_titles.append(item['title'])
            seen.add(item['title'])
    if auto:
        selected_title = unique_titles[0]
        links = [item for item in filtered_results if item['title'] == selected_title]
        return links[0]
    print("\nSelect a result using arrow keys and press Enter:")
    idx = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Results:")
        for i, title in enumerate(unique_titles):
            prefix = '>' if i == idx else ' '
            print(f"{prefix} {title}")
        print("\nUse Up/Down arrows and Enter to select.")
        if not readchar:
            print("(Install 'readchar' for keyboard navigation: pip install readchar)")
            choice = input("Type the number or letter of your choice: ").strip().lower()
            if choice.isdigit() and 0 <= int(choice) < len(unique_titles):
                idx = int(choice)
                break
            elif choice in letters[:len(unique_titles)]:
                idx = letters.index(choice)
                break
            else:
                print("Invalid selection.")
                continue
        key = readchar.readkey()
        if key in (readchar.key.UP, 'k'):
            idx = (idx - 1) % len(unique_titles)
        elif key in (readchar.key.DOWN, 'j'):
            idx = (idx + 1) % len(unique_titles)
        elif key == readchar.key.ENTER or key == '\r' or key == '\n':
            break
    selected_title = unique_titles[idx]
    links = [item for item in filtered_results if item['title'] == selected_title]
    if len(links) == 1:
        return links[0]
    # Link selection
    idx2 = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Links for '{selected_title}':")
        for i, item in enumerate(links):
            prefix = '>' if i == idx2 else ' '
            print(f"{prefix} {item['nzb_url']}")
        print("\nUse Up/Down arrows and Enter to select.")
        if not readchar:
            choice2 = input("Type the number or letter of your choice: ").strip().lower()
            if choice2.isdigit() and 0 <= int(choice2) < len(links):
                idx2 = int(choice2)
                break
            elif choice2 in letters[:len(links)]:
                idx2 = letters.index(choice2)
                break
            else:
                print("Invalid selection.")
                continue
        key = readchar.readkey()
        if key in (readchar.key.UP, 'k'):
            idx2 = (idx2 - 1) % len(links)
        elif key in (readchar.key.DOWN, 'j'):
            idx2 = (idx2 + 1) % len(links)
        elif key == readchar.key.ENTER or key == '\r' or key == '\n':
            break
    return links[idx2]

def cli_search(config, nzbgeek, sab, filter_engine, post_processor, notifier, args):
    for search in config['searches']:
        print(f"Searching for: {search}")
        results = nzbgeek.search(search)
        print(f"Found {len(results)} raw results.")
        filtered = filter_engine.filter(results)
        print(f"Filtered to {len(filtered)} results.")
        selected = display_and_select(filtered, auto=args.auto)
        if selected:
            print(f"Sending to SABnzbd: {selected['title']}")
            sab.add_nzb(selected)
            print("Waiting for download to complete...")
            if args.postprocess:
                print("Post-processing...")
                post_processor.process(selected['title'])
            if args.notify:
                notifier.notify(f"Downloaded: {selected['title']}")
        else:
            print("No selection made.")

def list_searches(config):
    print("Configured searches:")
    for s in config['searches']:
        print(f"- {s}")

def main():
    parser = argparse.ArgumentParser(description="useget CLI: Usenet automation tool")
    parser.add_argument('--search', nargs='+', help='Override search terms (space separated)')
    parser.add_argument('--auto', action='store_true', help='Run in non-interactive mode (auto-select first result)')
    parser.add_argument('--list', action='store_true', help='List configured searches and exit')
    parser.add_argument('--postprocess', action='store_true', help='Run post-processing after download')
    parser.add_argument('--notify', action='store_true', help='Send notification after download')
    parser.add_argument('--version', action='store_true', help='Show version and exit')
    args = parser.parse_args()

    if args.version:
        print("useget CLI version 0.1.0")
        sys.exit(0)

    config = load_config()
    if args.search:
        config['searches'] = args.search
    if args.list:
        list_searches(config)
        sys.exit(0)
    nzbgeek = NZBGeekClient(config['nzbgeek'])
    sab = SABnzbdClient(config['sabnzbd'])
    scene_parser = SceneNameParser()
    filter_engine = FilterEngine(config['filters'], scene_parser)
    post_processor = PostProcessor(config.get('postprocess', {}))
    notifier = Notifier(config.get('notify', {}))
    cli_search(config, nzbgeek, sab, filter_engine, post_processor, notifier, args)
