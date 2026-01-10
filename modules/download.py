# modules/download.py

import os
import requests
import hashlib
from modules import db_manager
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

def download_file(url, destination):
    """Downloads a file from a URL to a destination with a progress bar."""
    try:
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            
            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f"Downloading {os.path.basename(destination)}", total=total_size)
                
                with open(destination, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        progress.update(task, advance=len(chunk))
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
    
    if "SEARCH_XDA" in url or "placeholder" in url:
        print(f"The URL for {component} ({type}) is currently a placeholder: {url}")
        print("Please provide a valid URL or check the database later.")
        return

    # Determine a proper destination path under devices/
    model_sanitized = model.replace(' ', '_')
    destination = f"devices/{model_sanitized}/{component}/{type}_{os.path.basename(url)}"

    print(f"Starting download of {component} ({type})...")
    if download_file(url, destination):
        if checksum and not verify_checksum(destination, checksum):
            print(f"[red]Checksum verification failed for {destination}![/red]")
            # Log the failure
            db_manager.log_operation(model, f"Download {component} {type}", f"Checksum mismatch: {checksum}", "FAILED")
        else:
            print(f"Successfully downloaded {component} {type} to {destination}")
            # Log the success
            db_manager.log_operation(model, f"Download {component} {type}", f"Downloaded to {destination}", "SUCCESS")
            # Update verified status in DB
            db_manager.set_url_verified(model, component, type, True)
