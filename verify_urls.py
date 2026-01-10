import requests
import setup

def verify_urls():
    print("Verifying tool URLs...")
    for tool, metadata in setup.TOOL_METADATA.items():
        url = metadata.get("download_url")
        if url:
            try:
                response = requests.head(url, allow_redirects=True, timeout=5)
                if response.status_code == 200:
                    print(f"[OK] {tool}: {url}")
                else:
                    print(f"[FAIL] {tool}: {url} (Status: {response.status_code})")
            except requests.RequestException as e:
                print(f"[ERROR] {tool}: {url} ({e})")
        else:
            print(f"[SKIP] {tool}: No download URL")

if __name__ == "__main__":
    verify_urls()
