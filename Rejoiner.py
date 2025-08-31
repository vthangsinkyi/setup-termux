#!/usr/bin/env python3
"""
Enhanced Roblox Automation Tool (Rejoiner.py)
Supports: UGPHONE, VSPHONE, REDFINGER, Standard Android/Emulators
Author: Optimized for game monitoring and private server joining
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
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/sdcard/roblox_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Rejoiner")

# Configuration
COLORS = {
    "RESET": "\033[0m",
    "INFO": "\033[94m",
    "SUCCESS": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "BOLD": "\033[1m",
    "CYAN": "\033[96m",
    "HEADER": "\033[95m",
    "DEBUG": "\033[90m"
}

CONFIG_FILE = "/sdcard/roblox_config.json"
ROBLOX_PACKAGE = "com.roblox.client"
BROWSER_PACKAGES = [
    "com.android.chrome",
    "com.sec.android.app.sbrowser",
    "com.google.android.webview",
    "org.mozilla.firefox",
    "com.opera.browser",
    "com.brave.browser",
    "com.microsoft.emmx",
    "com.vivaldi.browser"
]

# Roblox Error Code Database
ROBLOX_ERROR_DATABASE = {
    "267": {"name": "Cannot rejoin game", "solution": "Wait 30 seconds before retry", "wait_time": 30},
    "279": {"name": "Server full", "solution": "Try different server or wait", "wait_time": 15},
    "292": {"name": "Kicked from game", "solution": "Check if banned, wait 5 minutes", "wait_time": 300},
    "529": {"name": "Connection lost", "solution": "Check network, restart if persistent", "wait_time": 10},
    "601": {"name": "Place unavailable", "solution": "Game might be updating, check later", "wait_time": 60}
}

# Global variables
automation_running = False
platform_info = None
last_game_join_time = None
error_codes_detected = set()
consecutive_failures = 0
last_error_time = 0
last_game_verification_time = 0  # Track when we last verified we're in the correct game

# Platform Detection
class PlatformDetector:
    def __init__(self):
        self.detected_platform = None
   
    def detect_platform(self) -> Dict[str, Any]:
        try:
            # Enhanced UGPHONE detection
            if self._is_ugphone():
                self.detected_platform = {
                    'type': 'ugphone',
                    'name': 'UGPHONE',
                    'has_root': self._check_root_ugphone(),
                    'use_adb': False,
                    'shell_prefix': '',
                    'special_commands': True,
                    'process_check_method': 'ps_grep',
                    'browser_launch': 'intent'
                }
                print_formatted("INFO", f"Platform detected: {self.detected_platform['name']}")
                return self.detected_platform
           
            # Enhanced VSPHONE detection
            if self._is_vsphone():
                self.detected_platform = {
                    'type': 'vsphone',
                    'name': 'VSPHONE',
                    'has_root': self._check_root_vsphone(),
                    'use_adb': False,
                    'shell_prefix': '',
                    'special_commands': True,
                    'process_check_method': 'ps_grep',
                    'browser_launch': 'intent'
                }
                print_formatted("INFO", f"Platform detected: {self.detected_platform['name']}")
                return self.detected_platform
           
            # Enhanced REDFINGER detection
            if self._is_redfinger():
                self.detected_platform = {
                    'type': 'redfinger',
                    'name': 'REDFINGER',
                    'has_root': self._check_root_redfinger(),
                    'use_adb': True,
                    'shell_prefix': 'su -c',
                    'special_commands': False,
                    'process_check_method': 'pidof',
                    'browser_launch': 'intent'
                }
                print_formatted("INFO", f"Platform detected: {self.detected_platform['name']}")
                return self.detected_platform
           
            # Standard Android/Emulator
            self.detected_platform = {
                'type': 'standard',
                'name': 'Standard Android',
                'has_root': self._check_root_standard(),
                'use_adb': True,
                'shell_prefix': 'su -c',
                'special_commands': False,
                'process_check_method': 'pidof',
                'browser_launch': 'intent'
            }
            print_formatted("INFO", f"Platform detected: {self.detected_platform['name']}")
            return self.detected_platform
           
        except Exception as e:
            print_formatted("ERROR", f"Platform detection error: {str(e)}")
            # Fallback to standard Android with limited functionality
            self.detected_platform = {
                'type': 'standard',
                'name': 'Standard Android (Fallback)',
                'has_root': False,
                'use_adb': False,
                'shell_prefix': '',
                'special_commands': False,
                'process_check_method': 'ps_grep',
                'browser_launch': 'intent'
            }
            return self.detected_platform
   
    def _is_ugphone(self) -> bool:
        try:
            # Check for UGPHONE specific indicators
            indicators = [
                '/system/bin/ugphone', '/system/app/UGPhone', '/data/local/tmp/ugphone',
                '/system/priv-app/UGPhone', '/system/framework/ugphone.jar',
                '/system/etc/ugphone', '/vendor/bin/ugphone', '/system/bin/ug_phone'
            ]
            
            # Check files
            for indicator in indicators:
                if os.path.exists(indicator):
                    return True
            
            # Check build properties
            build_info = self._get_build_prop()
            ugphone_patterns = ['ugphone', 'ug_phone', 'cloudphone', 'universal.global.phone', 'ugcloud']
            for pattern in ugphone_patterns:
                if pattern.lower() in build_info.lower():
                    return True
                    
            # Check environment
            env_vars = self._get_env_vars()
            if any('ugphone' in var.lower() for var in env_vars):
                return True
                
            # Check processes
            processes = self._get_running_processes()
            if any('ugphone' in proc.lower() for proc in processes):
                return True
                
            return False
        except:
            return False
   
    def _is_vsphone(self) -> bool:
        try:
            # Check for VSPHONE specific indicators
            indicators = [
                '/system/bin/vsphone', '/system/app/VSPhone', '/data/local/tmp/vsphone',
                '/system/priv-app/VSPhone', '/system/framework/vsphone.jar',
                '/system/etc/vsphone', '/vendor/bin/vsphone', '/system/bin/vs_phone'
            ]
            
            for indicator in indicators:
                if os.path.exists(indicator):
                    return True
            
            # Check build properties
            build_info = self._get_build_prop()
            vsphone_patterns = ['vsphone', 'vs_phone', 'virtualphone', 'virtual.space', 'vspace']
            for pattern in vsphone_patterns:
                if pattern.lower() in build_info.lower():
                    return True
                    
            # Check environment
            env_vars = self._get_env_vars()
            if any('vsphone' in var.lower() for var in env_vars):
                return True
                
            # Check processes
            processes = self._get_running_processes()
            if any('vsphone' in proc.lower() for proc in processes):
                return True
                
            return False
        except:
            return False
   
    def _is_redfinger(self) -> bool:
        try:
            # Check for REDFINGER specific indicators
            indicators = [
                '/system/bin/redfinger', '/system/app/RedFinger', '/data/local/tmp/redfinger',
                '/system/priv-app/RedFinger', '/system/framework/redfinger.jar',
                '/system/etc/redfinger', '/vendor/bin/redfinger', '/system/bin/red_finger'
            ]
            
            for indicator in indicators:
                if os.path.exists(indicator):
                    return True
            
            # Check build properties
            build_info = self._get_build_prop()
            redfinger_patterns = ['redfinger', 'red_finger', 'redcloud', 'red.finger', 'rfcloud']
            for pattern in redfinger_patterns:
                if pattern.lower() in build_info.lower():
                    return True
                    
            # Check environment
            env_vars = self._get_env_vars()
            if any('redfinger' in var.lower() for var in env_vars):
                return True
                
            # Check processes
            processes = self._get_running_processes()
            if any('redfinger' in proc.lower() for proc in processes):
                return True
                
            return False
        except:
            return False
   
    def _get_build_prop(self) -> str:
        try:
            result = subprocess.run(['cat', '/system/build.prop'],
                                  capture_output=True, text=True, timeout=5)
            return result.stdout
        except:
            return ""
    
    def _get_env_vars(self) -> List[str]:
        try:
            result = subprocess.run(['env'],
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.split('\n')
        except:
            return []
    
    def _get_running_processes(self) -> List[str]:
        try:
            result = subprocess.run(['ps', '-A'],
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.split('\n')
        except:
            return []
   
    def _check_root_standard(self) -> bool:
        try:
            result = subprocess.run(['su', '-c', 'echo test'],
                                  capture_output=True, text=True, timeout=5)
            return 'test' in result.stdout
        except:
            return False
   
    def _check_root_ugphone(self) -> bool:
        try:
            if self._check_root_standard():
                return True
            result = subprocess.run(['ugphone_su', '-c', 'echo test'],
                                  capture_output=True, text=True, timeout=5)
            return 'test' in result.stdout
        except:
            return False
   
    def _check_root_vsphone(self) -> bool:
        try:
            if self._check_root_standard():
                return True
            result = subprocess.run(['vsphone_su', '-c', 'echo test'],
                                  capture_output=True, text=True, timeout=5)
            return 'test' in result.stdout
        except:
            return False
            
    def _check_root_redfinger(self) -> bool:
        try:
            if self._check_root_standard():
                return True
            result = subprocess.run(['redfinger_su', '-c', 'echo test'],
                                  capture_output=True, text=True, timeout=5)
            return 'test' in result.stdout
        except:
            return False

# Core Functions
def print_formatted(level: str, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = {
        "INFO": "INFO",
        "SUCCESS": "OK",
        "WARNING": "WARN",
        "ERROR": "ERROR",
        "HEADER": "====",
        "DEBUG": "DEBUG"
    }.get(level, level)
    
    color = COLORS.get(level, COLORS["RESET"])
    print(f"{color}{timestamp} [{prefix}] {message}{COLORS['RESET']}")
    logger.log(
        getattr(logging, level.upper(), logging.INFO),
        message
    )

def run_shell_command(command: str, timeout: int = 10, platform_info: Optional[Dict] = None) -> str:
    try:
        if platform_info and platform_info.get('shell_prefix'):
            if platform_info['shell_prefix']:
                full_command = platform_info['shell_prefix'].split() + [command]
            else:
                full_command = command.split()
        else:
            full_command = command.split()
            
        result = subprocess.run(full_command, capture_output=True, text=True, timeout=timeout)
        
        if result.stderr and "permission denied" not in result.stderr.lower():
            print_formatted("DEBUG", f"Command stderr: {result.stderr.strip()}")
        
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print_formatted("WARNING", f"Command timeout: {command}")
        return ""
    except Exception as e:
        print_formatted("ERROR", f"Command failed: {command} - {str(e)}")
        return ""

def load_config() -> Dict[str, Any]:
    default_config = {
        "accounts": [],
        "game_id": "",
        "private_server": "",
        "check_delay": 60,  # Changed from 45 to 60 seconds
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
        "verbose_logging": True,
        "browser_preference": "auto",
        "error_detection": True,
        "performance_mode": False,
        "game_load_delay": 90,  # Added: Wait 90 seconds before checking if in game
        "game_verification_interval": 300,  # Added: Check every 5 minutes if still in correct game
        "error_wait_times": {
            "267": 30,
            "279": 15,
            "292": 300,
            "529": 10,
            "601": 60
        }
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
            # Merge with default config to ensure all keys exist
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    except Exception as e:
        print_formatted("ERROR", f"Config load error: {e}")
        return default_config

def save_config(config: Dict[str, Any]) -> bool:
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        run_shell_command(f"chmod 644 {CONFIG_FILE}", platform_info=platform_info)
        print_formatted("SUCCESS", "Config saved")
        return True
    except Exception as e:
        print_formatted("ERROR", f"Config save error: {e}")
        return False

# Roblox Control Functions
def verify_roblox_installation() -> bool:
    try:
        output = run_shell_command(f"pm list packages {ROBLOX_PACKAGE}", platform_info=platform_info)
        if ROBLOX_PACKAGE not in output:
            print_formatted("ERROR", "Roblox not installed.")
            return False
            
        version_output = run_shell_command(f"dumpsys package {ROBLOX_PACKAGE} | grep versionName", platform_info=platform_info)
        if version_output:
            version = version_output.split("versionName=")[1].split()[0] if "versionName=" in version_output else "Unknown"
            print_formatted("INFO", f"Roblox version: {version}")
            
        return True
    except Exception as e:
        print_formatted("ERROR", f"Roblox verification error: {e}")
        return False

def is_roblox_running(retries: int = 2, delay: int = 1) -> bool:
    for i in range(retries):
        try:
            # Use platform-specific process checking method
            if platform_info and platform_info.get('process_check_method') == 'ps_grep':
                # Use ps + grep for cloud phone services
                process_check = run_shell_command(f"ps -A | grep {ROBLOX_PACKAGE} | grep -v grep", platform_info=platform_info)
                if process_check.strip():
                    print_formatted("DEBUG", "Roblox process found via ps+grep")
                    return True
            else:
                # Use pidof for standard Android
                pid_check = run_shell_command(f"pidof {ROBLOX_PACKAGE}", platform_info=platform_info)
                if pid_check.strip():
                    print_formatted("DEBUG", "Roblox PID found via pidof")
                    return True

            # Additional checks for all platforms
            # Check activity state
            activity_info = run_shell_command("dumpsys activity | grep -A 10 -B 5 'mResumedActivity'", platform_info=platform_info)
            if ROBLOX_PACKAGE in activity_info and 'mResumedActivity' in activity_info:
                print_formatted("DEBUG", "Roblox is resumed and focused")
                return True
                
            # Check for any Roblox-related processes
            all_processes = run_shell_command("ps -A", platform_info=platform_info)
            if ROBLOX_PACKAGE in all_processes:
                print_formatted("DEBUG", "Roblox process found in all processes list")
                return True

            if i < retries - 1:
                time.sleep(delay)
                
        except Exception as e:
            print_formatted("ERROR", f"Roblox running check error: {str(e)}")
            if i < retries - 1:
                time.sleep(delay)

    print_formatted("DEBUG", "Roblox process not found")
    return False

def close_roblox(config: Optional[Dict] = None) -> bool:
    try:
        print_formatted("INFO", "Closing Roblox...")
        
        # First, try to go home to minimize the chance of UI interactions
        run_shell_command("input keyevent KEYCODE_HOME", platform_info=platform_info)
        time.sleep(2)
        
        # Try different methods to close Roblox
        run_shell_command(f"am force-stop {ROBLOX_PACKAGE}", platform_info=platform_info)
        time.sleep(2)
        
        # For cloud phone services, we might need different approaches
        if platform_info and platform_info['type'] in ['ugphone', 'vsphone', 'redfinger']:
            # Cloud phone services might need special handling
            run_shell_command(f"pkill -f {ROBLOX_PACKAGE}", platform_info=platform_info)
        else:
            # Standard Android
            run_shell_command(f"killall -9 {ROBLOX_PACKAGE}", platform_info=platform_info)
            
        force_kill_delay = config.get("force_kill_delay", 10) if config else 10
        time.sleep(force_kill_delay)
        
        if is_roblox_running():
            print_formatted("WARNING", "Roblox still running, clearing cache...")
            run_shell_command(f"pm clear {ROBLOX_PACKAGE}", platform_info=platform_info)
            time.sleep(5)
            
        success = not is_roblox_running()
        if success:
            print_formatted("SUCCESS", "Roblox closed successfully")
        else:
            print_formatted("ERROR", "Failed to close Roblox completely")
        return success
    except Exception as e:
        print_formatted("ERROR", f"Failed to close Roblox: {str(e)}")
        return False

def get_main_activity() -> str:
    try:
        output = run_shell_command(f"dumpsys package {ROBLOX_PACKAGE} | grep -A 5 'android.intent.action.MAIN'", platform_info=platform_info)
        match = re.search(r'com\.roblox\.client/(\.[A-Za-z0-9.]+)', output)
        if match:
            activity = match.group(1)
            print_formatted("DEBUG", f"Detected main activity: {activity}")
            return activity
            
        fallbacks = ['.startup.ActivitySplash', '.MainActivity', '.HomeActivity']
        for fallback in fallbacks:
            test_output = run_shell_command(f"dumpsys package {ROBLOX_PACKAGE} | grep {fallback}", platform_info=platform_info)
            if fallback in test_output:
                return fallback
                
        return '.MainActivity'
    except Exception as e:
        print_formatted("WARNING", f"Main activity detection error: {str(e)}")
        return '.MainActivity'

def build_game_url(game_id: str, private_server: str = '') -> str:
    try:
        if private_server:
            # Use the raw private server link as provided
            if not private_server.startswith(('http://', 'https://')):
                private_server = f"https://{private_server}"
            print_formatted("INFO", f"Using provided private server URL: {private_server}")
            return private_server
            
        # Fallback to deep link for public server
        url = f"roblox://experiences/start?placeId={game_id}"
        print_formatted("INFO", f"Built game deep link URL: {url}")
        return url
    except Exception as e:
        print_formatted("ERROR", f"URL build error: {e}")
        return f"roblox://experiences/start?placeId={game_id}"

def extract_private_server_code(link: str) -> Optional[str]:
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
                
        for separator in ['privateServerLinkCode=', 'share?code=', '&linkCode=', '=']:
            if separator in link:
                code = link.split(separator)[1].split('&')[0].strip()
                if code:
                    return code
                    
        return None
    except:
        return None

def get_available_browsers() -> List[str]:
    browsers = []
    for browser in BROWSER_PACKAGES:
        output = run_shell_command(f"pm list packages {browser}", platform_info=platform_info)
        if browser in output:
            browsers.append(browser)
    return browsers

# Game Launch Functions
def launch_via_deep_link(game_id: str, private_server: str = '') -> bool:
    try:
        if private_server:
            print_formatted("INFO", "Skipping deep link for private server, using browser method")
            return False
            
        print_formatted("INFO", f"Launching via deep link: Game ID {game_id}")
        url = build_game_url(game_id, private_server)
        command = f'am start -a android.intent.action.VIEW -d "{url}"'
        result = run_shell_command(command, platform_info=platform_info)
        
        # Wait for Roblox to start with more frequent checks
        start_time = time.time()
        while time.time() - start_time < 120:  # Wait up to 2 minutes
            if is_roblox_running():
                print_formatted("SUCCESS", "Roblox launched via deep link")
                # Wait a bit longer for the game to fully load
                time.sleep(10)
                return True
            time.sleep(3)
            
        print_formatted("WARNING", "Deep link launched but Roblox not running after extended wait")
        return False
    except Exception as e:
        print_formatted("ERROR", f"Deep link launch failed: {str(e)}")
        return False

def launch_via_browser(game_id: str, private_server: str = '', config: Optional[Dict] = None) -> bool:
    try:
        if not private_server:
            print_formatted("WARNING", "No private server link provided for browser launch")
            return False
            
        print_formatted("INFO", f"Launching via browser: Game ID {game_id}")
        url = build_game_url(game_id, private_server)
        
        # Get browser preference from config
        browser_pref = config.get('browser_preference', 'auto') if config else 'auto'
        browsers = get_available_browsers()
        
        if browser_pref != 'auto' and browser_pref in browsers:
            # Use preferred browser
            command = f'am start -a android.intent.action.VIEW -d "{url}" {browser_pref}'
        elif browsers:
            # Use first available browser
            command = f'am start -a android.intent.action.VIEW -d "{url}" {browsers[0]}'
        else:
            # Use default browser
            command = f'am start -a android.intent.action.VIEW -d "{url}"'
            
        result = run_shell_command(command, platform_info=platform_info)
        
        # Wait for Roblox to start with more frequent checks
        start_time = time.time()
        while time.time() - start_time < 120:  # Wait up to 2 minutes
            if is_roblox_running():
                print_formatted("SUCCESS", "Roblox launched via browser")
                # Wait a bit longer for the game to fully load
                time.sleep(10)
                return True
            time.sleep(3)
            
        print_formatted("WARNING", "Browser launch initiated but Roblox not running after extended wait")
        return False
    except Exception as e:
        print_formatted("ERROR", f"Browser launch failed: {str(e)}")
        return False

# Game State Detection
def is_in_game(game_id: str, private_server: str = '') -> bool:
    try:
        if not is_roblox_running():
            print_formatted("DEBUG", "Roblox not running - not in game")
            return False
            
        # For cloud phone services, we might need to rely on different detection methods
        if platform_info and platform_info['type'] in ['ugphone', 'vsphone', 'redfinger']:
            # Cloud phone services might not support all the standard detection methods
            # Use a simpler approach focused on process existence and basic activity checks
            activity_info = run_shell_command("dumpsys activity | grep -A 10 -B 5 'mResumedActivity'", platform_info=platform_info)
            if ROBLOX_PACKAGE in activity_info and 'mResumedActivity' in activity_info:
                print_formatted("DEBUG", "Roblox is resumed and focused - likely in game")
                return True
                
            # Check if Roblox is in the foreground
            window_info = run_shell_command("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'", platform_info=platform_info)
            if ROBLOX_PACKAGE in window_info:
                print_formatted("DEBUG", "Roblox is in focus - likely in game")
                return True
                
            # If we can't determine accurately, assume we're in game if Roblox is running
            print_formatted("DEBUG", "Assuming in game due to Roblox running on cloud phone")
            return True
        
        # Standard detection for regular Android devices
        # Check for game-specific textures and assets
        texture_check = run_shell_command(f"dumpsys gfxinfo {ROBLOX_PACKAGE} | grep -i 'draw\\|render\\|texture'", platform_info=platform_info)
        if texture_check and ('draw' in texture_check.lower() or 'render' in texture_check.lower()):
            print_formatted("DEBUG", "Game rendering detected - likely in game")
            return True
            
        # Check for specific game process states
        process_states = run_shell_command(f"dumpsys activity processes {ROBLOX_PACKAGE} | grep -E 'state\\|procstate'", platform_info=platform_info)
        if process_states and ('foreground' in process_states.lower() or 'top' in process_states.lower()):
            print_formatted("DEBUG", "Roblox in foreground state - likely in game")
            return True
            
        # Enhanced logcat checking for game join confirmation
        run_shell_command("logcat -c", platform_info=platform_info)
        time.sleep(2)
       
        game_patterns = [
            f"place.*{game_id}", f"game.*{game_id}", f"join.*{game_id}",
            "loading.*complete", "game.*start", "experience.*load",
            "character.*load", "player.*join", "render.*start",
            "physics.*start", "workspace.*load", "joined game",
            "successfully joined"
        ]
       
        if private_server:
            code = extract_private_server_code(private_server)
            if code:
                game_patterns.extend([f"privateServer.*{code}", f"linkCode.*{code}", "private server.*joined"])
       
        log_command = f"logcat -d | grep -iE '{'|'.join(game_patterns)}' | grep -v su | head -20"
        game_logs = run_shell_command(log_command, platform_info=platform_info)
       
        if game_logs.strip():
            print_formatted("DEBUG", f"Game activity logs found: {game_logs.strip()}")
            return True
            
        # Check memory usage
        memory_usage = run_shell_command(f"dumpsys meminfo {ROBLOX_PACKAGE} | grep 'TOTAL'", platform_info=platform_info)
        if memory_usage:
            try:
                mem_value = int(''.join(filter(str.isdigit, memory_usage.split()[0])))
                if mem_value > 500000:
                    print_formatted("DEBUG", f"High memory usage ({mem_value} KB) - likely in game")
                    return True
            except:
                pass
                
        print_formatted("DEBUG", "No strong indicators of being in game found")
        return False
    except Exception as e:
        print_formatted("ERROR", f"Game detection error: {str(e)}")
        return False

def detect_roblox_error_codes() -> List[str]:
    try:
        # Check for Roblox error codes
        error_patterns = [
            r'error code[:\s]*(\d+)',
            r'error.*code[:\s]*(\d+)',
            r'code[:\s]*(\d+).*error',
            r'err.*code[:\s]*(\d+)',
            r'error\s+(\d+)',
            r'code\s+(\d+).*failed',
            r'failed.*code\s+(\d+)'
        ]
        
        error_codes = []
        
        # Check logcat for errors
        log_output = run_shell_command("logcat -d | grep -i error | grep -v su | head -20", platform_info=platform_info)
        
        for pattern in error_patterns:
            matches = re.findall(pattern, log_output, re.IGNORECASE)
            error_codes.extend(matches)
            
        # Also check for specific Roblox error patterns
        roblox_errors = run_shell_command("logcat -d | grep -i roblox | grep -i error | grep -v su | head -10", platform_info=platform_info)
        for pattern in error_patterns:
            matches = re.findall(pattern, roblox_errors, re.IGNORECASE)
            error_codes.extend(matches)
            
        return list(set(error_codes))  # Remove duplicates
    except Exception as e:
        print_formatted("ERROR", f"Error code detection failed: {str(e)}")
        return []

def check_error_states(config: Optional[Dict] = None) -> Optional[str]:
    try:
        if not config or not config.get('error_detection', True):
            return None
            
        # Check for common error dialogs and popups
        ui_dump = run_shell_command("uiautomator dump /sdcard/ui_dump.xml && cat /sdcard/ui_dump.xml", platform_info=platform_info)
       
        error_indicators = [
            'error', 'crash', 'disconnect', 'kicked', 'banned',
            'failed', 'unable', 'sorry', 'oops', 'problem',
            'restart', 'rejoin', 'retry', 'close', 'exit',
            'unexpected client', 'exploiting', 'same account', 
            'idle', 'anti-cheat', 'connection lost', 'reconnect'
        ]
       
        if any(indicator in ui_dump.lower() for indicator in error_indicators):
            print_formatted("WARNING", "Error dialog detected in UI")
            return 'ui_error'
            
        # Check for ANR
        anr_info = run_shell_command("dumpsys activity | grep -i 'anr'", platform_info=platform_info)
        if anr_info and ROBLOX_PACKAGE in anr_info:
            print_formatted("WARNING", f"ANR detected: {anr_info.strip()}")
            return 'frozen'
            
        if platform_info.get('has_root'):
            anr_files = run_shell_command("ls -l /data/anr/ | grep anr", platform_info=platform_info)
            if anr_files and ROBLOX_PACKAGE in anr_files:
                print_formatted("WARNING", "ANR trace files detected for Roblox")
                return 'frozen'
                
        # Check for recent crashes in logcat
        run_shell_command("logcat -c", platform_info=platform_info)
        time.sleep(1)
       
        crash_patterns = [
            'fatal', 'exception', 'sigsegv', 'segmentation',
            'native crash', 'system_server', 'am_crash',
            'beginning of crash', 'backtrace', 'unexpected client',
            'kicked', 'banned', 'disconnected'
        ]
       
        crash_logs = run_shell_command(f"logcat -d | grep -iE '{'|'.join(crash_patterns)}' | grep -v su | head -10", platform_info=platform_info)
        if crash_logs.strip():
            print_formatted("WARNING", f"Crash detected in logs: {crash_logs.strip()}")
            return 'crash'
            
        # Check for network/timeout errors
        network_errors = run_shell_command("logcat -d | grep -iE 'timeout|disconnect|network|connection|idle' | grep -v su | head -5", platform_info=platform_info)
        if network_errors.strip():
            print_formatted("WARNING", f"Network issues: {network_errors.strip()}")
            return 'network_error'
            
        # Check for Roblox error codes
        error_codes = detect_roblox_error_codes()
        if error_codes:
            for code in error_codes:
                if code not in error_codes_detected:
                    print_formatted("WARNING", f"Roblox error code detected: {code}")
                    error_info = ROBLOX_ERROR_DATABASE.get(code, {"name": "Unknown error", "solution": "Check logs", "wait_time": 30})
                    print_formatted("INFO", f"Error {code}: {error_info['name']} - {error_info['solution']}")
                    error_codes_detected.add(code)
            return 'roblox_error'
            
        return None
    except Exception as e:
        print_formatted("ERROR", f"Error state check failed: {str(e)}")
        return None

# Main Automation Logic
def attempt_game_join(config: Dict) -> bool:
    global last_game_join_time, consecutive_failures, last_error_time
    
    game_id = config.get('game_id')
    private_server = config.get('private_server', '')
    
    if not game_id:
        print_formatted("ERROR", "No game ID specified in config")
        return False
    
    # Check if we need to wait due to a recent error
    current_time = time.time()
    if current_time - last_error_time < 10:  # Minimum 10 seconds between attempts after errors
        wait_time = 10 - (current_time - last_error_time)
        print_formatted("INFO", f"Waiting {wait_time:.1f} seconds after recent error...")
        time.sleep(wait_time)
   
    # Check if already in game
    if is_roblox_running() and is_in_game(game_id, private_server) and not check_error_states(config):
        print_formatted("SUCCESS", f"Already joined in game {game_id} - no need to relaunch")
        last_game_join_time = time.time()
        consecutive_failures = 0
        return True
   
    print_formatted("INFO", f"Attempting to join game {game_id}")
    if not close_roblox(config):
        print_formatted("WARNING", "Failed to close Roblox properly")
   
    time.sleep(3)
   
    # Prioritize browser launch for private server
    success = False
    if private_server:
        print_formatted("INFO", "Trying launch method: launch_via_browser")
        if launch_via_browser(game_id, private_server, config):
            if wait_for_game_join(config, timeout=180):
                last_game_join_time = time.time()
                print_formatted("SUCCESS", "Successfully joined game using browser")
                success = True
            else:
                print_formatted("WARNING", "Game join timeout with browser launch")
        else:
            print_formatted("WARNING", "Browser launch failed")
    else:
        # Use deep link for public server
        print_formatted("INFO", "Trying launch method: launch_via_deep_link")
        if launch_via_deep_link(game_id, private_server):
            if wait_for_game_join(config, timeout=180):
                last_game_join_time = time.time()
                print_formatted("SUCCESS", "Successfully joined game using deep link")
                success = True
            else:
                print_formatted("WARNING", "Game join timeout with deep link")
        else:
            print_formatted("WARNING", "Deep link launch failed")
   
    if success:
        consecutive_failures = 0
        return True
    else:
        consecutive_failures += 1
        last_error_time = time.time()
        print_formatted("ERROR", "Game join attempt failed")
        return False

def wait_for_game_join(config: Dict, timeout: int = 180) -> bool:
    start_time = time.time()
    game_id = config.get('game_id')
    private_server = config.get('private_server', '')
    
    # Wait longer before starting to check if we're in the game
    initial_wait = config.get('game_load_delay', 90)  # Wait 90 seconds before checking
    print_formatted("INFO", f"Waiting {initial_wait} seconds for game to load before checking...")
    time.sleep(initial_wait)
    
    while time.time() - start_time < timeout:
        if is_in_game(game_id, private_server):
            print_formatted("SUCCESS", f"Detected successful join in game {game_id}")
            return True
            
        # Check for errors that might prevent joining
        error_state = check_error_states(config)
        if error_state:
            print_formatted("WARNING", f"Detected error during join: {error_state}")
            return False
            
        time.sleep(5)  # Check more frequently
        
    print_formatted("INFO", "Game join timeout, checking error states")
    error_state = check_error_states(config)
    if error_state:
        print_formatted("WARNING", f"Detected error during join: {error_state}")
        
    return False

def automation_loop(config: Dict) -> None:
    global automation_running, last_game_join_time, consecutive_failures, last_game_verification_time
    
    automation_running = True
    print_formatted("SUCCESS", "Automation started successfully!")
   
    max_consecutive_failures = config.get('max_retries', 5)
    game_verification_interval = config.get('game_verification_interval', 300)  # Default 5 minutes
   
    while automation_running:
        try:
            game_id = config.get('game_id')
            current_time = time.time()
           
            # Check if it's time to verify we're still in the correct game
            if (last_game_verification_time > 0 and 
                current_time - last_game_verification_time >= game_verification_interval):
                print_formatted("INFO", "Periodic game verification check...")
                in_target_game = is_in_game(game_id, config.get('private_server', ''))
                if not in_target_game:
                    print_formatted("WARNING", "No longer in target game during periodic check - rejoining...")
                    if attempt_game_join(config):
                        consecutive_failures = 0
                    else:
                        consecutive_failures += 1
                else:
                    print_formatted("INFO", "Still in correct game - continuing...")
                    consecutive_failures = 0
                
                last_game_verification_time = current_time
                # Continue with normal check after verification
                continue
           
            # Check current state
            roblox_running = is_roblox_running()
            in_target_game = is_in_game(game_id, config.get('private_server', '')) if roblox_running else False
            error_state = check_error_states(config) if roblox_running else None
           
            # Decision logic
            if not roblox_running:
                print_formatted("INFO", "Roblox not running - launching...")
                if attempt_game_join(config):
                    consecutive_failures = 0
                    last_game_verification_time = current_time
                else:
                    consecutive_failures += 1
                   
            elif error_state:
                print_formatted("WARNING", f"Error detected ({error_state}) - restarting...")
                if attempt_game_join(config):
                    consecutive_failures = 0
                    last_game_verification_time = current_time
                else:
                    consecutive_failures += 1
                   
            elif not in_target_game:
                print_formatted("INFO", "Not in target game - rejoining...")
                if attempt_game_join(config):
                    consecutive_failures = 0
                    last_game_verification_time = current_time
                else:
                    consecutive_failures += 1
                   
            else:
                print_formatted("INFO", f"Already in game {game_id} and running normally - monitoring...")
                consecutive_failures = 0
                # Update verification time if not set
                if last_game_verification_time == 0:
                    last_game_verification_time = current_time
           
            # Safety check for too many failures
            if consecutive_failures >= max_consecutive_failures:
                print_formatted("ERROR", f"Too many consecutive failures ({consecutive_failures}) - pausing...")
                time.sleep(300)
                consecutive_failures = 0
           
            check_delay = config.get('check_delay', 60)  # Default to 60 seconds
            print_formatted("INFO", f"Waiting {check_delay} seconds before next check...")
            
            # Add some randomness to the delay to avoid predictable patterns
            random_delay = random.uniform(0.8, 1.2) * check_delay
            time.sleep(random_delay)
           
        except KeyboardInterrupt:
            print_formatted("INFO", "Automation interrupted by user")
            break
        except Exception as e:
            print_formatted("ERROR", f"Automation loop error: {str(e)}")
            time.sleep(10)
   
    automation_running = False
    print_formatted("INFO", "Automation stopped")

# Interactive Menu
def display_menu() -> None:
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{COLORS['HEADER']}{'='*50}")
    print(f" ENHANCED ROBLOX AUTOMATION TOOL")
    print(f"{'='*50}{COLORS['RESET']}")
    
    if platform_info:
        print(f"{COLORS['INFO']}Platform: {platform_info['name']} ({platform_info['type']}){COLORS['RESET']}")
        print(f"{COLORS['INFO']}Root Access: {'Yes' if platform_info.get('has_root') else 'Limited'}{COLORS['RESET']}")
        
    print(f"\n{COLORS['CYAN']}1.{COLORS['RESET']} Configure Settings")
    print(f"{COLORS['CYAN']}2.{COLORS['RESET']} Start Automation")
    print(f"{COLORS['CYAN']}3.{COLORS['RESET']} Stop Automation")
    print(f"{COLORS['CYAN']}4.{COLORS['RESET']} Test Game Join")
    print(f"{COLORS['CYAN']}5.{COLORS['RESET']} View Current Config")
    print(f"{COLORS['CYAN']}6.{COLORS['RESET']} System Information")
    print(f"{COLORS['CYAN']}7.{COLORS['RESET']} Exit")
    
    if automation_running:
        print(f"\n{COLORS['SUCCESS']}Status: Automation is RUNNING{COLORS['RESET']}")
    else:
        print(f"\n{COLORS['WARNING']}Status: Automation is STOPPED{COLORS['RESET']}")
        
    if last_game_join_time:
        join_time = datetime.fromtimestamp(last_game_join_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{COLORS['INFO']}Last Game Join: {join_time}{COLORS['RESET']}")
        
    if error_codes_detected:
        print(f"{COLORS['WARNING']}Detected Error Codes: {', '.join(error_codes_detected)}{COLORS['RESET']}")

def configure_settings() -> None:
    config = load_config()
    print(f"\n{COLORS['HEADER']}=== CONFIGURATION SETUP ==={COLORS['RESET']}")
    
    # Game ID
    current_game_id = config.get('game_id', '')
    print(f"\nCurrent Game ID: {current_game_id if current_game_id else 'Not set'}")
    new_game_id = input("Enter new Game ID (or press Enter to keep current): ").strip()
    if new_game_id:
        config['game_id'] = new_game_id
        
    # Private Server
    current_private_server = config.get('private_server', '')
    print(f"\nCurrent Private Server: {current_private_server if current_private_server else 'Not set'}")
    print("Enter the full private server URL")
    new_private_server = input("Enter Private Server link (or press Enter to keep current): ").strip()
    if new_private_server:
        config['private_server'] = new_private_server
        
    # Check Delay
    current_delay = config.get('check_delay', 60)
    print(f"\nCurrent Check Delay: {current_delay} seconds")
    new_delay = input("Enter new Check Delay in seconds (or press Enter to keep current): ").strip()
    if new_delay and new_delay.isdigit():
        config['check_delay'] = int(new_delay)
        
    # Game Load Delay
    current_load_delay = config.get('game_load_delay', 90)
    print(f"\nCurrent Game Load Delay: {current_load_delay} seconds")
    print("This is how long to wait after launching before checking if you're in the game")
    new_load_delay = input("Enter new Game Load Delay in seconds (or press Enter to keep current): ").strip()
    if new_load_delay and new_load_delay.isdigit():
        config['game_load_delay'] = int(new_load_delay)
        
    # Game Verification Interval
    current_verification_interval = config.get('game_verification_interval', 300)
    print(f"\nCurrent Game Verification Interval: {current_verification_interval} seconds")
    print("This is how often to check if you're still in the correct game (5 minutes = 300 seconds)")
    new_verification_interval = input("Enter new Game Verification Interval in seconds (or press Enter to keep current): ").strip()
    if new_verification_interval and new_verification_interval.isdigit():
        config['game_verification_interval'] = int(new_verification_interval)
        
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
        
    # Browser Preference
    browsers = get_available_browsers()
    current_browser = config.get('browser_preference', 'auto')
    print(f"\nCurrent Browser Preference: {current_browser}")
    print(f"Available browsers: {', '.join(browsers) if browsers else 'None detected'}")
    print("Enter browser package name or 'auto' for automatic selection")
    new_browser = input("Enter Browser Preference (or press Enter to keep current): ").strip()
    if new_browser:
        config['browser_preference'] = new_browser
        
    # Error Detection
    current_error_detection = config.get('error_detection', True)
    print(f"\nCurrent Error Detection: {'Enabled' if current_error_detection else 'Disabled'}")
    new_error_detection = input("Enable Error Detection? (y/n, or press Enter to keep current): ").strip().lower()
    if new_error_detection in ['y', 'yes']:
        config['error_detection'] = True
    elif new_error_detection in ['n', 'no']:
        config['error_detection'] = False
        
    if save_config(config):
        print_formatted("SUCCESS", "Configuration saved successfully!")
    else:
        print_formatted("ERROR", "Failed to save configuration!")
        
    input("\nPress Enter to continue...")

def view_current_config() -> None:
    config = load_config()
    print(f"\n{COLORS['HEADER']}=== CURRENT CONFIGURATION ==={COLORS['RESET']}")
    print(f"{COLORS['CYAN']}Game ID:{COLORS['RESET']} {config.get('game_id', 'Not set')}")
    print(f"{COLORS['CYAN']}Private Server:{COLORS['RESET']} {config.get('private_server', 'Not set')}")
    print(f"{COLORS['CYAN']}Check Delay:{COLORS['RESET']} {config.get('check_delay', 60)} seconds")
    print(f"{COLORS['CYAN']}Game Load Delay:{COLORS['RESET']} {config.get('game_load_delay', 90)} seconds")
    print(f"{COLORS['CYAN']}Game Verification Interval:{COLORS['RESET']} {config.get('game_verification_interval', 300)} seconds")
    print(f"{COLORS['CYAN']}Max Retries:{COLORS['RESET']} {config.get('max_retries', 3)}")
    print(f"{COLORS['CYAN']}Auto Rejoin:{COLORS['RESET']} {'Enabled' if config.get('auto_rejoin', True) else 'Disabled'}")
    print(f"{COLORS['CYAN']}Browser Preference:{COLORS['RESET']} {config.get('browser_preference', 'auto')}")
    print(f"{COLORS['CYAN']}Error Detection:{COLORS['RESET']} {'Enabled' if config.get('error_detection', True) else 'Disabled'}")
    print(f"{COLORS['CYAN']}Game Validation:{COLORS['RESET']} {'Enabled' if config.get('game_validation', True) else 'Disabled'}")
    print(f"{COLORS['CYAN']}Launch Delay:{COLORS['RESET']} {config.get('launch_delay', 300)} seconds")
    print(f"{COLORS['CYAN']}Retry Delay:{COLORS['RESET']} {config.get('retry_delay', 15)} seconds")
    input("\nPress Enter to continue...")

def test_game_join() -> None:
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

def show_system_info() -> None:
    print(f"\n{COLORS['HEADER']}=== SYSTEM INFORMATION ==={COLORS['RESET']}")
    
    if platform_info:
        print(f"{COLORS['CYAN']}Platform Type:{COLORS['RESET']} {platform_info['type']}")
        print(f"{COLORS['CYAN']}Platform Name:{COLORS['RESET']} {platform_info['name']}")
        print(f"{COLORS['CYAN']}Root Access:{COLORS['RESET']} {'Available' if platform_info.get('has_root') else 'Limited'}")
        print(f"{COLORS['CYAN']}ADB Support:{COLORS['RESET']} {'Yes' if platform_info.get('use_adb') else 'No'}")
        print(f"{COLORS['CYAN']}Shell Prefix:{COLORS['RESET']} {platform_info.get('shell_prefix', 'None')}")
        print(f"{COLORS['CYAN']}Process Check Method:{COLORS['RESET']} {platform_info.get('process_check_method', 'Unknown')}")
        print(f"{COLORS['CYAN']}Browser Launch Method:{COLORS['RESET']} {platform_info.get('browser_launch', 'Unknown')}")
        
    roblox_installed = verify_roblox_installation()
    print(f"{COLORS['CYAN']}Roblox Installed:{COLORS['RESET']} {'Yes' if roblox_installed else 'No'}")
    
    if roblox_installed:
        roblox_running = is_roblox_running()
        print(f"{COLORS['CYAN']}Roblox Running:{COLORS['RESET']} {'Yes' if roblox_running else 'No'}")
        
    # Show available browsers
    browsers = get_available_browsers()
    print(f"{COLORS['CYAN']}Available Browsers:{COLORS['RESET']} {', '.join(browsers) if browsers else 'None'}")
    
    try:
        android_version = run_shell_command("getprop ro.build.version.release", platform_info=platform_info)
        print(f"{COLORS['CYAN']}Android Version:{COLORS['RESET']} {android_version if android_version else 'Unknown'}")
    except:
        pass
        
    try:
        device_model = run_shell_command("getprop ro.product.model", platform_info=platform_info)
        print(f"{COLORS['CYAN']}Device Model:{COLORS['RESET']} {device_model if device_model else 'Unknown'}")
    except:
        pass
        
    input("\nPress Enter to continue...")

# Main Function
def main() -> None:
    global platform_info, automation_running
    
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{COLORS['HEADER']}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║               ENHANCED ROBLOX AUTOMATION TOOL                ║")
        print("║         Supports: UGPHONE, VSPHONE, REDFINGER                ║")
        print("║             Standard Android & Emulators                     ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{COLORS['RESET']}")
        
        detector = PlatformDetector()
        platform_info = detector.detect_platform()
        
        if not verify_roblox_installation():
            print_formatted("ERROR", "Roblox is not installed or not accessible!")
            print_formatted("INFO", "Please install Roblox and ensure proper permissions.")
            sys.exit(1)
            
        automation_thread = None
        
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
