#!/bin/bash

# ACRD-GEMINI Launcher Script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting ACRD-GEMINI Launcher...${NC}"

# 1. Check Python Version (3.10+)
echo -n "Checking Python version... "
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}FAIL${NC}"
    echo "Error: python3 could not be found."
    exit 1
fi

python3 -c "import sys; exit(0) if sys.version_info >= (3, 10) else exit(1)"
if [ $? -ne 0 ]; then
    echo -e "${RED}FAIL${NC}"
    echo "Error: Python 3.10+ is required."
    exit 1
else
    echo -e "${GREEN}OK${NC}"
fi

# 2. Check System Dependencies
echo "Checking system dependencies..."

# Check for Java
echo -n "  - Java (OpenJDK/JRE)... "
if command -v java &> /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "Error: Java is not installed. Required for tools like Apktool."
    echo "Please install it (e.g., sudo apt install default-jre)."
    exit 1
fi

# Check for Unzip
echo -n "  - Unzip... "
if command -v unzip &> /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "Error: unzip is not installed."
    echo "Please install it (e.g., sudo apt install unzip)."
    exit 1
fi

# Check for lsusb (libusb)
echo -n "  - lsusb (libusb)... "
if command -v lsusb &> /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}WARNING${NC}"
    echo "Warning: lsusb is not found. Device detection might be limited."
fi

# 3. Install Python Dependencies
echo "Installing/Verifying Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install python dependencies.${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: requirements.txt not found.${NC}"
    exit 1
fi

# 4. Run Setup Script (Tools Download & DB Init)
echo "Running setup configuration..."
python3 setup.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Setup failed. Please check the errors above.${NC}"
    exit 1
fi

# 5. Launch Main Application
echo -e "${GREEN}----------------------------------------${NC}"
echo -e "${GREEN}       Launching ACRD-GEMINI TUI        ${NC}"
echo -e "${GREEN}----------------------------------------${NC}"

python3 main.py
