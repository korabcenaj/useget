# CLI entrypoint for useget
from config.config_loader import load_config
from useget.clients.nzbgeek_client import NZBGeekClient
from useget.clients.sabnzbd_client import SABnzbdClient
from useget.clients.jellyfin_client import JellyfinClient
from useget.filters.scene_parser import SceneNameParser
from useget.filters.filter_engine import FilterEngine
from useget.postprocess.post_processor import PostProcessor
from useget.notify.notifier import Notifier
import os
import logging
import os
import logging

try:
    import readchar
except ImportError:
    readchar = None

logging.basicConfig(level=logging.INFO)

from typing import List, Dict, Any, Optional

def display_and_select(results: List[Dict[str, Any]], auto: bool = False) -> Optional[Dict[str, Any]]:
    """
    Display search results and allow user to select one interactively.
    Args:
        results: List of search result dicts.
        auto: If True, auto-select the first result.
    Returns:
        The selected result dict, or None if no results.
    """
    if not results:
        print("No results found. Please refine your search criteria and try again.")
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
    logging.info("\nSelect a result using arrow keys and press Enter:")
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
                print("Invalid selection. Please enter a valid number or letter.")
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
                print("Invalid selection. Please enter a valid number or letter.")
                continue
        key = readchar.readkey()
        if key in (readchar.key.UP, 'k'):
            idx2 = (idx2 - 1) % len(links)
        elif key in (readchar.key.DOWN, 'j'):
            idx2 = (idx2 + 1) % len(links)
        elif key == readchar.key.ENTER or key == '\r' or key == '\n':
            break
    return links[idx2]

def cli_search(
    config: dict,
    nzbgeek: Any,
    sab: Any,
    filter_engine: Any,
    post_processor: Any,
    notifier: Any,
    args: Any
) -> None:
    """
    Run CLI search workflow using provided config and clients.
    Args:
        config: Configuration dictionary.
        nzbgeek: NZBGeekClient instance.
        sab: SABnzbdClient instance.
        filter_engine: FilterEngine instance.
        post_processor: PostProcessor instance.
        notifier: Notifier instance.
        args: Parsed CLI arguments.
    """
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
    parser = argparse.ArgumentParser(description="useget CLI: NZB search, download, and automation tool.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommand to run")

    # Search subcommand
    search_parser = subparsers.add_parser("search", help="Search for NZBs")
    search_parser.add_argument("query", nargs="*", help="Search query terms")
    search_parser.add_argument("--auto", action="store_true", help="Auto-select first result")

    # Download subcommand
    download_parser = subparsers.add_parser("download", help="Download NZB by title")
    download_parser.add_argument("title", help="Title of NZB to download")

    # Monitor subcommand
    monitor_parser = subparsers.add_parser("monitor", help="Monitor downloads and post-process")

    # Version
    parser.add_argument('--version', action='version', version='useget CLI version 0.1.0')

    args = parser.parse_args()

    config = load_config()
    nzbgeek = NZBGeekClient(config['nzbgeek'])
    sab = SABnzbdClient(config['sabnzbd'])
    filter_engine = FilterEngine(config['filters'], SceneNameParser())
    post_processor = PostProcessor(config.get('postprocess', {}))
    notifier = Notifier(config.get('notify', {}))

    if args.command == "search":
        query = " ".join(args.query) if args.query else None
        if not query:
            print("Please provide a search query.")
            return
        results = nzbgeek.search(query)
        filtered = filter_engine.apply(results)
        selected = display_and_select(filtered, auto=args.auto)
        if selected:
            print(f"Selected: {selected['title']}")
    elif args.command == "download":
        # Download by title
        results = nzbgeek.search(args.title)
        filtered = filter_engine.apply(results)
        selected = display_and_select(filtered, auto=True)
        if selected:
            sab.add_nzb(selected)
            print(f"Sent '{selected['title']}' to SABnzbd.")
        else:
            print("No matching NZB found.")
    elif args.command == "monitor":
        sab.monitor_downloads(post_processor, notifier)
        print("Monitoring downloads...")
