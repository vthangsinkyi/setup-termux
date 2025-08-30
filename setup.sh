#!/bin/bash
echo "Setting up Koala Hub Auto-Rejoin environment..."

MEMORY=$(free -m | awk '/Mem:/ {print $2}' 2>/dev/null || echo "0")
if [ -z "$MEMORY" ] || [ "$MEMORY" -eq 0 ]; then
    echo "Warning: Unable to check memory. Ensure at least 512MB is available."
else
    if [ "$MEMORY" -lt 512 ]; then
        echo "Error: Less than 512MB memory available ($MEMORY MB). Free up memory and retry."
        exit 1
    fi
    echo "Memory check: $MEMORY MB available"
fi

if ! su -c "echo test" | grep -q "test" 2>/dev/null; then
    echo "Error: Root access required. Install Magisk or equivalent and retry."
    exit 1
fi
echo "Root access verified"

if [ -e "/data/data/com.termux/files/home/storage" ]; then
    rm -rf /data/data/com.termux/files/home/storage
fi
termux-setup-storage
sleep 2
echo "Storage access configured"

# Clear package cache to free up space
pkg clean
apt-get clean

# Update and install packages with more specific approach
pkg update -y && pkg upgrade -y
pkg install python -y
pkg install curl -y

# Install pip using ensurepip (built into Python)
python -m ensurepip --upgrade
python -m pip install --upgrade pip

PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
if [[ ! "$PYTHON_VERSION" =~ ^3\.[6-9]|^3\.[1-9][0-9] ]]; then
    echo "Error: Python 3.6 or higher required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "Python version: $PYTHON_VERSION"

python -c "import urllib.parse" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: urllib.parse module not found. Reinstalling Python..."
    pkg uninstall python -y
    pkg install python -y
    python -c "import urllib.parse" 2>/dev/null || {
        echo "Error: Failed to verify urllib.parse after reinstall."
        exit 1
    }
fi
echo "urllib.parse module verified"

# Install required Python packages
python -m pip install requests psutil prettytable
echo "Python libraries installed: requests, psutil, prettytable"

# Download Rejoiner.py
curl -Ls "https://raw.githubusercontent.com/vthangsinkyi/setup-termux/refs/heads/main/Rejoiner.py" -o /sdcard/Download/Rejoiner.py
su -c "chmod 644 /sdcard/Download/Rejoiner.py"
echo "Rejoiner.py downloaded to /sdcard/Download"

if ! su -c "pm list packages com.roblox.client" | grep -q "com.roblox.client"; then
    echo "Warning: Roblox is not installed."
    echo "Please install Roblox from the Play Store or download the APK."
fi

echo ""
echo "Setup completed successfully!"
echo "To run the tool:"
echo "cd /sdcard/Download && python Rejoiner.py"
