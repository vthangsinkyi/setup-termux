#!/bin/bash
echo "Setting up Roblox Rejoiner environment..."

# Check memory
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

# Check root access
if ! su -c "echo test" | grep -q "test" 2>/dev/null; then
    echo "Error: Root access required. Install Magisk or equivalent and retry."
    exit 1
fi
echo "Root access verified"

# Setup storage
if [ -e "/data/data/com.termux/files/home/storage" ]; then
    rm -rf /data/data/com.termux/files/home/storage
fi
termux-setup-storage
sleep 2
echo "Storage access configured"

# Update packages and install dependencies
pkg update -y
pkg install python python-pip curl -y

# Verify Python version
PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
if [[ ! "$PYTHON_VERSION" =~ ^3\.[6-9]|^3\.[1-9][0-9] ]]; then
    echo "Error: Python 3.6 or higher required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "Python version: $PYTHON_VERSION"

# Install required Python packages
pip install --upgrade pip
pip install requests psutil prettytable
echo "Python libraries installed: requests, psutil, prettytable"

# Install additional dependencies
echo "Installing additional dependencies..."
pkg install tsu -y
pkg install android-tools -y

# Download the enhanced Rejoiner
curl -Ls "https://raw.githubusercontent.com/vthangsinkyi/setup-termux/refs/heads/main/Rejoiner.py" -o /sdcard/Download/Rejoiner.py
su -c "chmod 644 /sdcard/Download/Rejoiner.py"
echo "Rejoiner.py downloaded to /sdcard/Download"

# Create a launcher script
cat > /data/data/com.termux/files/usr/bin/rejoiner << 'EOF'
#!/bin/bash
cd /sdcard/Download
python Rejoiner.py "$@"
EOF

chmod +x /data/data/com.termux/files/usr/bin/rejoiner
echo "Launcher script 'rejoiner' created."

# Check if Roblox is installed
if ! su -c "pm list packages com.roblox.client" | grep -q "com.roblox.client"; then
    echo "Warning: Roblox is not installed."
    echo "Please install Roblox from the Play Store or download the APK manually."
fi

echo ""
echo "Setup complete!"
echo "To run Rejoiner, type: rejoiner"
echo "Or navigate to /sdcard/Download and run: python Rejoiner.py"
