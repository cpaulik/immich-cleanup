import os
import requests

def get_stacks(api_key, base_url="http://localhost:2283"):
    url = f"{base_url}/api/stacks"
    headers = {"x-api-key": f"{api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def update_stack_primary(api_key, base_url, stack_id, primary_asset_id):
    url = f"{base_url}/api/stacks/{stack_id}"
    headers = {"x-api-key": f"{api_key}"}
    data = {"primaryAssetId": primary_asset_id}
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    api_key = os.getenv("IMMICH_API_KEY")
    base_url = os.getenv("IMMICH_BASE_URL", "http://localhost:2283")
    
    if not api_key:
        print("Error: IMMICH_API_KEY environment variable is required")
        return
    stacks = get_stacks(api_key, base_url)
    total_assets = sum(len(stack['assets']) for stack in stacks)
    print(f"Found {len(stacks)} stacks with {total_assets} total assets")
    for stack in stacks:
        print(f"\nStack ID: {stack['id']}")
        assets = stack['assets']
        if not assets:
            print("  No assets in this stack")
            continue
        filenames = [asset.get('originalPath', 'N/A').split('/')[-1] for asset in assets]
        primary_id = stack.get('primaryAssetId')
        if primary_id:
            for i, asset in enumerate(assets):
                if asset['id'] == primary_id:
                    filenames[i] += " (P)"
                    break  # Assuming only one primary
        timestamps = [asset.get('exifInfo', {}).get('dateTimeOriginal', 'N/A') for asset in assets]
        widths = [str(asset.get('exifInfo', {}).get('exifImageWidth', 'N/A')) for asset in assets]
        heights = [str(asset.get('exifInfo', {}).get('exifImageHeight', 'N/A')) for asset in assets]
        resolutions = [f"{w}x{h}" if w != 'N/A' and h != 'N/A' else 'N/A' for w, h in zip(widths, heights)]
        print("Filenames:  " + " | ".join(filenames))
        print("Timestamps: " + " | ".join(timestamps))
        print("Resolutions: " + " | ".join(resolutions))
        # Update primary to lowest resolution if needed (skip if only one asset)
        if len(assets) > 1:
            valid_assets = []
            for asset in assets:
                exif = asset.get('exifInfo', {})
                w = exif.get('exifImageWidth')
                h = exif.get('exifImageHeight')
                if w is not None and h is not None:
                    area = w * h
                    valid_assets.append((asset['id'], area))
            if valid_assets:
                min_asset_id = min(valid_assets, key=lambda x: x[1])[0]
                current_primary = stack.get('primaryAssetId')
                if min_asset_id != current_primary:
                    print(f"Updating stack {stack['id']} primary to asset with lower resolution: {min_asset_id}")
                    update_stack_primary(api_key, base_url, stack['id'], min_asset_id)


if __name__ == "__main__":
    main()
