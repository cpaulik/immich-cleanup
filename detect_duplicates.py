import os
import requests
from collections import defaultdict

def get_stacks(api_key, base_url="http://localhost:2283"):
    url = f"{base_url}/api/stacks"
    headers = {"x-api-key": f"{api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_stack(api_key, base_url, asset_ids):
    url = f"{base_url}/api/stacks"
    headers = {"x-api-key": f"{api_key}"}
    data = {"assetIds": asset_ids}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_assets(api_key, base_url="http://localhost:2283"):
    all_assets = []
    page = 1
    size = 1000
    while True:
        url = f"{base_url}/api/search/metadata"
        headers = {"x-api-key": f"{api_key}"}
        data = {"page": page, "size": size}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        resjson = response.json()
        assets = resjson["assets"]["items"]
        all_assets.extend(assets)
        print(f"Loaded {len(all_assets)} assets so far...")
        if len(assets) < size:
            break
        page += 1
    return all_assets

def main():
    api_key = os.getenv("IMMICH_API_KEY")
    base_url = os.getenv("IMMICH_BASE_URL", "http://localhost:2283")
    
    if not api_key:
        print("Error: IMMICH_API_KEY environment variable is required")
        return
    assets = get_assets(api_key, base_url)
    print(f"Found {len(assets)} assets")
    stacks = get_stacks(api_key, base_url)
    asset_to_stack = {}
    for stack in stacks:
        for asset in stack['assets']:
            asset_to_stack[asset['id']] = stack['id']
    print(f"Found {len(stacks)} stacks with {len(asset_to_stack)} assets")
    groups = defaultdict(list)
    for asset in assets:
        filename = asset.get('originalFileName', asset.get('originalPath', '').split('/')[-1])
        datetime = asset.get('localDateTime', '')
        if filename and datetime:
            key = (filename, datetime)
            groups[key].append(asset['id'])
    duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}
    # Filter groups where all duplicates are already in the same stack
    filtered_groups = {}
    for k, ids in duplicate_groups.items():
        stacks_for_group = set(asset_to_stack.get(id) for id in ids)
        if len(stacks_for_group) == 1 and list(stacks_for_group)[0] is not None:
            continue  # all in same stack
        filtered_groups[k] = ids
    duplicate_groups = filtered_groups
    if duplicate_groups:
        for (filename, dt), ids in duplicate_groups.items():
            stacks_info = [asset_to_stack.get(id, 'none') for id in ids]
            print(f"  {filename} at {dt}: {len(ids)} assets - Stacks: {stacks_info} - IDs: {ids}")
        print(f"Found {len(duplicate_groups)} duplicate groups to stack:")
        print("Creating stacks for duplicate groups...")
        for (filename, dt), ids in duplicate_groups.items():
            print(f"Creating stack for {filename} at {dt}")
            create_stack(api_key, base_url, ids)
        print("Done creating stacks")
    else:
        print("No duplicates found that need stacking")

if __name__ == "__main__":
    main()
