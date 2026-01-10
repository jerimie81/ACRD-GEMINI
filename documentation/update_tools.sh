#!/bin/bash

# Configuration
PYTHON_SCRIPT="acrd_updater.py"
REPORT_FILE="acrd_update_report.json"
DOWNLOAD_DIR="./downloads"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting ACRD Toolset Updater...${NC}"

# 1. Run the Python script to check for updates and generate the JSON report
echo "Fetching latest version info from GitHub..."
python3 "$PYTHON_SCRIPT"

# Check if the report was generated successfully
if [ ! -f "$REPORT_FILE" ]; then
    echo -e "${RED}Error: Report file $REPORT_FILE not found. Python script failed.${NC}"
    exit 1
fi

# 2. Create download directory if it doesn't exist
if [ ! -d "$DOWNLOAD_DIR" ]; then
    mkdir -p "$DOWNLOAD_DIR"
    echo "Created directory: $DOWNLOAD_DIR"
fi

echo -e "\n${YELLOW}Processing downloads...${NC}"

# 3. Parse JSON and Download Files
# We use jq to read the file and output a clean list of: NAME | URL | FILENAME | VERSION
jq -r '.[] | select(.status == "Success") | "\(.name)|\(.url)|\(.filename)|\(.version)"' "$REPORT_FILE" | while IFS='|' read -r name url filename version; do
    
    # Skip if URL is empty or invalid
    if [ -z "$url" ] || [ "$url" == "null" ]; then
        echo -e "${RED}[SKIP] $name: No download URL found.${NC}"
        continue
    fi

    # Construct the target file path
    FILE_PATH="$DOWNLOAD_DIR/$filename"

    # Check if we already have this file
    if [ -f "$FILE_PATH" ]; then
        echo -e "${GREEN}[EXISTS] $name ($version) is already downloaded.${NC}"
    else
        echo -e "${YELLOW}[DOWNLOADING] $name ($version)...${NC}"
        echo "   Source: $url"
        
        # Run wget
        # -q: Quiet mode (turn off output)
        # --show-progress: Show the progress bar
        # -O: Output file name
        wget -q --show-progress -O "$FILE_PATH" "$url"

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}   Success! Saved to $FILE_PATH${NC}"
        else
            echo -e "${RED}   Failed to download $name.${NC}"
        fi
    fi
done

echo -e "\n${GREEN}All operations complete.${NC}"
