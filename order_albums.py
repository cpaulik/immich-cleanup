import os
import requests

def get_albums(api_key, base_url="http://localhost:2283"):
    url = f"{base_url}/api/albums"
    headers = {"x-api-key": f"{api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def order_album(api_key, base_url, album_id, album_name):
    url = f"{base_url}/api/albums/{album_id}"
    headers = {"x-api-key": f"{api_key}"}
    data = {"order": "asc"}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    print(f"Ordered album '{album_name}' oldest first")

def main():
    api_key = os.getenv("IMMICH_API_KEY")
    base_url = os.getenv("IMMICH_BASE_URL", "http://localhost:2283")
    
    if not api_key:
        print("Error: IMMICH_API_KEY environment variable is required")
        return
    albums = get_albums(api_key, base_url)
    print(f"Found {len(albums)} albums")
    for album in albums:
        album_id = album['id']
        album_name = album.get('albumName', album.get('name', 'Unknown'))
        order_album(api_key, base_url, album_id, album_name)
    print("All albums ordered oldest first")

if __name__ == "__main__":
    main()