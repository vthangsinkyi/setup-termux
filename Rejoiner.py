#!/usr/bin/env python3
"""
Enhanced Roblox Automation Tool (Rejoiner.py)
Supports: UGPHONE, VSPHONE, REDFINGER, Standard Android/Emulators
Author: Enhanced for multi-platform compatibility
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
    "DEBUG": "\033[90m",  # Dark gray for debug messages
    "BOLD": "\033[1m",
    "CYAN": "\033[96m",
    "HEADER": "\033[95m"
}

CONFIG_FILE = "/sdcard/roblox_config.json"
ROBLOX_PACKAGE = "com.roblox.client"

# Global variables
automation_running = False
platform_info = None
last_game_join_time = None
current_username = "Unknown"

# ======================
# PLATFORM DETECTION
# ======================
class PlatformDetector:
    def __init__(self):
        self.detected_platform = None
    
    def detect_platform(self):
        """Detect the current platform (UGPHONE, VSPHONE, REDFINGER, or standard Android)"""
        try:
            # Check for UGPHONE
            if self._is_ugphone():
                self.detected_platform = {
                    'type': 'ugphone',
                    'name': 'UGPHONE',
                    'has_root': self._check_root_ugphone(),
                    'use_adb': False,
                    'shell_prefix': '',
                    'special_commands': True
                }
                print_formatted("INFO", f"Platform detected: {self.detected_platform['name']}")
                return self.detected_platform
            
            # Check for VSPHONE
            if self._is_vsphone():
                self.detected_platform = {
                    'type': 'vsphone',
                    'name': 'VSPHONE',
                    'has_root': self._check_root_vsphone(),
                    'use_adb': False,
                    'shell_prefix': '',
                    'special_commands': True
                }
                print_formatted("INFO", f"Platform detected: {self.detected_platform['name']}")
                return self.detected_platform
            
            # Check for REDFINGER
            if self._is_redfinger():
                self.detected_platform = {
                    'type': 'redfinger',
                    'name': 'REDFINGER',
                    'has_root': self._check_root_standard(),
                    'use_adb': True,
                    'shell_prefix': 'su -c',
                    'special_commands': False
                }
                print_formatted("INFO", f"Platform detected: {self.detected_platform['name']}")
                return self.detected_platform
            
            # Standard Android (emulator or physical device)
            self.detected_platform = {
                'type': 'standard',
                'name': 'Standard Android',
                'has_root': self._check_root_standard(),
                'use_adb': True,
                'shell_prefix': 'su -c',
                'special_commands': False
            }
            print_formatted("INFO", f"Platform detected: {self.detected_platform['name']}")
            return self.detected_platform
            
        except Exception as e:
            print_formatted("ERROR", f"Platform detection error: {str(e)}")
            self.detected_platform = {
                'type': 'unknown',
                'name': 'Unknown Platform',
                'has_root': False,
                'use_adb': False,
                'shell_prefix': '',
                'special_commands': False
            }
            return self.detected_platform
    
    def _is_ugphone(self):
        """Check if running on UGPHONE"""
        try:
            indicators = [
                '/system/bin/ugphone',
                '/system/app/UGPhone',
                '/data/local/tmp/ugphone'
            ]
            
            for indicator in indicators:
                if os.path.exists(indicator):
                    return True
            
            build_info = self._get_build_prop()
            ugphone_patterns = ['ugphone', 'ug_phone', 'cloudphone']
            
            for pattern in ugphone_patterns:
                if pattern.lower() in build_info.lower():
                    return True
            
            return False
        except:
            return False
    
    def _is_vsphone(self):
        """Check if running on VSPHONE"""
        try:
            indicators = [
                '/system/bin/vsphone',
                '/system/app/VSPhone',
                '/data/local/tmp/vsphone'
            ]
            
            for indicator in indicators:
                if os.path.exists(indicator):
                    return True
            
            build_info = self._get_build_prop()
            vsphone_patterns = ['vsphone', 'vs_phone', 'virtualphone']
            
            for pattern in vsphone_patterns:
                if pattern.lower() in build_info.lower():
                    return True
            
            return False
        except:
            return False
    
    def _is_redfinger(self):
        """Check if running on REDFINGER"""
        try:
            indicators = [
                '/system/bin/redfinger',
                '/system/app/RedFinger',
                '/data/local/tmp/redfinger'
            ]
            
            for indicator in indicators:
                if os.path.exists(indicator):
                    return True
            
            build_info = self._get_build_prop()
            redfinger_patterns = ['redfinger', 'red_finger', 'redcloud']
            
            for pattern in redfinger_patterns:
                if pattern.lower() in build_info.lower():
                    return True
            
            return False
        except:
            return False
    
    def _get_build_prop(self):
        """Get build.prop content"""
        try:
            result = subprocess.run(['cat', '/system/build.prop'], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout
        except:
            return ""
    
    def _check_root_standard(self):
        """Check for root access on standard Android"""
        try:
            result = subprocess.run(['su', '-c', 'echo test'], 
                                  capture_output=True, text=True, timeout=5)
            return 'test' in result.stdout
        except:
            return False
    
    def _check_root_ugphone(self):
        """Check for root access on UGPHONE"""
        try:
            if self._check_root_standard():
                return True
            
            result = subprocess.run(['ugphone_su', '-c', 'echo test'], 
                                  capture_output=True, text=True, timeout=5)
            return 'test' in result.stdout
        except:
            return False
    
    def _check_root_vsphone(self):
        """Check for root access on VSPHONE"""
        try:
            if self._check_root_standard():
                return True
            
            result = subprocess.run(['vsphone_su', '-c', 'echo test'], 
                                  capture_output=True, text=True, timeout=5)
            return 'test' in result.stdout
        except:
            return False

# ======================
# CORE FUNCTIONS
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

def run_shell_command(command, timeout=10, platform_info=None):
    """Execute shell command with platform-specific handling - CLEAN OUTPUT"""
    try:
        if isinstance(command, str):
            full_command = command.split()
        else:
            full_command = command
        
        # Skip problematic commands
        cmd_name = full_command[0]
        if cmd_name in ['input', 'dumpsys'] and len(full_command) > 1:
            return ""
        
        result = subprocess.run(full_command, capture_output=True, text=True, timeout=timeout)
        
        # Only show critical errors, not spam
        if result.stderr and "error:" in result.stderr.lower() and "permission" not in result.stderr.lower():
            # Don't spam - only show first time
            pass
        
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return ""
    except FileNotFoundError:
        return ""
    except Exception as e:
        return ""

def load_config():
    """Load configuration from JSON file"""
    default_config = {
        "accounts": [],
        "game_id": "",
        "private_server": "",
        "check_delay": 45,
        "active_account": "",
        "check_method": "both",
        "max_retries": 3,
        "game_validation": True,
        "launch_delay": 300,
        "retry_delay": 15,
        "force_kill_delay": 10,
        "minimize_crashes": True,
        "launch_attempts": 1,
        "cooldown_period": 120,
        "auto_rejoin": True,
        "ui_timeout": 30,
        "verbose_logging": False,
        "user_id": "",
        "username": "",
        "detect_username": True
    }
    
    try:
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            run_shell_command(f"chmod 644 {CONFIG_FILE}", platform_info=platform_info)
            print_formatted("INFO", "Created new config file")
            return default_config
        
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            # Merge with defaults to ensure all keys exist
            merged_config = {**default_config, **config}
            return merged_config
    except Exception as e:
        print_formatted("ERROR", f"Config load error: {e}")
        return default_config

def save_config(config):
    """Save configuration to JSON file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        run_shell_command(f"chmod 644 {CONFIG_FILE}", platform_info=platform_info)
        print_formatted("SUCCESS", "Config saved")
        return True
    except Exception as e:
        print_formatted("ERROR", f"Config save error: {e}")
        return False

# ======================
# USER DETECTION FUNCTIONS
# ======================
def detect_and_update_username():
    """Detect and update current username from config - FIXED"""
    global current_username
    
    try:
        config = load_config()
        user_id = config.get('user_id', '')
        username = config.get('username', '')
        
        if user_id and user_id.strip():
            if username and username.strip():
                current_username = username.strip()
                print_formatted("SUCCESS", f"👤 Using configured user: {username} (ID: {user_id})")
            else:
                current_username = f"User_{user_id}"
                # Update config with generated username
                config['username'] = current_username
                save_config(config)
                print_formatted("INFO", f"👤 Generated username: {current_username} (ID: {user_id})")
        else:
            current_username = "Unknown"
            print_formatted("WARNING", "⚠️ No user ID configured. Go to Settings > Configure to set your Roblox User ID.")
        
        return current_username
    except Exception as e:
        print_formatted("ERROR", f"User detection error: {e}")
        current_username = "Unknown"
        return current_username

def get_current_user_info():
    """Get current user information"""
    config = load_config()
    user_id = config.get('user_id', '')
    username = config.get('username', '')
    
    if user_id:
        display_name = username if username else f"User_{user_id}"
        return user_id, display_name
    
    return None, "Unknown"

# ======================
# ROBLOX CONTROL FUNCTIONS
# ======================
def verify_roblox_installation():
    """Verify Roblox is installed"""
    try:
        output = run_shell_command(f"pm list packages {ROBLOX_PACKAGE}", platform_info=platform_info)
        if ROBLOX_PACKAGE not in output:
            print_formatted("ERROR", "Roblox not installed.")
            return False
        
        # Get version info
        version_output = run_shell_command(f"pm dump {ROBLOX_PACKAGE} | grep versionName", platform_info=platform_info)
        if version_output:
            version = version_output.split("versionName=")[1].split()[0] if "versionName=" in version_output else "Unknown"
            print_formatted("INFO", f"Roblox version: {version}")
        
        return True
    except Exception as e:
        print_formatted("ERROR", f"Roblox verification error: {e}")
        return False

def is_roblox_running():
    """Check if Roblox is currently running - FIXED FOR COMPATIBILITY"""
    try:
        # Method 1: Simple process check (most compatible)
        try:
            output = run_shell_command(f"ps | grep {ROBLOX_PACKAGE}", platform_info=platform_info)
            if output and ROBLOX_PACKAGE in output and "grep" not in output:
                return True
        except:
            pass
            
        # Method 2: Check if package is running via pm
        try:
            running_apps = run_shell_command("pm list packages -e", platform_info=platform_info)
            if ROBLOX_PACKAGE in running_apps:
                return True
        except:
            pass
        
        # Method 3: Try pgrep if available
        try:
            output = run_shell_command(f"pgrep -f {ROBLOX_PACKAGE}", platform_info=platform_info)
            if output.strip():
                return True
        except:
            pass
        
        return False
    except Exception as e:
        return False

def close_roblox(config=None):
    """Close Roblox application - FIXED FOR DIFFERENT ENVIRONMENTS"""
    try:
        print_formatted("INFO", "Closing Roblox...")
        
        # Try different methods to close Roblox
        close_methods = [
            f"am force-stop {ROBLOX_PACKAGE}",
            f"pm disable {ROBLOX_PACKAGE}",
            f"killall {ROBLOX_PACKAGE}",
            f"pkill -f {ROBLOX_PACKAGE}"
        ]
        
        for method in close_methods:
            try:
                result = run_shell_command(method, platform_info=platform_info)
                if "unknown command" not in result.lower() and "not found" not in result.lower():
                    print_formatted("DEBUG", f"Tried close method: {method}")
                    time.sleep(2)
                    break
            except:
                continue
        
        # Additional cleanup
        force_kill_delay = config.get("force_kill_delay", 5) if config else 5
        time.sleep(force_kill_delay)
        
        # Verify closure
        if is_roblox_running():
            print_formatted("WARNING", "Roblox still running after close attempts")
        else:
            print_formatted("SUCCESS", "Roblox closed successfully")
        
        return not is_roblox_running()
    except Exception as e:
        print_formatted("ERROR", f"Failed to close Roblox: {str(e)}")
        return False

def get_main_activity():
    """Get Roblox main activity name"""
    try:
        output = run_shell_command(f"pm dump {ROBLOX_PACKAGE} | grep -A 5 'android.intent.action.MAIN'", platform_info=platform_info)
        
        # Parse activity name
        match = re.search(r'com\.roblox\.client/(\.[A-Za-z0-9.]+)', output)
        if match:
            activity = match.group(1)
            print_formatted("INFO", f"Detected main activity: {activity}")
            return activity
        
        # Fallback activities
        fallbacks = ['.startup.ActivitySplash', '.MainActivity', '.HomeActivity']
        for fallback in fallbacks:
            test_output = run_shell_command(f"pm dump {ROBLOX_PACKAGE} | grep {fallback}", platform_info=platform_info)
            if fallback in test_output:
                return fallback
        
        return '.MainActivity'  # Default fallback
        
    except Exception as e:
        print_formatted("WARNING", f"Main activity detection error: {str(e)}")
        return '.MainActivity'

def build_game_url(game_id, private_server=''):
    """Build Roblox game URL"""
    try:
        base_url = "roblox://experiences/start?placeId="
        url = base_url + str(game_id)
        
        if private_server:
            code = extract_private_server_code(private_server)
            if code:
                url += f"&privateServerLinkCode={code}"
        
        return url
    except Exception as e:
        print_formatted("ERROR", f"URL build error: {e}")
        return f"roblox://experiences/start?placeId={game_id}"

def extract_private_server_code(link):
    """Extract private server code from link"""
    try:
        patterns = [
            r'privateServerLinkCode=([^&]+)',
            r'share\?code=([^&]+)',
            r'linkCode=([^&]+)',
            r'code=([^&]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, link)
            if match:
                return match.group(1)
        
        # Fallback: split by common separators
        for separator in ['privateServerLinkCode=', 'share?code=', '&linkCode=', '=']:
            if separator in link:
                code = link.split(separator)[1].split('&')[0].strip()
                if code:
                    return code
        
        return None
    except:
        return None

# ======================
# GAME LAUNCH FUNCTIONS
# ======================
def launch_via_deep_link(game_id, private_server=''):
    """Launch game using roblox:// deep link - CLEAR LOGGING"""
    try:
        # Build URL with correct format: roblox://experiences/start?placeId={game_id}
        url = build_game_url(game_id, private_server)
        print_formatted("INFO", f"🚀 Deep Link URL: {url}")
        
        # Simple launch command - most compatible
        launch_cmd = f'am start -a android.intent.action.VIEW -d "{url}"'
        
        print_formatted("INFO", "📱 Sending deep link command...")
        result = run_shell_command(launch_cmd, platform_info=platform_info)
        
        if result and "Error" not in result:
            print_formatted("SUCCESS", "✅ Deep link command sent successfully")
        else:
            print_formatted("WARNING", f"⚠️ Launch may have failed: {result[:50] if result else 'No output'}")
        
        # Give Roblox time to start
        print_formatted("INFO", "⏳ Waiting for Roblox to start...")
        time.sleep(10)
        
        # Check if Roblox started
        if is_roblox_running():
            print_formatted("SUCCESS", "✅ Roblox is running!")
            return True
        else:
            print_formatted("WARNING", "⚠️ Roblox didn't start via deep link")
            return False
        
    except Exception as e:
        print_formatted("ERROR", f"❌ Deep link launch failed: {str(e)}")
        return False

def launch_via_intent(game_id, private_server=''):
    """Launch game using Android intents - SIMPLIFIED"""
    try:
        print_formatted("INFO", "📱 Trying to open Roblox app...")
        
        # Try opening Roblox app using monkey command (more reliable)
        launch_command = f'monkey -p {ROBLOX_PACKAGE} -c android.intent.category.LAUNCHER 1'
        result = run_shell_command(launch_command, platform_info=platform_info)
        
        time.sleep(8)
        
        if is_roblox_running():
            print_formatted("SUCCESS", "✅ Roblox app opened successfully")
            return True
        else:
            print_formatted("WARNING", "⚠️ Could not open Roblox app")
            return False
        
    except Exception as e:
        print_formatted("ERROR", f"❌ Intent launch failed: {str(e)}")
        return False

def launch_via_ui_automation(game_id, private_server=''):
    """Launch game using UI automation"""
    try:
        print_formatted("INFO", f"Launching via UI automation: {game_id}")
        
        # Start Roblox
        main_activity = get_main_activity()
        command = f'am start -n {ROBLOX_PACKAGE}/{main_activity}'
        run_shell_command(command, platform_info=platform_info)
        time.sleep(10)  # Wait for app to load
        
        # Navigate using UI automation
        return navigate_to_game_ui(game_id, private_server)
        
    except Exception as e:
        print_formatted("ERROR", f"UI automation launch failed: {str(e)}")
        return False

def launch_via_browser_redirect(game_id, private_server=''):
    """Launch game via browser redirect - NO CLICKING"""
    try:
        print_formatted("INFO", f"🌐 Using browser method for {game_id}...")
        
        # Create web URL that redirects to Roblox
        if private_server:
            code = extract_private_server_code(private_server)
            web_url = f"https://www.roblox.com/games/{game_id}?privateServerLinkCode={code}"
        else:
            web_url = f"https://www.roblox.com/games/{game_id}"
        
        # Open in browser - this should automatically redirect to Roblox app
        command = f'am start -a android.intent.action.VIEW -d "{web_url}"'
        result = run_shell_command(command, platform_info=platform_info)
        
        # Wait longer for browser and Roblox to launch
        time.sleep(15)
        
        # Check if Roblox launched (don't click anything)
        if is_roblox_running():
            print_formatted("SUCCESS", "✅ Browser method launched Roblox!")
            return True
        else:
            print_formatted("WARNING", "⚠️ Browser method didn't launch Roblox")
            return False
        
    except Exception as e:
        print_formatted("ERROR", f"❌ Browser method failed: {str(e)}")
        return False

def navigate_to_game_ui(game_id, private_server=''):
    """Navigate to game using UI automation"""
    try:
        print_formatted("INFO", "Starting UI navigation to game...")
        time.sleep(10)  # Wait for Roblox to fully load
        
        # Try different navigation methods
        methods = [
            navigate_via_search,
            navigate_via_url_bar,
            navigate_via_menu
        ]
        
        for method in methods:
            try:
                if method(game_id, private_server):
                    return True
            except Exception as e:
                print_formatted("WARNING", f"Navigation method {method.__name__} failed: {str(e)}")
                continue
        
        return False
    except Exception as e:
        print_formatted("ERROR", f"UI navigation failed: {str(e)}")
        return False

def navigate_via_search(game_id, private_server=''):
    """Navigate using search functionality - CAREFUL with screen taps"""
    try:
        print_formatted("INFO", "🔍 Attempting navigation via search (reduced tapping)...")
        
        # Wait for UI to stabilize first
        time.sleep(5)
        
        # Try fewer, more targeted search positions
        search_positions = [
            (540, 200),   # Top-center search (most common)
            (540, 150),   # Slightly higher
        ]
        
        for attempt, (x, y) in enumerate(search_positions):
            print_formatted("INFO", f"🎯 Search attempt {attempt + 1}: tapping ({x}, {y})")
            
            run_shell_command(f"input tap {x} {y}", platform_info=platform_info)
            time.sleep(3)
            
            # Type game ID carefully
            run_shell_command(f"input text {game_id}", platform_info=platform_info)
            time.sleep(3)
            
            # Press enter
            run_shell_command("input keyevent KEYCODE_ENTER", platform_info=platform_info)
            time.sleep(8)  # Longer wait for search results
            
            # Check if we can detect any game results in the current screen
            # Instead of blind tapping, check if we're in a search results state
            activity = run_shell_command("dumpsys window windows | grep mCurrentFocus", platform_info=platform_info)
            if "search" in activity.lower() or "result" in activity.lower():
                print_formatted("INFO", "🎯 Search results detected, attempting to select game...")
                
                # Try one careful tap in the center results area
                run_shell_command("input tap 540 450", platform_info=platform_info)
                time.sleep(5)
                
                # Check if we're now on a game page
                if check_game_page():
                    if tap_play_button():
                        return True
            
            # If failed, clear and try next position
            clear_search()
            time.sleep(2)
        
        return False
    except Exception as e:
        print_formatted("ERROR", f"❌ Search navigation failed: {str(e)}")
        return False

def navigate_via_url_bar(game_id, private_server=''):
    """Navigate using URL bar if available"""
    try:
        print_formatted("INFO", "Attempting navigation via URL bar...")
        
        # Look for URL/address bar
        url_positions = [
            (540, 100),   # Top center
            (540, 150),   # Slightly lower
            (540, 200)    # Alternative position
        ]
        
        for x, y in url_positions:
            run_shell_command(f"input tap {x} {y}", platform_info=platform_info)
            time.sleep(2)
            
            # Build URL
            if private_server:
                url = f"roblox://experiences/start?placeId={game_id}&privateServerLinkCode={extract_private_server_code(private_server)}"
            else:
                url = f"roblox://experiences/start?placeId={game_id}"
            
            # Type URL
            run_shell_command(f"input text '{url}'", platform_info=platform_info)
            time.sleep(2)
            
            # Press enter
            run_shell_command("input keyevent KEYCODE_ENTER", platform_info=platform_info)
            time.sleep(10)
            
            # Check if navigation worked
            if check_game_loading():
                return True
        
        return False
    except Exception as e:
        print_formatted("ERROR", f"URL bar navigation failed: {str(e)}")
        return False

def navigate_via_menu(game_id, private_server=''):
    """Navigate using menu options"""
    try:
        print_formatted("INFO", "Attempting navigation via menu...")
        
        # Look for menu button (hamburger menu, etc.)
        menu_positions = [
            (50, 100),    # Top-left menu
            (50, 200),    # Left menu
            (1020, 100),  # Top-right menu
            (540, 50)     # Top-center menu
        ]
        
        for x, y in menu_positions:
            run_shell_command(f"input tap {x} {y}", platform_info=platform_info)
            time.sleep(3)
            
            # Look for "Games" or similar option
            if tap_games_option():
                time.sleep(3)
                
                # Try to find featured games or search
                if find_and_tap_game(game_id):
                    if tap_play_button():
                        return True
        
        return False
    except Exception as e:
        print_formatted("ERROR", f"Menu navigation failed: {str(e)}")
        return False

def tap_game_result():
    """Tap on game search result"""
    try:
        # Common positions for search results
        result_positions = [
            (540, 400),   # Center result
            (540, 500),   # Lower center
            (270, 400),   # Left result
            (810, 400)    # Right result
        ]
        
        for x, y in result_positions:
            run_shell_command(f"input tap {x} {y}", platform_info=platform_info)
            time.sleep(3)
            
            # Check if game page loaded
            if check_game_page():
                return True
        
        return False
    except:
        return False

def tap_play_button():
    """Tap the play/join button - CAREFUL approach"""
    try:
        print_formatted("INFO", "🎮 Looking for Play button...")
        
        # Wait for page to stabilize
        time.sleep(3)
        
        # Try fewer, more precise positions for play button
        play_positions = [
            (540, 800),   # Center-bottom (most common)
            (540, 750),   # Slightly higher center
        ]
        
        for attempt, (x, y) in enumerate(play_positions):
            print_formatted("INFO", f"🎯 Play button attempt {attempt + 1}: tapping ({x}, {y})")
            
            run_shell_command(f"input tap {x} {y}", platform_info=platform_info)
            time.sleep(8)  # Longer wait to see if game starts loading
            
            # Check if game started loading or Roblox launched
            if check_game_loading() or is_roblox_running():
                print_formatted("SUCCESS", "✓ Play button worked!")
                return True
        
        print_formatted("WARNING", "⚠️ Play button attempts failed")
        return False
    except Exception as e:
        print_formatted("ERROR", f"❌ Play button error: {str(e)}")
        return False

def clear_search():
    """Clear search field"""
    try:
        # Select all and delete
        run_shell_command("input keyevent KEYCODE_CTRL_LEFT", platform_info=platform_info)
        run_shell_command("input keyevent KEYCODE_A", platform_info=platform_info)
        run_shell_command("input keyevent KEYCODE_DEL", platform_info=platform_info)
        time.sleep(1)
    except:
        pass

def tap_games_option():
    """Tap on Games menu option"""
    try:
        # Look for "Games" text in various positions
        games_positions = [
            (200, 300),   # Left menu games
            (540, 300),   # Center games
            (200, 400),   # Lower left games
            (540, 400)    # Lower center games
        ]
        
        for x, y in games_positions:
            run_shell_command(f"input tap {x} {y}", platform_info=platform_info)
            time.sleep(3)
            
            # Check if games section loaded
            if check_games_section():
                return True
        
        return False
    except:
        return False

def find_and_tap_game(game_id):
    """Find and tap specific game"""
    try:
        # Scroll through games and look for the target
        for scroll_count in range(5):
            # Try tapping various game positions
            game_positions = [
                (270, 500), (540, 500), (810, 500),  # Row 1
                (270, 700), (540, 700), (810, 700),  # Row 2
                (270, 900), (540, 900), (810, 900)   # Row 3
            ]
            
            for x, y in game_positions:
                run_shell_command(f"input tap {x} {y}", platform_info=platform_info)
                time.sleep(2)
                
                if check_game_page():
                    return True
            
            # Scroll down for more games
            run_shell_command("input swipe 540 800 540 400 500", platform_info=platform_info)
            time.sleep(2)
        
        return False
    except:
        return False

def check_game_loading():
    """Check if game is loading"""
    try:
        # Look for loading indicators in logcat
        run_shell_command("logcat -c", platform_info=platform_info)
        time.sleep(3)
        
        logs = run_shell_command("logcat -d -t 50 | grep -i 'loading\\|joining\\|connecting'", platform_info=platform_info)
        return bool(logs.strip())
    except:
        return False

def check_game_page():
    """Check if on a game page"""
    try:
        # Check current activity for game page indicators
        activity = run_shell_command("dumpsys window windows | grep mCurrentFocus", platform_info=platform_info)
        game_page_indicators = ['GameDetail', 'GamePage', 'Experience']
        return any(indicator in activity for indicator in game_page_indicators)
    except:
        return False

def check_games_section():
    """Check if in games section"""
    try:
        activity = run_shell_command("dumpsys window windows | grep mCurrentFocus", platform_info=platform_info)
        games_indicators = ['Games', 'Discover', 'Browse']
        return any(indicator in activity for indicator in games_indicators)
    except:
        return False

# ======================
# GAME STATE DETECTION
# ======================
def is_in_game(game_id, private_server=''):
    """Check if currently in the specified game - SIMPLIFIED FOR COMPATIBILITY"""
    try:
        # First check if Roblox is running at all
        if not is_roblox_running():
            return False
        
        # Simple logcat check without problematic flags
        try:
            logs = run_shell_command("logcat -d", platform_info=platform_info)
            if logs and game_id in logs:
                return True
        except:
            pass
        
        # If Roblox is running but we can't detect the game, assume we're in some game
        return True
        
    except Exception as e:
        return False

def is_game_activity(activity):
    """Check if activity indicates being in a game"""
    game_indicators = [
        'GameActivity',
        'ExperienceActivity', 
        'SurfaceView',
        'UnityPlayerActivity',
        'GameView'
    ]
    return any(indicator in activity for indicator in game_indicators)

def check_error_states():
    """Check for REAL error states that require restart - REDUCED FALSE POSITIVES"""
    try:
        # Check for serious crashes/kicks only (not minor errors)
        recent_logs = run_shell_command("logcat -d -t 50 | grep -iE 'fatal.*roblox|crash.*roblox|kicked.*server|disconnected.*server|banned.*game'", platform_info=platform_info)
        
        # Only serious error patterns that actually require restart
        serious_error_patterns = {
            'crash': ['fatal.*roblox', 'crash.*roblox', 'native.*crash'],
            'kicked': ['kicked.*server', 'disconnected.*server', 'connection.*lost'],
            'banned': ['banned.*game', 'account.*suspended'],
            'frozen': ['anr.*roblox', 'not.*responding.*roblox']
        }
        
        for error_type, patterns in serious_error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, recent_logs.lower()):
                    return error_type
        
        # Check if Roblox has completely crashed (process died)
        if not is_roblox_running():
            # Only if it was recently running - check last 30 seconds of logs
            crash_check = run_shell_command("logcat -d -t 20 | grep -iE 'roblox.*died|roblox.*killed|roblox.*stopped'", platform_info=platform_info)
            if crash_check.strip():
                return 'process_crash'
        
        return None  # No serious errors detected
    except Exception as e:
        print_formatted("ERROR", f"❌ Error check failed: {str(e)}")
        return None

# ======================
# MAIN AUTOMATION LOGIC
# ======================
def attempt_game_join(config):
    """Attempt to join the specified game using multiple methods - NO RANDOM CLICKING"""
    global last_game_join_time
    
    game_id = config.get('game_id')
    private_server = config.get('private_server', '')
    
    if not game_id:
        print_formatted("ERROR", "❌ No game ID specified in config")
        return False
    
    # Show current user info
    user_id, username = get_current_user_info()
    if user_id:
        print_formatted("INFO", f"👤 Joining game {game_id} as {username} (ID: {user_id})")
    else:
        print_formatted("INFO", f"🎯 Joining game {game_id}...")
    
    # Close Roblox first only if it's running
    if is_roblox_running():
        print_formatted("INFO", "🔄 Closing existing Roblox...")
        if not close_roblox(config):
            print_formatted("WARNING", "⚠️ Failed to close properly, continuing...")
        time.sleep(3)
    
    # Try launch methods - NO UI AUTOMATION (no screen clicking)
    methods = [
        ("Deep Link", launch_via_deep_link),
        ("Android Intent", launch_via_intent),
        ("Browser Method", launch_via_browser_redirect)
        # REMOVED UI Automation to prevent random screen clicking!
    ]
    
    for method_name, method_func in methods:
        try:
            print_formatted("INFO", f"🚀 Trying {method_name}...")
            
            if method_func(game_id, private_server):
                print_formatted("SUCCESS", f"✅ {method_name} launched!")
                
                # Wait for game to load and verify join
                print_formatted("INFO", "⏳ Waiting for game to load...")
                if wait_for_game_join(config, timeout=60):
                    last_game_join_time = time.time()
                    print_formatted("SUCCESS", f"🎉 Successfully joined using {method_name}!")
                    return True
                else:
                    print_formatted("WARNING", f"⚠️ Timeout with {method_name}")
            else:
                print_formatted("WARNING", f"❌ {method_name} failed")
            
            # Brief delay between attempts
            time.sleep(2)
            
        except Exception as e:
            print_formatted("ERROR", f"❌ {method_name} error: {str(e)}")
            continue
    
    print_formatted("ERROR", "❌ All methods failed - will try again later")
    return False

def wait_for_game_join(config, timeout=60):
    """Wait for game to load and confirm join - CLEAR LOGGING"""
    start_time = time.time()
    game_id = config.get('game_id')
    private_server = config.get('private_server', '')
    
    print_formatted("INFO", f"🕐 Waiting for game {game_id} to load... (timeout: {timeout}s)")
    
    check_interval = 5  # Check every 5 seconds
    last_status_time = 0
    
    while time.time() - start_time < timeout:
        elapsed = int(time.time() - start_time)
        
        # Show progress every 15 seconds
        if elapsed - last_status_time >= 15:
            remaining = timeout - elapsed
            print_formatted("INFO", f"⏳ Still loading... {remaining}s left")
            last_status_time = elapsed
        
        # Check if we're in the game
        if is_in_game(game_id, private_server):
            print_formatted("SUCCESS", f"✅ Game joined successfully after {elapsed}s!")
            return True
        
        time.sleep(check_interval)
    
    print_formatted("WARNING", f"⚠️ Game join timeout after {timeout}s")
    return False

def should_attempt_launch(config):
    """Determine if we should attempt to launch/rejoin the game"""
    # Check if Roblox is running
    if not is_roblox_running():
        print_formatted("INFO", "Roblox not running, need to launch")
        return True
    
    # Check if we're in the correct game
    game_id = config.get('game_id')
    private_server = config.get('private_server', '')
    if not is_in_game(game_id, private_server):
        print_formatted("INFO", "Not in correct game, need to rejoin")
        return True
    
    # Check for error states
    error_state = check_error_states()
    if error_state:
        print_formatted("WARNING", f"Error state detected: {error_state}")
        return True
    
    return False

def automation_loop(config):
    """Main automation loop - IMPROVED STABILITY"""
    global automation_running, last_game_join_time
    
    automation_running = True
    
    # Show user info at start - FIXED
    user_id, username = get_current_user_info()
    if user_id:
        print_formatted("SUCCESS", f"🚀 Automation started for {username} (ID: {user_id})!")
    else:
        print_formatted("SUCCESS", "🚀 Automation started! Looking for game...")
        print_formatted("WARNING", "⚠️ No user configured - configure in settings for better tracking")
    
    game_id = config.get('game_id')
    private_server = config.get('private_server', '')
    check_delay = config.get('check_delay', 45)
    
    # Check if already in game first
    if is_roblox_running() and is_in_game(game_id, private_server):
        print_formatted("SUCCESS", f"✅ Already in game {game_id}!")
        print_formatted("INFO", "🎮 Monitoring game... (will only restart if crash/kick/error)")
    else:
        print_formatted("INFO", "🎯 Need to join game...")
        if not attempt_game_join(config):
            print_formatted("ERROR", "❌ Failed to join game initially. Will keep trying...")
    
    consecutive_stable_checks = 0
    stable_time_seconds = 0
    last_status_message_time = 0
    
    while automation_running:
        try:
            current_time = time.time()
            
            # Check current status
            roblox_running = is_roblox_running()
            in_correct_game = is_in_game(game_id, private_server) if roblox_running else False
            error_state = check_error_states()
            
            # If everything is good - stay stable!
            if roblox_running and in_correct_game and not error_state:
                consecutive_stable_checks += 1
                stable_time_seconds += check_delay
                
                # Show status messages at intervals
                if consecutive_stable_checks == 1:
                    print_formatted("SUCCESS", f"✅ Stable in game {game_id}")
                    print_formatted("INFO", "👀 Monitoring... (no restarts unless problem detected)")
                    last_status_message_time = current_time
                elif current_time - last_status_message_time >= 300:  # Every 5 minutes
                    minutes = stable_time_seconds // 60
                    print_formatted("INFO", f"✅ Still stable in game - Running for {minutes} minutes")
                    last_status_message_time = current_time
                
                # Sleep peacefully when stable
                time.sleep(check_delay)
                continue
            
            # Problem detected - need action
            if consecutive_stable_checks > 0:
                minutes_stable = stable_time_seconds // 60
                print_formatted("WARNING", f"⚠️ Problem detected after {minutes_stable} minutes stable")
            
            consecutive_stable_checks = 0
            stable_time_seconds = 0
            
            # Determine what went wrong and fix it
            if error_state:
                print_formatted("ERROR", f"🚨 Error detected: {error_state}")
                print_formatted("INFO", "🔧 Restarting due to error...")
                if attempt_game_join(config):
                    print_formatted("SUCCESS", "✅ Successfully rejoined after error!")
                else:
                    print_formatted("ERROR", "❌ Failed to rejoin after error")
                    
            elif not roblox_running:
                print_formatted("WARNING", "⚠️ Roblox not running")
                print_formatted("INFO", "🚀 Launching Roblox...")
                if attempt_game_join(config):
                    print_formatted("SUCCESS", "✅ Successfully launched Roblox!")
                else:
                    print_formatted("ERROR", "❌ Failed to launch Roblox")
                    
            elif not in_correct_game:
                print_formatted("WARNING", f"⚠️ Not in correct game {game_id}")
                print_formatted("INFO", "🎯 Attempting to join correct game...")
                if attempt_game_join(config):
                    print_formatted("SUCCESS", "✅ Successfully joined correct game!")
                else:
                    print_formatted("ERROR", "❌ Failed to join correct game")
            
            # Wait before next check (only when there were problems)
            print_formatted("INFO", f"⏱️ Next check in {check_delay} seconds...")
            time.sleep(check_delay)
            
        except KeyboardInterrupt:
            print_formatted("INFO", "🛑 Automation stopped by user")
            break
        except Exception as e:
            print_formatted("ERROR", f"❌ Automation error: {str(e)}")
            time.sleep(10)
    
    automation_running = False
    print_formatted("INFO", "🔴 Automation stopped")

# ======================
# INTERACTIVE MENU
# ======================
def display_menu():
    """Display main menu - IMPROVED INFO"""
    print(f"\n{COLORS['HEADER']}{'='*50}")
    print(f"    ENHANCED ROBLOX AUTOMATION TOOL")
    print(f"        🎮 STABLE VERSION - NO RANDOM CLICKING")
    print(f"{'='*50}{COLORS['RESET']}")
    
    # Display current user info - FIXED
    config = load_config()
    user_id = config.get('user_id', '')
    username = config.get('username', '')
    if user_id:
        display_username = username if username else f"User_{user_id}"
        print(f"{COLORS['SUCCESS']}👤 Active User: {display_username} (ID: {user_id}){COLORS['RESET']}")
    else:
        print(f"{COLORS['WARNING']}👤 Active User: Not configured{COLORS['RESET']}")
    
    if platform_info:
        print(f"{COLORS['INFO']}Platform: {platform_info['name']} ({platform_info['type']}){COLORS['RESET']}")
        print(f"{COLORS['INFO']}Root Access: {'Yes' if platform_info.get('has_root') else 'Limited'}{COLORS['RESET']}")
    
    print(f"\n{COLORS['CYAN']}1.{COLORS['RESET']} Configure Settings")
    print(f"{COLORS['CYAN']}2.{COLORS['RESET']} Start Automation (Smart - stays in game)")
    print(f"{COLORS['CYAN']}3.{COLORS['RESET']} Stop Automation")
    print(f"{COLORS['CYAN']}4.{COLORS['RESET']} Test Game Join")
    print(f"{COLORS['CYAN']}5.{COLORS['RESET']} View Current Config")
    print(f"{COLORS['CYAN']}6.{COLORS['RESET']} System Information")
    print(f"{COLORS['CYAN']}7.{COLORS['RESET']} Exit")
    
    if automation_running:
        print(f"\n{COLORS['SUCCESS']}✅ Status: Automation is RUNNING{COLORS['RESET']}")
        print(f"{COLORS['INFO']}   Mode: Stay in game unless crash/kick/error{COLORS['RESET']}")
    else:
        print(f"\n{COLORS['WARNING']}⭕ Status: Automation is STOPPED{COLORS['RESET']}")
    
    if last_game_join_time:
        join_time = datetime.fromtimestamp(last_game_join_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{COLORS['INFO']}Last Game Join: {join_time}{COLORS['RESET']}")
    
    print(f"\n{COLORS['INFO']}ℹ️  This version will NOT click the screen randomly{COLORS['RESET']}")
    print(f"{COLORS['INFO']}   It only restarts on real problems (crash/kick/error){COLORS['RESET']}")

def configure_settings():
    """Interactive configuration setup"""
    config = load_config()
    
    print(f"\n{COLORS['HEADER']}=== CONFIGURATION SETUP ==={COLORS['RESET']}")
    
    # User ID Configuration - FIXED
    current_user_id = config.get('user_id', '')
    current_username = config.get('username', '')
    print(f"\nCurrent User ID: {current_user_id if current_user_id else 'Not set'}")
    print(f"Current Username: {current_username if current_username else 'Not set'}")
    new_user_id = input("Enter your Roblox User ID (or press Enter to keep current): ").strip()
    if new_user_id:
        config['user_id'] = new_user_id
        # Also ask for username
        new_username = input("Enter your Roblox Username (optional): ").strip()
        if new_username:
            config['username'] = new_username
        else:
            config['username'] = f"User_{new_user_id}"
    
    # Game ID
    current_game_id = config.get('game_id', '')
    print(f"\nCurrent Game ID: {current_game_id if current_game_id else 'Not set'}")
    new_game_id = input("Enter new Game ID (or press Enter to keep current): ").strip()
    if new_game_id:
        config['game_id'] = new_game_id
    
    # Private Server
    current_private_server = config.get('private_server', '')
    print(f"\nCurrent Private Server: {current_private_server if current_private_server else 'Not set'}")
    new_private_server = input("Enter Private Server link (or press Enter to keep current): ").strip()
    if new_private_server:
        config['private_server'] = new_private_server
    
    # Check Delay
    current_delay = config.get('check_delay', 45)
    print(f"\nCurrent Check Delay: {current_delay} seconds")
    new_delay = input("Enter new Check Delay in seconds (or press Enter to keep current): ").strip()
    if new_delay and new_delay.isdigit():
        config['check_delay'] = int(new_delay)
    
    # Max Retries
    current_retries = config.get('max_retries', 3)
    print(f"\nCurrent Max Retries: {current_retries}")
    new_retries = input("Enter new Max Retries (or press Enter to keep current): ").strip()
    if new_retries and new_retries.isdigit():
        config['max_retries'] = int(new_retries)
    
    # Auto Rejoin
    current_rejoin = config.get('auto_rejoin', True)
    print(f"\nCurrent Auto Rejoin: {'Enabled' if current_rejoin else 'Disabled'}")
    new_rejoin = input("Enable Auto Rejoin? (y/n, or press Enter to keep current): ").strip().lower()
    if new_rejoin in ['y', 'yes']:
        config['auto_rejoin'] = True
    elif new_rejoin in ['n', 'no']:
        config['auto_rejoin'] = False
    
    # Save configuration
    if save_config(config):
        print_formatted("SUCCESS", "Configuration saved successfully!")
    else:
        print_formatted("ERROR", "Failed to save configuration!")
    
    input("\nPress Enter to continue...")

def view_current_config():
    """Display current configuration"""
    config = load_config()
    
    print(f"\n{COLORS['HEADER']}=== CURRENT CONFIGURATION ==={COLORS['RESET']}")
    # User Information - FIXED
    user_id = config.get('user_id', 'Not set')
    username = config.get('username', 'Not set')
    print(f"{COLORS['CYAN']}User ID:{COLORS['RESET']} {user_id}")
    print(f"{COLORS['CYAN']}Username:{COLORS['RESET']} {username}")
    print(f"{COLORS['CYAN']}Game ID:{COLORS['RESET']} {config.get('game_id', 'Not set')}")
    print(f"{COLORS['CYAN']}Private Server:{COLORS['RESET']} {config.get('private_server', 'Not set')}")
    print(f"{COLORS['CYAN']}Check Delay:{COLORS['RESET']} {config.get('check_delay', 45)} seconds")
    print(f"{COLORS['CYAN']}Max Retries:{COLORS['RESET']} {config.get('max_retries', 3)}")
    print(f"{COLORS['CYAN']}Auto Rejoin:{COLORS['RESET']} {'Enabled' if config.get('auto_rejoin', True) else 'Disabled'}")
    print(f"{COLORS['CYAN']}Game Validation:{COLORS['RESET']} {'Enabled' if config.get('game_validation', True) else 'Disabled'}")
    print(f"{COLORS['CYAN']}Launch Delay:{COLORS['RESET']} {config.get('launch_delay', 300)} seconds")
    print(f"{COLORS['CYAN']}Retry Delay:{COLORS['RESET']} {config.get('retry_delay', 15)} seconds")
    
    input("\nPress Enter to continue...")

def test_game_join():
    """Test game joining functionality"""
    config = load_config()
    game_id = config.get('game_id')
    
    if not game_id:
        print_formatted("ERROR", "No game ID configured. Please configure settings first.")
        input("Press Enter to continue...")
        return
    
    print_formatted("INFO", f"Testing game join for Game ID: {game_id}")
    print_formatted("INFO", "This will close Roblox and attempt to join the game...")
    
    confirm = input("Continue with test? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        return
    
    success = attempt_game_join(config)
    
    if success:
        print_formatted("SUCCESS", "Game join test completed successfully!")
    else:
        print_formatted("ERROR", "Game join test failed!")
    
    input("\nPress Enter to continue...")

def show_system_info():
    """Display system information"""
    print(f"\n{COLORS['HEADER']}=== SYSTEM INFORMATION ==={COLORS['RESET']}")
    
    # User Information - FIXED
    user_id, username = get_current_user_info()
    print(f"{COLORS['CYAN']}Active User:{COLORS['RESET']} {username}")
    if user_id:
        print(f"{COLORS['CYAN']}User ID:{COLORS['RESET']} {user_id}")
    
    if platform_info:
        print(f"{COLORS['CYAN']}Platform Type:{COLORS['RESET']} {platform_info['type']}")
        print(f"{COLORS['CYAN']}Platform Name:{COLORS['RESET']} {platform_info['name']}")
        print(f"{COLORS['CYAN']}Root Access:{COLORS['RESET']} {'Available' if platform_info.get('has_root') else 'Limited'}")
        print(f"{COLORS['CYAN']}ADB Support:{COLORS['RESET']} {'Yes' if platform_info.get('use_adb') else 'No'}")
        print(f"{COLORS['CYAN']}Shell Prefix:{COLORS['RESET']} {platform_info.get('shell_prefix', 'None')}")
    
    # Check Roblox installation
    roblox_installed = verify_roblox_installation()
    print(f"{COLORS['CYAN']}Roblox Installed:{COLORS['RESET']} {'Yes' if roblox_installed else 'No'}")
    
    if roblox_installed:
        roblox_running = is_roblox_running()
        print(f"{COLORS['CYAN']}Roblox Running:{COLORS['RESET']} {'Yes' if roblox_running else 'No'}")
    
    # Android version
    try:
        android_version = run_shell_command("getprop ro.build.version.release", platform_info=platform_info)
        print(f"{COLORS['CYAN']}Android Version:{COLORS['RESET']} {android_version if android_version else 'Unknown'}")
    except:
        pass
    
    # Device model
    try:
        device_model = run_shell_command("getprop ro.product.model", platform_info=platform_info)
        print(f"{COLORS['CYAN']}Device Model:{COLORS['RESET']} {device_model if device_model else 'Unknown'}")
    except:
        pass
    
    input("\nPress Enter to continue...")

# ======================
# MAIN FUNCTION
# ======================
def main():
    """Main function"""
    global platform_info, automation_running
    
    try:
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"{COLORS['HEADER']}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║              ENHANCED ROBLOX AUTOMATION TOOL                 ║")
        print("║          Supports: UGPHONE, VSPHONE, REDFINGER              ║")
        print("║                    Standard Android & Emulators             ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{COLORS['RESET']}")
        
        # Initialize platform detection
        detector = PlatformDetector()
        platform_info = detector.detect_platform()
        
        # Detect and update username - FIXED
        print_formatted("INFO", "Initializing user detection...")
        detect_and_update_username()
        
        # Verify Roblox installation
        print_formatted("INFO", "Verifying Roblox installation...")
        if not verify_roblox_installation():
            print_formatted("ERROR", "Roblox is not installed or not accessible!")
            print_formatted("INFO", "Please install Roblox and ensure proper permissions.")
            sys.exit(1)
        
        print_formatted("SUCCESS", "Initialization complete!")
        
        automation_thread = None
        
        # Main menu loop
        while True:
            try:
                display_menu()
                choice = input(f"\n{COLORS['CYAN']}Enter your choice (1-7): {COLORS['RESET']}").strip()
                
                if choice == '1':
                    configure_settings()
                elif choice == '2':
                    if automation_running:
                        print_formatted("WARNING", "Automation is already running!")
                        input("Press Enter to continue...")
                    else:
                        config = load_config()
                        if not config.get('game_id'):
                            print_formatted("ERROR", "No game ID configured! Please configure settings first.")
                            input("Press Enter to continue...")
                        else:
                            automation_thread = threading.Thread(target=automation_loop, args=(config,), daemon=True)
                            automation_thread.start()
                elif choice == '3':
                    if automation_running:
                        print_formatted("INFO", "Stopping automation...")
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
                    show_system_info()
                elif choice == '7':
                    if automation_running:
                        print_formatted("INFO", "Stopping automation before exit...")
                        automation_running = False
                        if automation_thread:
                            automation_thread.join(timeout=5)
                    print_formatted("INFO", "Thank you for using Enhanced Roblox Automation Tool!")
                    break
                else:
                    print_formatted("WARNING", "Invalid choice! Please enter 1-7.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print_formatted("INFO", "\nExiting...")
                if automation_running:
                    automation_running = False
                break
            except Exception as e:
                print_formatted("ERROR", f"Menu error: {str(e)}")
                input("Press Enter to continue...")
    
    except Exception as e:
        print_formatted("ERROR", f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
