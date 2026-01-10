import requests
import json
import time
import os

# Configuration file name
CONFIG_FILE = "acrd_config.json"

def load_config(filename):
    """Loads the JSON configuration file."""
    if not os.path.exists(filename):
        print(f"Error: Configuration file '{filename}' not found.")
        return None
    
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON file. {e}")
            return None

def get_latest_release(api_url_template, repo_path):
    """Queries GitHub API for the latest release and direct download link."""
    url = api_url_template.format(repo_path)
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # ATTEMPT TO FIND THE ASSET DOWNLOAD URL
            # We take the first asset found (usually the main zip/apk).
            assets = data.get("assets", [])
            if assets:
                download_url = assets[0].get("browser_download_url")
                filename = assets[0].get("name")
            else:
                # Fallback to source code zip if no binary assets exist
                download_url = data.get("zipball_url", data.get("html_url"))
                filename = "source_code.zip"

            return {
                "version": data.get("tag_name", "Unknown"),
                "url": download_url,
                "filename": filename,
                "status": "Success"
            }
        elif response.status_code == 404:
            return {
                "version": "No Release Found",
                "url": "",
                "filename": "",
                "status": "No Official Release"
            }
        else:
            return {
                "version": "Error",
                "url": "",
                "filename": "",
                "status": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "version": "Error",
            "url": "",
            "filename": "",
            "status": str(e)
        }

def main():
    config = load_config(CONFIG_FILE)
    if not config:
        return

    settings = config.get("acrd_settings", {})
    tools = config.get("tools", [])
    api_template = settings.get("github_api_url", "https://api.github.com/repos/{}/releases/latest")

    print(f"Running {settings.get('project_name', 'Updater')}...\n")
    print(f"{'TOOL NAME':<25} | {'CATEGORY':<15} | {'LATEST VERSION':<20} | {'STATUS'}")
    print("-" * 85)
    
    results = []
    
    for tool in tools:
        name = tool.get("name", "Unknown Tool")
        repo = tool.get("repo")
        category = tool.get("category", "General")
        
        if not repo:
            print(f"Skipping {name}: No repository configured.")
            continue

        info = get_latest_release(api_template, repo)
        
        # Merge info with tool data for potential saving later
        tool_result = {**tool, **info}
        results.append(tool_result)
        
        print(f"{name:<25} | {category:<15} | {info['version']:<20} | {info['status']}")
        
        time.sleep(0.5)

    print("-" * 85)
    print("Update check complete.")

    # Optional: Save results to a report file
    with open("acrd_update_report.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Report saved to 'acrd_update_report.json'")

if __name__ == "__main__":
    main()
