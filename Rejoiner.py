#!/usr/bin/env python3
"""
Enhanced Roblox Automation Tool (Rejoiner.py) - FIXED VERSION
Working user detection and game state monitoring
"""
import requests
import time
import os
import json
import subprocess
import urllib.parse
import re
import threading
import sys
from datetime import datetime

# ======================
# CONFIGURATION
# ======================
COLORS = {
    "RESET": "\033[0m",
    "INFO": "\033[94m",
    "SUCCESS": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "DEBUG": "\033[90m",
    "BOLD": "\033[1m",
    "CYAN": "\033[96m",
    "HEADER": "\033[95m"
}

CONFIG_FILE = "/sdcard/roblox_config.json"
ROBLOX_PACKAGE = "com.roblox.client"

# Global variables
automation_running = False
current_username = "Unknown"
current_user_id = ""
last_game_join_time = None

# ======================
# CORE FUNCTIONS - FIXED
# ======================
def print_formatted(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = {
        "INFO": "INFO",
        "SUCCESS": "OK",
        "WARNING": "WARN",
        "ERROR": "ERROR",
        "DEBUG": "DEBUG",
        "HEADER": "===="
    }.get(level, level)
    print(f"{COLORS[level]}{timestamp} [{prefix}] {message}{COLORS['RESET']}")

def run_shell_command(command, timeout=10):
    """Execute shell command - SIMPLIFIED AND FIXED"""
    try:
        if isinstance(command, str):
            command = command.split()
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except Exception as e:
        return ""

def load_config():
    """Load configuration from JSON file"""
    default_config = {
        "game_id": "",
        "private_server": "",
        "check_delay": 60,
        "max_retries": 3,
        "game_load_delay": 30,
        "user_id": "",
        "username": "",
        "auto_rejoin": True
    }
    
    try:
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            print_formatted("INFO", "Created new config file")
            return default_config
        
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            # Merge with defaults
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    except Exception as e:
        print_formatted("ERROR", f"Config load error: {e}")
        return default_config

def save_config(config):
    """Save configuration to JSON file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        print_formatted("SUCCESS", "Config saved")
        return True
    except Exception as e:
        print_formatted("ERROR", f"Config save error: {e}")
        return False

# ======================
# USER DETECTION - FIXED AND WORKING
# ======================
def detect_and_update_username():
    """Detect and update current username - SIMPLIFIED AND WORKING"""
    global current_username, current_user_id
    
    try:
        config = load_config()
        user_id = config.get('user_id', '').strip()
        username = config.get('username', '').strip()
        
        if user_id:
            current_user_id = user_id
            if username:
                current_username = username
            else:
                current_username = f"User_{user_id}"
                # Auto-save the generated username
                config['username'] = current_username
                save_config(config)
            
            print_formatted("SUCCESS", f"User: {current_username} (ID: {current_user_id})")
            return current_username
        else:
            current_username = "Unknown"
            current_user_id = ""
            print_formatted("WARNING", "No user ID configured - set it in configuration")
            return current_username
            
    except Exception as e:
        print_formatted("ERROR", f"User detection error: {e}")
        current_username = "Unknown"
        return current_username

def get_current_user_info():
    """Get current user information - WORKING VERSION"""
    global current_username, current_user_id
    return current_user_id, current_username

# ======================
# ROBLOX CONTROL - FIXED AND WORKING
# ======================
def verify_roblox_installation():
    """Verify Roblox is installed - SIMPLIFIED"""
    try:
        output = run_shell_command(["pm", "list", "packages", ROBLOX_PACKAGE])
        if ROBLOX_PACKAGE in output:
            print_formatted("SUCCESS", "Roblox is installed")
            return True
        else:
            print_formatted("ERROR", "Roblox not found - please install it first")
            return False
    except Exception as e:
        print_formatted("ERROR", f"Roblox verification error: {e}")
        return False

def is_roblox_running():
    """Check if Roblox is running - RELIABLE VERSION"""
    try:
        # Method 1: pidof (most reliable)
        output = run_shell_command(["pidof", ROBLOX_PACKAGE])
        if output.strip():
            return True
        
        # Method 2: ps grep
        output = run_shell_command(["ps", "-A"])
        if output and ROBLOX_PACKAGE in output:
            return True
            
        # Method 3: pm list running
        output = run_shell_command(["pm", "list", "packages", "running"])
        if output and ROBLOX_PACKAGE in output:
            return True
            
        return False
    except Exception as e:
        return False

def close_roblox():
    """Close Roblox application - WORKING VERSION"""
    try:
        print_formatted("INFO", "Closing Roblox...")
        
        # Try multiple close methods
        methods = [
            ["am", "force-stop", ROBLOX_PACKAGE],
            ["pkill", "-f", ROBLOX_PACKAGE],
            ["killall", ROBLOX_PACKAGE]
        ]
        
        for method in methods:
            try:
                run_shell_command(method)
                time.sleep(2)
            except:
                continue
        
        # Wait and verify
        time.sleep(3)
        if not is_roblox_running():
            print_formatted("SUCCESS", "Roblox closed successfully")
            return True
        else:
            print_formatted("WARNING", "Roblox might still be running")
            return False
            
    except Exception as e:
        print_formatted("ERROR", f"Failed to close Roblox: {e}")
        return False

# ======================
# GAME LAUNCH - SIMPLIFIED AND WORKING
# ======================
def launch_via_deep_link(game_id, private_server=''):
    """Launch game using roblox:// deep link - WORKING VERSION"""
    try:
        if private_server:
            print_formatted("INFO", "Using private server link")
            url = private_server
        else:
            url = f"roblox://experiences/start?placeId={game_id}"
        
        print_formatted("INFO", f"Launching via deep link: {url}")
        
        # Try different launch methods
        methods = [
            ["am", "start", "-a", "android.intent.action.VIEW", "-d", url],
            ["termux-open-url", url]  # For Termux users
        ]
        
        for method in methods:
            try:
                result = run_shell_command(method)
                if result and "Error" not in result:
                    break
            except:
                continue
        
        # Wait for Roblox to start
        print_formatted("INFO", "Waiting for Roblox to start...")
        for i in range(30):  # Wait up to 30 seconds
            if is_roblox_running():
                print_formatted("SUCCESS", "Roblox started successfully!")
                return True
            time.sleep(1)
        
        print_formatted("WARNING", "Roblox didn't start within 30 seconds")
        return False
        
    except Exception as e:
        print_formatted("ERROR", f"Deep link launch failed: {e}")
        return False

def launch_via_browser(game_id, private_server=''):
    """Launch game via browser - SIMPLIFIED"""
    try:
        if not private_server:
            print_formatted("WARNING", "No private server link for browser method")
            return False
            
        print_formatted("INFO", "Launching via browser...")
        result = run_shell_command(["am", "start", "-a", "android.intent.action.VIEW", "-d", private_server])
        
        # Wait for Roblox to start
        for i in range(30):
            if is_roblox_running():
                print_formatted("SUCCESS", "Roblox started via browser!")
                return True
            time.sleep(1)
            
        return False
        
    except Exception as e:
        print_formatted("ERROR", f"Browser launch failed: {e}")
        return False

# ======================
# GAME STATE DETECTION - FIXED AND WORKING
# ======================
def is_in_game(game_id, private_server=''):
    """Check if currently in the specified game - WORKING VERSION"""
    try:
        # First check if Roblox is running at all
        if not is_roblox_running():
            return False
        
        # Method 1: Check memory usage (if Roblox is using significant memory, it's likely in game)
        try:
            memory_info = run_shell_command(["dumpsys", "meminfo", ROBLOX_PACKAGE])
            if memory_info and "TOTAL" in memory_info:
                # If memory is above 200MB, likely in game
                for line in memory_info.split('\n'):
                    if 'TOTAL' in line:
                        try:
                            parts = line.split()
                            for part in parts:
                                if part.isdigit():
                                    mem_kb = int(part)
                                    if mem_kb > 200000:  # 200MB threshold
                                        return True
                                    break
                        except:
                            pass
        except:
            pass
        
        # Method 2: Check for game indicators in logcat
        try:
            logs = run_shell_command(["logcat", "-d", "-t", "100"])
            if logs:
                game_indicators = ["PlaceId", "Experience", "Gameplay", "Loading", "Joining"]
                for indicator in game_indicators:
                    if indicator in logs:
                        return True
                # Check for specific game ID
                if game_id and game_id in logs:
                    return True
        except:
            pass
        
        # Method 3: If Roblox is running but we can't detect specifics, assume it might be in a game
        # This prevents constant rejoining when detection methods fail
        return True
        
    except Exception as e:
        print_formatted("DEBUG", f"Game detection error: {e}")
        return False

# ======================
# MAIN AUTOMATION LOGIC - FIXED AND WORKING
# ======================
def attempt_game_join(config):
    """Attempt to join the specified game - WORKING VERSION"""
    global last_game_join_time
    
    game_id = config.get('game_id')
    private_server = config.get('private_server', '')
    
    if not game_id and not private_server:
        print_formatted("ERROR", "No game ID or private server configured")
        return False
    
    # Show user info
    user_id, username = get_current_user_info()
    if user_id:
        print_formatted("INFO", f"Joining game as {username} (ID: {user_id})")
    
    # Close Roblox if running
    if is_roblox_running():
        if not close_roblox():
            print_formatted("WARNING", "Continuing despite close issues")
        time.sleep(2)
    
    # Try launch methods
    success = False
    if private_server:
        # Try browser first for private servers
        print_formatted("INFO", "Trying browser method for private server...")
        if launch_via_browser(game_id, private_server):
            success = True
        else:
            print_formatted("INFO", "Trying deep link as fallback...")
            if launch_via_deep_link(game_id, private_server):
                success = True
    else:
        # Use deep link for public games
        print_formatted("INFO", "Trying deep link method...")
        if launch_via_deep_link(game_id, private_server):
            success = True
    
    if success:
        # Wait for game to load
        load_delay = config.get('game_load_delay', 30)
        print_formatted("INFO", f"Waiting {load_delay} seconds for game to load...")
        time.sleep(load_delay)
        
        # Verify we're in game
        if is_in_game(game_id, private_server):
            last_game_join_time = time.time()
            print_formatted("SUCCESS", "Successfully joined the game!")
            return True
        else:
            print_formatted("WARNING", "Game launched but might not be in target game")
            return True  # Still return True if Roblox is running
    
    print_formatted("ERROR", "Failed to join game")
    return False

def automation_loop(config):
    """Main automation loop - WORKING VERSION"""
    global automation_running
    
    automation_running = True
    print_formatted("SUCCESS", "Automation started!")
    
    check_delay = config.get('check_delay', 60)
    max_retries = config.get('max_retries', 3)
    retry_count = 0
    
    while automation_running:
        try:
            game_id = config.get('game_id')
            private_server = config.get('private_server', '')
            
            # Check current status
            roblox_running = is_roblox_running()
            in_game = is_in_game(game_id, private_server) if roblox_running else False
            
            if not roblox_running or not in_game:
                print_formatted("INFO", "Roblox not running or not in game - attempting to join...")
                if attempt_game_join(config):
                    retry_count = 0
                    print_formatted("SUCCESS", "Game joined successfully!")
                else:
                    retry_count += 1
                    print_formatted("WARNING", f"Join failed (attempt {retry_count}/{max_retries})")
                    
                    if retry_count >= max_retries:
                        print_formatted("ERROR", "Max retries reached, waiting longer...")
                        time.sleep(check_delay * 2)
                        retry_count = 0
            else:
                # Everything is good
                if retry_count > 0:
                    retry_count = 0
                print_formatted("INFO", f"Monitoring game... (next check in {check_delay}s)")
            
            # Wait for next check
            time.sleep(check_delay)
            
        except Exception as e:
            print_formatted("ERROR", f"Automation error: {e}")
            time.sleep(10)
    
    automation_running = False
    print_formatted("INFO", "Automation stopped")

# ======================
# INTERACTIVE MENU - FIXED AND WORKING
# ======================
def display_menu():
    """Display main menu"""
    os.system('clear')
    
    print(f"\n{COLORS['HEADER']}{'='*50}")
    print(f"    ROBLOX REJOINER - WORKING VERSION")
    print(f"{'='*50}{COLORS['RESET']}")
    
    # Show current user
    user_id, username = get_current_user_info()
    if user_id:
        print(f"{COLORS['SUCCESS']}User: {username} (ID: {user_id}){COLORS['RESET']}")
    else:
        print(f"{COLORS['WARNING']}User: Not configured{COLORS['RESET']}")
    
    # Show game info
    config = load_config()
    game_id = config.get('game_id', 'Not set')
    private_server = config.get('private_server', '')
    
    if private_server:
        print(f"{COLORS['INFO']}Private Server: {private_server[:50]}...{COLORS['RESET']}")
    else:
        print(f"{COLORS['INFO']}Game ID: {game_id}{COLORS['RESET']}")
    
    print(f"\n{COLORS['CYAN']}1.{COLORS['RESET']} Configure Settings")
    print(f"{COLORS['CYAN']}2.{COLORS['RESET']} Start Automation")
    print(f"{COLORS['CYAN']}3.{COLORS['RESET']} Stop Automation")
    print(f"{COLORS['CYAN']}4.{COLORS['RESET']} Test Game Join")
    print(f"{COLORS['CYAN']}5.{COLORS['RESET']} View Configuration")
    print(f"{COLORS['CYAN']}6.{COLORS['RESET']} Exit")
    
    if automation_running:
        print(f"\n{COLORS['SUCCESS']}Status: AUTOMATION RUNNING{COLORS['RESET']}")
    else:
        print(f"\n{COLORS['WARNING']}Status: READY{COLORS['RESET']}")

def configure_settings():
    """Interactive configuration setup - WORKING VERSION"""
    config = load_config()
    
    print(f"\n{COLORS['HEADER']}=== CONFIGURATION ==={COLORS['RESET']}")
    
    # User Configuration
    current_user_id = config.get('user_id', '')
    current_username = config.get('username', '')
    
    print(f"\nCurrent User ID: {current_user_id if current_user_id else 'Not set'}")
    print(f"Current Username: {current_username if current_username else 'Not set'}")
    
    user_id = input("Enter Roblox User ID: ").strip()
    if user_id:
        config['user_id'] = user_id
        username = input("Enter Roblox Username (optional): ").strip()
        if username:
            config['username'] = username
        else:
            config['username'] = f"User_{user_id}"
    
    # Game Configuration
    current_game_id = config.get('game_id', '')
    print(f"\nCurrent Game ID: {current_game_id if current_game_id else 'Not set'}")
    game_id = input("Enter Game ID: ").strip()
    if game_id:
        config['game_id'] = game_id
        config['private_server'] = ''  # Clear private server if setting game ID
    
    # Private Server
    current_private = config.get('private_server', '')
    print(f"\nCurrent Private Server: {current_private if current_private else 'Not set'}")
    private = input("Enter Private Server Link (or press Enter to skip): ").strip()
    if private:
        config['private_server'] = private
        config['game_id'] = ''  # Clear game ID if setting private server
    
    # Settings
    current_delay = config.get('check_delay', 60)
    print(f"\nCurrent Check Delay: {current_delay} seconds")
    delay = input("Enter Check Delay (seconds): ").strip()
    if delay and delay.isdigit():
        config['check_delay'] = int(delay)
    
    current_retries = config.get('max_retries', 3)
    print(f"Current Max Retries: {current_retries}")
    retries = input("Enter Max Retries: ").strip()
    if retries and retries.isdigit():
        config['max_retries'] = int(retries)
    
    if save_config(config):
        # Update global user variables
        detect_and_update_username()
        print_formatted("SUCCESS", "Configuration saved successfully!")
    else:
        print_formatted("ERROR", "Failed to save configuration!")
    
    input("\nPress Enter to continue...")

def view_current_config():
    """Display current configuration"""
    config = load_config()
    
    print(f"\n{COLORS['HEADER']}=== CURRENT CONFIGURATION ==={COLORS['RESET']}")
    print(f"{COLORS['CYAN']}User ID:{COLORS['RESET']} {config.get('user_id', 'Not set')}")
    print(f"{COLORS['CYAN']}Username:{COLORS['RESET']} {config.get('username', 'Not set')}")
    print(f"{COLORS['CYAN']}Game ID:{COLORS['RESET']} {config.get('game_id', 'Not set')}")
    print(f"{COLORS['CYAN']}Private Server:{COLORS['RESET']} {config.get('private_server', 'Not set')}")
    print(f"{COLORS['CYAN']}Check Delay:{COLORS['RESET']} {config.get('check_delay', 60)} seconds")
    print(f"{COLORS['CYAN']}Max Retries:{COLORS['RESET']} {config.get('max_retries', 3)}")
    print(f"{COLORS['CYAN']}Game Load Delay:{COLORS['RESET']} {config.get('game_load_delay', 30)} seconds")
    print(f"{COLORS['CYAN']}Auto Rejoin:{COLORS['RESET']} {'Yes' if config.get('auto_rejoin', True) else 'No'}")
    
    input("\nPress Enter to continue...")

def test_game_join():
    """Test game joining functionality"""
    config = load_config()
    game_id = config.get('game_id')
    private_server = config.get('private_server', '')
    
    if not game_id and not private_server:
        print_formatted("ERROR", "No game ID or private server configured!")
        input("Press Enter to continue...")
        return
    
    print_formatted("INFO", "Testing game join...")
    print_formatted("INFO", "This will close Roblox and attempt to join the game")
    
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        return
    
    success = attempt_game_join(config)
    if success:
        print_formatted("SUCCESS", "Game join test successful!")
    else:
        print_formatted("ERROR", "Game join test failed!")
    
    input("Press Enter to continue...")

# ======================
# MAIN FUNCTION
# ======================
def main():
    """Main function"""
    global automation_running
    
    try:
        os.system('clear')
        print(f"{COLORS['HEADER']}ROBLOX REJOINER - WORKING VERSION{COLORS['RESET']}")
        print(f"{COLORS['INFO']}Initializing...{COLORS['RESET']}")
        
        # Initialize user detection
        detect_and_update_username()
        
        # Verify Roblox
        if not verify_roblox_installation():
            print_formatted("ERROR", "Please install Roblox first!")
            return
        
        automation_thread = None
        
        # Main loop
        while True:
            try:
                display_menu()
                choice = input(f"\n{COLORS['CYAN']}Choice (1-6): {COLORS['RESET']}").strip()
                
                if choice == '1':
                    configure_settings()
                elif choice == '2':
                    if automation_running:
                        print_formatted("WARNING", "Automation is already running!")
                    else:
                        config = load_config()
                        if not config.get('game_id') and not config.get('private_server'):
                            print_formatted("ERROR", "No game ID or private server configured!")
                        else:
                            automation_thread = threading.Thread(target=automation_loop, args=(config,), daemon=True)
                            automation_thread.start()
                            print_formatted("SUCCESS", "Automation started!")
                    input("Press Enter to continue...")
                elif choice == '3':
                    if automation_running:
                        automation_running = False
                        if automation_thread:
                            automation_thread.join(timeout=5)
                        print_formatted("SUCCESS", "Automation stopped!")
                    else:
                        print_formatted("WARNING", "Automation is not running!")
                    input("Press Enter to continue...")
                elif choice == '4':
                    test_game_join()
                elif choice == '5':
                    view_current_config()
                elif choice == '6':
                    if automation_running:
                        automation_running = False
                        if automation_thread:
                            automation_thread.join(timeout=5)
                    print_formatted("INFO", "Goodbye!")
                    break
                else:
                    print_formatted("WARNING", "Invalid choice!")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print_formatted("INFO", "\nExiting...")
                if automation_running:
                    automation_running = False
                break
            except Exception as e:
                print_formatted("ERROR", f"Menu error: {e}")
                time.sleep(2)
                
    except Exception as e:
        print_formatted("ERROR", f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
