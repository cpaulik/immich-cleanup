import os
import requests

def get_stacks(api_key, base_url="http://localhost:2283"):
    url = f"{base_url}/api/stacks"
    headers = {"x-api-key": f"{api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def delete_stack(api_key, base_url, stack_id):
    url = f"{base_url}/api/stacks/{stack_id}"
    headers = {"x-api-key": f"{api_key}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()

def main():
    api_key = os.getenv("IMMICH_API_KEY")
    base_url = os.getenv("IMMICH_BASE_URL", "http://localhost:2283")
    
    if not api_key:
        print("Error: IMMICH_API_KEY environment variable is required")
        return
    stacks = get_stacks(api_key, base_url)
    print(f"Found {len(stacks)} stacks")
    removed_count = 0
    for stack in stacks:
        assets = stack['assets']
        if len(assets) == 1:
            asset = assets[0]
            filename = asset.get('originalPath', 'N/A').split('/')[-1]
            exif = asset.get('exifInfo', {})
            timestamp = exif.get('dateTimeOriginal', 'N/A')
            w = exif.get('exifImageWidth', 'N/A')
            h = exif.get('exifImageHeight', 'N/A')
            resolution = f"{w}x{h}" if w != 'N/A' and h != 'N/A' else 'N/A'
            print(f"Stack {stack['id']} has single asset:")
            print(f"  Filename: {filename}")
            print(f"  Timestamp: {timestamp}")
            print(f"  Resolution: {resolution}")
            print(f"Removing stack {stack['id']}")
            delete_stack(api_key, base_url, stack['id'])
            removed_count += 1
    print(f"Removed {removed_count} stacks with single assets")

if __name__ == "__main__":
    main()
