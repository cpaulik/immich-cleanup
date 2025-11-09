# Immich Stacks Cleanup

A Python toolkit for managing and cleaning up photo stacks in Immich, a self-hosted photo and video backup solution. This repository contains utilities to automate common stack management tasks.

## Features

- **Stack Management**: Automatically set primary assets in stacks based on resolution
- **Duplicate Detection**: Find and stack duplicate photos based on filename and timestamp
- **Album Cleanup**: Remove duplicate stack assets from albums
- **Single Asset Cleanup**: Remove stacks that contain only a single asset
- **Album Ordering**: Sort all albums by date (oldest first)

## Scripts

### `main.py`

Analyzes and updates stack primary assets to use the lowest resolution image as primary, which is optimal for storage efficiency.

### `detect_duplicates.py`

Scans all assets to find duplicates (same filename + timestamp) and automatically creates stacks for them.

### `check_album_stacks.py`

Identifies albums containing multiple assets from the same stack and removes non-primary assets to clean up album views.

### `remove_single_asset_stacks.py`

Finds and removes stacks that contain only one asset, effectively unstacking them.

### `order_albums.py`

Sets all albums to display in chronological order (oldest first).

## Setup

1. Clone this repository
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Set up environment variables

## Configuration

Set the following environment variables:

```bash
export IMMICH_API_KEY="your_immich_api_key"
export IMMICH_BASE_URL="http://your-immich-server:2283"  # Optional, defaults to localhost:2283
```

To get an API key:

1. Log into your Immich web interface
2. Go to Administration → API Keys
3. Create a new key with appropriate permissions

For convenience, you can add these to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) or create a `.env` file:

```bash
# .env file
IMMICH_API_KEY="your_immich_api_key"
IMMICH_BASE_URL="http://your-immich-server:2283"
```

## Usage

Run each script individually:

```bash
uv run main.py
uv run detect_duplicates.py
uv run check_album_stacks.py
uv run remove_single_asset_stacks.py
uv run order_albums.py
```

## Safety

- Scripts include print statements to show what actions will be taken
- Always backup your Immich database before running cleanup operations

## Dependencies

- Python 3.12+
- `requests` library

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project is not affiliated with Immich. Use at your own risk.

