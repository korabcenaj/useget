import sys
import argparse
from useget.gui import main as gui_main
from useget.cli import main as cli_main

def main():
    parser = argparse.ArgumentParser(description="useget: Usenet automation tool")
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode (headless)')
    args = parser.parse_args()

    if args.cli:
        cli_main()
    else:
        gui_main()

if __name__ == "__main__":
    main()
