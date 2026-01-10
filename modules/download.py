# modules/download.py

import os
import requests
import hashlib
from modules import db_manager

def download_file(url, destination):
    """Downloads a file from a URL to a destination."""
    try:
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

def verify_checksum(file_path, checksum):
    """Verifies the checksum of a downloaded file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest() == checksum

def download_component(model, component, type):
    """Downloads a specific component for a given model."""
    # Get the URL from the database
    url_info = db_manager.get_url(model, component, type)
    if not url_info:
        print(f"No URL found for {component} {type} for model {model}")
        return

    url = url_info['url']
    checksum = url_info.get('checksum')
    
    # TODO: Determine a proper destination path
    destination = f"downloads/{model}/{component}_{type}"

    if download_file(url, destination):
        if checksum and not verify_checksum(destination, checksum):
            print("Checksum verification failed!")
        else:
            print(f"Successfully downloaded {component} {type} for {model}")
