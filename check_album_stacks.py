import os
import requests
from collections import defaultdict

def get_stacks(api_key, base_url="http://localhost:2283"):
    url = f"{base_url}/api/stacks"
    headers = {"x-api-key": f"{api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_albums(api_key, base_url="http://localhost:2283"):
    url = f"{base_url}/api/albums"
    headers = {"x-api-key": f"{api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_album_assets(api_key, base_url, album_id):
    url = f"{base_url}/api/albums/{album_id}"
    headers = {"x-api-key": f"{api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['assets']

def remove_assets_from_album(api_key, base_url, album_id, asset_ids):
    url = f"{base_url}/api/albums/{album_id}/assets"
    headers = {"x-api-key": f"{api_key}"}
    data = {"ids": asset_ids}
    response = requests.delete(url, headers=headers, json=data)
    response.raise_for_status()

def main():
    api_key = os.getenv("IMMICH_API_KEY")
    base_url = os.getenv("IMMICH_BASE_URL", "http://localhost:2283")
    
    if not api_key:
        print("Error: IMMICH_API_KEY environment variable is required")
        return
    stacks = get_stacks(api_key, base_url)
    asset_to_stack = {}
    stack_to_primary = {}
    for stack in stacks:
        stack_to_primary[stack['id']] = stack.get('primaryAssetId')
        for asset in stack['assets']:
            asset_to_stack[asset['id']] = stack['id']
    print(f"Found {len(stacks)} stacks")
    albums = get_albums(api_key, base_url)
    print(f"Found {len(albums)} albums")
    found_issues = False
    for album in albums:
        album_id = album['id']
        album_name = album['albumName']
        assets = get_album_assets(api_key, base_url, album_id)
        stack_counts = defaultdict(list)
        for asset in assets:
            stack_id = asset_to_stack.get(asset['id'])
            if stack_id:
                stack_counts[stack_id].append(asset)
        issues = [(stack_id, stack_assets) for stack_id, stack_assets in stack_counts.items() if len(stack_assets) > 1]
        if issues:
            found_issues = True
            print(f"Album: {album_name}")
            for stack_id, stack_assets in issues:
                print(f"  Stack {stack_id} has {len(stack_assets)} assets:")
                for asset in stack_assets:
                    filename = asset.get('originalPath', '').split('/')[-1]
                    date = asset.get('exifInfo', {}).get('dateTimeOriginal', 'N/A')
                    print(f"    {filename} - {date}")
                primary_id = stack_to_primary.get(stack_id)
                if primary_id:
                    assets_to_remove = [a['id'] for a in stack_assets if a['id'] != primary_id]
                    if assets_to_remove:
                        print(f"  Removing {len(assets_to_remove)} non-primary assets from stack {stack_id}")
                        remove_assets_from_album(api_key, base_url, album_id, assets_to_remove)
    if not found_issues:
        print("No albums found with multiple assets from the same stack")

if __name__ == "__main__":
    main()
