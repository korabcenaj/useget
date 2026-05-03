
# useget

A modular Python application for searching, downloading, and post-processing media using NZB, SABnzbd, and Jellyfin integrations.

## Project Structure

- `useget/` - Main package (all core code and tests are here)
- `main.py` - Entry point for the application
- `requirements.txt` - Python dependencies
- `.github/` - GitHub workflows and Copilot instructions
- `.vscode/` - VS Code tasks and settings

## Setup

1. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

2. Run the app:

   ```sh
   python main.py
   ```

## Development

- All source code and tests are inside the `useget/` package.
- Configuration is handled via the GUI and stored persistently (no config files required).
- Branch flow uses `main` for production, `dev` for feature integration, `staging` for pre-release validation, and `release/*` for release stabilization.

## Testing

Run all tests:

```sh
python -m unittest discover -s useget -p 'test_*.py'
```

## Contributing

- Follow PEP8 and best practices.
- Use clear commit messages.
- Add/modify tests for all features and bugfixes.
