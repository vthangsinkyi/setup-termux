lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII, lllllllllllIlll, lllllllllllIllI, lllllllllllIlIl, lllllllllllIlII, lllllllllllIIll, lllllllllllIIlI, lllllllllllIIIl = filter, range, __name__, Exception, KeyboardInterrupt, list, bool, print, open, any, input, getattr, set, int, str

from logging import INFO as IllIIllIIIlIIl, basicConfig as llIlIIIlIIlIlI, FileHandler as IIIllIIIlIlIII, StreamHandler as IIlllIIllIIlIl, getLogger as lIIIllIIlIlllI
from os.path import exists as IlIIlIIIlIlIll
from subprocess import TimeoutExpired as lllllIIlIlIIII, run as llIIlIlIlIllII
from json import dump as llIIllllIIIllI, load as lIlIIIllIIllIl
from requests import post as IllllIIlllIIIl
from time import sleep as llIIIIIlIllIII, time as IlIllIIIllIlIl
from re import search as IIlIlIllIlIlII, findall as lIlIIlllllIIlI, IGNORECASE as IIIlIIIIIlIIlI
from random import uniform as IllIllIIIlllll
from os import name as lIIIlIIlIlllII, system as IIlllllllIIIll
from sys import exit as IlIllIlllIIIll
from threading import Thread as lIllllllIIIlll
'\nEnhanced Roblox Automation Tool (Rejoiner.py)\nSupports: UGPHONE, VSPHONE, REDFINGER, Standard Android/Emulators\nAuthor: Optimized for game monitoring and private server joining\n'
from datetime import datetime as IIIlIIIIllllIl
from typing import Dict as IIIllIlIllIIll, List as lIIIIlllllIlIl, Optional as llllIIllIllllI, Any as IlllIlIIllIlII
llIlIIIlIIlIlI(level=IllIIllIIIlIIl, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[IIIllIIIlIlIII('/sdcard/roblox_automation.log'), IIlllIIllIIlIl()])
lIllllIIlllIIlllII = lIIIllIIlIlllI('Rejoiner')
lIIllllllIlIllllll = {'RESET': '\x1b[0m', 'INFO': '\x1b[94m', 'SUCCESS': '\x1b[92m', 'WARNING': '\x1b[93m', 'ERROR': '\x1b[91m', 'BOLD': '\x1b[1m', 'CYAN': '\x1b[96m', 'HEADER': '\x1b[95m', 'DEBUG': '\x1b[90m'}
llllIIIllllIIIllII = '/sdcard/roblox_config.json'
IlIlllIIIllIlllIII = 'com.roblox.client'
IIlIlIIlllIIllllIl = ['com.android.chrome', 'com.sec.android.app.sbrowser', 'com.google.android.webview', 'org.mozilla.firefox', 'com.opera.browser', 'com.brave.browser', 'com.microsoft.emmx', 'com.vivaldi.browser']
IllIIIllllIlllIIIl = {'267': {'name': 'Cannot rejoin game', 'solution': 'Wait 30 seconds before retry', 'wait_time': 30}, '279': {'name': 'Server full', 'solution': 'Try different server or wait', 'wait_time': 15}, '292': {'name': 'Kicked from game', 'solution': 'Check if banned, wait 5 minutes', 'wait_time': 300}, '529': {'name': 'Connection lost', 'solution': 'Check network, restart if persistent', 'wait_time': 10}, '601': {'name': 'Place unavailable', 'solution': 'Game might be updating, check later', 'wait_time': 60}}
llIIIlIlllIIIlllII = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
IlIIlllIlIllIIIIll = None
lIIllllIllIlllIlll = None
IIllllIlIlIlllllII = lllllllllllIIll()
lIIllllllIllIlllIl = 0
IIlllIIllIlIIIllII = 0
lllIlllIlllIlIIIll = 0
IIlIllllIlllllIlll = 'unknown'

class IIlIllIllIllIlIIIl:

    def __init__(llllIlIlIllIlIIlIl):
        llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll = None

    def llIIIIIllIllIlIIlI(llllIlIlIllIlIIlIl) -> IIIllIlIllIIll[lllllllllllIIIl, IlllIlIIllIlII]:
        try:
            if llllIlIlIllIlIIlIl.IlIlIllllIIIIlIlIl():
                llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll = {'type': 'ugphone', 'name': 'UGPHONE', 'has_root': llllIlIlIllIlIIlIl.lIIlIlIllIIIllIllI(), 'use_adb': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'shell_prefix': '', 'special_commands': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'process_check_method': 'ps_grep', 'browser_launch': 'intent'}
                IIIIIllIIIIllIlllI('INFO', f"Platform detected: {llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll['name']}")
                return llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll
            if llllIlIlIllIlIIlIl.IIIIlIIllIIlIllIlI():
                llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll = {'type': 'vsphone', 'name': 'VSPHONE', 'has_root': llllIlIlIllIlIIlIl.IIIIllllIlllIlIlIl(), 'use_adb': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'shell_prefix': '', 'special_commands': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'process_check_method': 'ps_grep', 'browser_launch': 'intent'}
                IIIIIllIIIIllIlllI('INFO', f"Platform detected: {llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll['name']}")
                return llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll
            if llllIlIlIllIlIIlIl.IIlIlIIlIlIllIllll():
                llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll = {'type': 'redfinger', 'name': 'REDFINGER', 'has_root': llllIlIlIllIlIIlIl.lIlllIllllIIlIIIIl(), 'use_adb': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'shell_prefix': 'su -c', 'special_commands': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'process_check_method': 'pidof', 'browser_launch': 'intent'}
                IIIIIllIIIIllIlllI('INFO', f"Platform detected: {llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll['name']}")
                return llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll
            llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll = {'type': 'standard', 'name': 'Standard Android', 'has_root': llllIlIlIllIlIIlIl.lIIlIIIlIIlIIIIlIl(), 'use_adb': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'shell_prefix': 'su -c', 'special_commands': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'process_check_method': 'pidof', 'browser_launch': 'intent'}
            IIIIIllIIIIllIlllI('INFO', f"Platform detected: {llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll['name']}")
            return llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll
        except lllllllllllllII as lIlIIlIlIIllIllIIl:
            IIIIIllIIIIllIlllI('ERROR', f'Platform detection error: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
            llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll = {'type': 'standard', 'name': 'Standard Android (Fallback)', 'has_root': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'use_adb': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'shell_prefix': '', 'special_commands': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'process_check_method': 'ps_grep', 'browser_launch': 'intent'}
            return llllIlIlIllIlIIlIl.IIlllIIIIIIllIIlll

    def IlIlIllllIIIIlIlIl(llllIlIlIllIlIIlIl) -> llllllllllllIIl:
        try:
            IIIIIIllIlllIIlIll = ['/system/bin/ugphone', '/system/app/UGPhone', '/data/local/tmp/ugphone', '/system/priv-app/UGPhone', '/system/framework/ugphone.jar', '/system/etc/ugphone', '/vendor/bin/ugphone', '/system/bin/ug_phone']
            for lIIlIIIllllIllIIIl in IIIIIIllIlllIIlIll:
                if IlIIlIIIlIlIll(lIIlIIIllllIllIIIl):
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIllIIIIlIIlIIlII = llllIlIlIllIlIIlIl.IlIlIIlIlllIIIlIlI()
            IlIlllIIllIlIIlllI = ['ugphone', 'ug_phone', 'cloudphone', 'universal.global.phone', 'ugcloud']
            for lllIllIllIlllIlIIl in IlIlllIIllIlIIlllI:
                if lllIllIllIlllIlIIl.lower() in llIllIIIIlIIlIIlII.lower():
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIIlIlIllIlIIIIlI = llllIlIlIllIlIIlIl.IlIlIIlIllllIllIlI()
            if lllllllllllIllI(('ugphone' in var.lower() for var in llIIlIlIllIlIIIIlI)):
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIIlllIllIlIlIlII = llllIlIlIllIlIIlIl.lllIlIlIlIllIIlllI()
            if lllllllllllIllI(('ugphone' in proc.lower() for proc in llIIlllIllIlIlIlII)):
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        except:
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def IIIIlIIllIIlIllIlI(llllIlIlIllIlIIlIl) -> llllllllllllIIl:
        try:
            IIIIIIllIlllIIlIll = ['/system/bin/vsphone', '/system/app/VSPhone', '/data/local/tmp/vsphone', '/system/priv-app/VSPhone', '/system/framework/vsphone.jar', '/system/etc/vsphone', '/vendor/bin/vsphone', '/system/bin/vs_phone']
            for lIIlIIIllllIllIIIl in IIIIIIllIlllIIlIll:
                if IlIIlIIIlIlIll(lIIlIIIllllIllIIIl):
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIllIIIIlIIlIIlII = llllIlIlIllIlIIlIl.IlIlIIlIlllIIIlIlI()
            lIIIlllllIIIIlIlII = ['vsphone', 'vs_phone', 'virtualphone', 'virtual.space', 'vspace']
            for lllIllIllIlllIlIIl in lIIIlllllIIIIlIlII:
                if lllIllIllIlllIlIIl.lower() in llIllIIIIlIIlIIlII.lower():
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIIlIlIllIlIIIIlI = llllIlIlIllIlIIlIl.IlIlIIlIllllIllIlI()
            if lllllllllllIllI(('vsphone' in var.lower() for var in llIIlIlIllIlIIIIlI)):
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIIlllIllIlIlIlII = llllIlIlIllIlIIlIl.lllIlIlIlIllIIlllI()
            if lllllllllllIllI(('vsphone' in proc.lower() for proc in llIIlllIllIlIlIlII)):
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        except:
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def IIlIlIIlIlIllIllll(llllIlIlIllIlIIlIl) -> llllllllllllIIl:
        try:
            IIIIIIllIlllIIlIll = ['/system/bin/redfinger', '/system/app/RedFinger', '/data/local/tmp/redfinger', '/system/priv-app/RedFinger', '/system/framework/redfinger.jar', '/system/etc/redfinger', '/vendor/bin/redfinger', '/system/bin/red_finger']
            for lIIlIIIllllIllIIIl in IIIIIIllIlllIIlIll:
                if IlIIlIIIlIlIll(lIIlIIIllllIllIIIl):
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIllIIIIlIIlIIlII = llllIlIlIllIlIIlIl.IlIlIIlIlllIIIlIlI()
            lIlIIIIIIlIIllllll = ['redfinger', 'red_finger', 'redcloud', 'red.finger', 'rfcloud']
            for lllIllIllIlllIlIIl in lIlIIIIIIlIIllllll:
                if lllIllIllIlllIlIIl.lower() in llIllIIIIlIIlIIlII.lower():
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIIlIlIllIlIIIIlI = llllIlIlIllIlIIlIl.IlIlIIlIllllIllIlI()
            if lllllllllllIllI(('redfinger' in var.lower() for var in llIIlIlIllIlIIIIlI)):
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIIlllIllIlIlIlII = llllIlIlIllIlIIlIl.lllIlIlIlIllIIlllI()
            if lllllllllllIllI(('redfinger' in proc.lower() for proc in llIIlllIllIlIlIlII)):
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        except:
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def IlIlIIlIlllIIIlIlI(llllIlIlIllIlIIlIl) -> lllllllllllIIIl:
        try:
            IIIllIllIllIlIlIlI = llIIlIlIlIllII(['cat', '/system/build.prop'], capture_output=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), text=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), timeout=5)
            return IIIllIllIllIlIlIlI.stdout
        except:
            return ''

    def IlIlIIlIllllIllIlI(llllIlIlIllIlIIlIl) -> lIIIIlllllIlIl[lllllllllllIIIl]:
        try:
            IIIllIllIllIlIlIlI = llIIlIlIlIllII(['env'], capture_output=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), text=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), timeout=5)
            return IIIllIllIllIlIlIlI.stdout.split('\n')
        except:
            return []

    def lllIlIlIlIllIIlllI(llllIlIlIllIlIIlIl) -> lIIIIlllllIlIl[lllllllllllIIIl]:
        try:
            IIIllIllIllIlIlIlI = llIIlIlIlIllII(['ps', '-A'], capture_output=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), text=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), timeout=5)
            return IIIllIllIllIlIlIlI.stdout.split('\n')
        except:
            return []

    def lIIlIIIlIIlIIIIlIl(llllIlIlIllIlIIlIl) -> llllllllllllIIl:
        try:
            IIIllIllIllIlIlIlI = llIIlIlIlIllII(['su', '-c', 'echo test'], capture_output=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), text=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), timeout=5)
            return 'test' in IIIllIllIllIlIlIlI.stdout
        except:
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def lIIlIlIllIIIllIllI(llllIlIlIllIlIIlIl) -> llllllllllllIIl:
        try:
            if llllIlIlIllIlIIlIl.lIIlIIIlIIlIIIIlIl():
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            IIIllIllIllIlIlIlI = llIIlIlIlIllII(['ugphone_su', '-c', 'echo test'], capture_output=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), text=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), timeout=5)
            return 'test' in IIIllIllIllIlIlIlI.stdout
        except:
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def IIIIllllIlllIlIlIl(llllIlIlIllIlIIlIl) -> llllllllllllIIl:
        try:
            if llllIlIlIllIlIIlIl.lIIlIIIlIIlIIIIlIl():
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            IIIllIllIllIlIlIlI = llIIlIlIlIllII(['vsphone_su', '-c', 'echo test'], capture_output=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), text=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), timeout=5)
            return 'test' in IIIllIllIllIlIlIlI.stdout
        except:
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def lIlllIllllIIlIIIIl(llllIlIlIllIlIIlIl) -> llllllllllllIIl:
        try:
            if llllIlIlIllIlIIlIl.lIIlIIIlIIlIIIIlIl():
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            IIIllIllIllIlIlIlI = llIIlIlIlIllII(['redfinger_su', '-c', 'echo test'], capture_output=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), text=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), timeout=5)
            return 'test' in IIIllIllIllIlIlIlI.stdout
        except:
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def IIIIIllIIIIllIlllI(llllIIlIlIIllIIlII: lllllllllllIIIl, llllllllllllIIllll: lllllllllllIIIl) -> None:
    llllIIIIIlllIlIIII = IIIlIIIIllllIl.now().strftime('%Y-%m-%d %H:%M:%S')
    IIlIIIlIlIIIIIlIlI = {'INFO': 'INFO', 'SUCCESS': 'OK', 'WARNING': 'WARN', 'ERROR': 'ERROR', 'HEADER': '====', 'DEBUG': 'DEBUG'}.get(llllIIlIlIIllIIlII, llllIIlIlIIllIIlII)
    lIIllllIIIIIIlIIII = lIIllllllIlIllllll.get(llllIIlIlIIllIIlII, lIIllllllIlIllllll['RESET'])
    llllllllllllIII(f"{lIIllllIIIIIIlIIII}{llllIIIIIlllIlIIII} [{IIlIIIlIlIIIIIlIlI}] {llllllllllllIIllll}{lIIllllllIlIllllll['RESET']}")
    lIllllIIlllIIlllII.log(lllllllllllIlII(logging, llllIIlIlIIllIIlII.upper(), IllIIllIIIlIIl), llllllllllllIIllll)

def IIIIIIIIIllIIllIII(lIIlllIIIlllllllll: lllllllllllIIIl, lIIllIlIlIIIlIIlIl: lllllllllllIIlI=10, IlIIlllIlIllIIIIll: llllIIllIllllI[IIIllIlIllIIll]=None) -> lllllllllllIIIl:
    try:
        if IlIIlllIlIllIIIIll and IlIIlllIlIllIIIIll.get('shell_prefix'):
            if IlIIlllIlIllIIIIll['shell_prefix']:
                llIIlIIIIlllIIllll = IlIIlllIlIllIIIIll['shell_prefix'].split() + [lIIlllIIIlllllllll]
            else:
                llIIlIIIIlllIIllll = lIIlllIIIlllllllll.split()
        else:
            llIIlIIIIlllIIllll = lIIlllIIIlllllllll.split()
        IIIllIllIllIlIlIlI = llIIlIlIlIllII(llIIlIIIIlllIIllll, capture_output=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), text=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), timeout=lIIllIlIlIIIlIIlIl)
        if IIIllIllIllIlIlIlI.stderr and 'permission denied' not in IIIllIllIllIlIlIlI.stderr.lower():
            IIIIIllIIIIllIlllI('DEBUG', f'Command stderr: {IIIllIllIllIlIlIlI.stderr.strip()}')
        return IIIllIllIllIlIlIlI.stdout.strip()
    except lllllIIlIlIIII:
        IIIIIllIIIIllIlllI('WARNING', f'Command timeout: {lIIlllIIIlllllllll}')
        return ''
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Command failed: {lIIlllIIIlllllllll} - {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        return ''

def lIllIIIlIlIIIIlllI() -> IIIllIlIllIIll[lllllllllllIIIl, IlllIlIIllIlII]:
    IllllIlIllIIlIllII = {'accounts': [], 'game_id': '', 'private_server': '', 'check_delay': 60, 'active_account': '', 'check_method': 'both', 'max_retries': 3, 'game_validation': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'launch_delay': 300, 'retry_delay': 15, 'force_kill_delay': 10, 'minimize_crashes': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'launch_attempts': 1, 'cooldown_period': 120, 'auto_rejoin': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'ui_timeout': 30, 'verbose_logging': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'browser_preference': 'auto', 'error_detection': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'performance_mode': llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'game_load_delay': 90, 'game_verification_interval': 300, 'error_wait_times': {'267': 30, '279': 15, '292': 300, '529': 10, '601': 60}, 'discord_webhook': ''}
    try:
        if not IlIIlIIIlIlIll(llllIIIllllIIIllII):
            with lllllllllllIlll(llllIIIllllIIIllII, 'w') as IIlIIlIIlIIIllIlll:
                llIIllllIIIllI(IllllIlIllIIlIllII, IIlIIlIIlIIIllIlll, indent=4)
            IIIIIIIIIllIIllIII(f'chmod 644 {llllIIIllllIIIllII}', platform_info=IlIIlllIlIllIIIIll)
            IIIIIllIIIIllIlllI('INFO', 'Created new config file')
            return IllllIlIllIIlIllII
        with lllllllllllIlll(llllIIIllllIIIllII, 'r') as IIlIIlIIlIIIllIlll:
            IlIlIIIllIllllIlIl = lIlIIIllIIllIl(IIlIIlIIlIIIllIlll)
            for (lIlIIllIlIlllIIlll, llIlIIIlllIlllIllI) in IllllIlIllIIlIllII.items():
                if lIlIIllIlIlllIIlll not in IlIlIIIllIllllIlIl:
                    IlIlIIIllIllllIlIl[lIlIIllIlIlllIIlll] = llIlIIIlllIlllIllI
            return IlIlIIIllIllllIlIl
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Config load error: {lIlIIlIlIIllIllIIl}')
        return IllllIlIllIIlIllII

def IIIIlIIlIIllIIlIlI(IlIlIIIllIllllIlIl: IIIllIlIllIIll[lllllllllllIIIl, IlllIlIIllIlII]) -> llllllllllllIIl:
    try:
        with lllllllllllIlll(llllIIIllllIIIllII, 'w') as IIlIIlIIlIIIllIlll:
            llIIllllIIIllI(IlIlIIIllIllllIlIl, IIlIIlIIlIIIllIlll, indent=4)
        IIIIIIIIIllIIllIII(f'chmod 644 {llllIIIllllIIIllII}', platform_info=IlIIlllIlIllIIIIll)
        IIIIIllIIIIllIlllI('SUCCESS', 'Config saved')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Config save error: {lIlIIlIlIIllIllIIl}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def lIIllllllIIlIlIlll(IIlIllIlIIllIlIlll: lllllllllllIIIl, llllllllllllIIllll: lllllllllllIIIl) -> None:
    if not IIlIllIlIIllIlIlll:
        return
    try:
        lIlIIIlllIIIllIllI = {'content': llllllllllllIIllll}
        lllllIIIllIIlllllI = IllllIIlllIIIl(IIlIllIlIIllIlIlll, json=lIlIIIlllIIIllIllI)
        if lllllIIIllIIlllllI.status_code != 204:
            IIIIIllIIIIllIlllI('WARNING', f'Discord alert failed: {lllllIIIllIIlllllI.status_code}')
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Discord alert error: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')

def lllllllIlIIIIIIlII() -> llllllllllllIIl:
    try:
        lIlllIIIIIllIlIllI = IIIIIIIIIllIIllIII(f'pm list packages {IlIlllIIIllIlllIII}', platform_info=IlIIlllIlIllIIIIll)
        if IlIlllIIIllIlllIII not in lIlllIIIIIllIlIllI:
            IIIIIllIIIIllIlllI('ERROR', 'Roblox not installed.')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        llIlIlIllllIIlIlll = IIIIIIIIIllIIllIII(f'dumpsys package {IlIlllIIIllIlllIII} | grep versionName', platform_info=IlIIlllIlIllIIIIll)
        if llIlIlIllllIIlIlll:
            IIIlIIllIlIlIIIIIl = llIlIlIllllIIlIlll.split('versionName=')[1].split()[0] if 'versionName=' in llIlIlIllllIIlIlll else 'Unknown'
            IIIIIllIIIIllIlllI('INFO', f'Roblox version: {IIIlIIllIlIlIIIIIl}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Roblox verification error: {lIlIIlIlIIllIllIIl}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def IIllIlllIIlIIIIIIl(llIlIIIIIlIIIlIIIl: lllllllllllIIlI=2, lIIIlIIIlllIlllIll: lllllllllllIIlI=1) -> llllllllllllIIl:
    for IIIIllIIIllIllIlIl in llllllllllllllI(llIlIIIIIlIIIlIIIl):
        try:
            if IlIIlllIlIllIIIIll and IlIIlllIlIllIIIIll.get('process_check_method') == 'ps_grep':
                lIlllIIlllllIlllII = IIIIIIIIIllIIllIII(f'ps -A | grep {IlIlllIIIllIlllIII} | grep -v grep', platform_info=IlIIlllIlIllIIIIll)
                if lIlllIIlllllIlllII.strip():
                    IIIIIllIIIIllIlllI('DEBUG', 'Roblox process found via ps+grep')
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            else:
                llllllIlIlIllIllIl = IIIIIIIIIllIIllIII(f'pidof {IlIlllIIIllIlllIII}', platform_info=IlIIlllIlIllIIIIll)
                if llllllIlIlIllIllIl.strip():
                    IIIIIllIIIIllIlllI('DEBUG', 'Roblox PID found via pidof')
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            IlIlIllIllIIIIIIIl = IIIIIIIIIllIIllIII("dumpsys activity | grep -A 10 -B 5 'mResumedActivity'", platform_info=IlIIlllIlIllIIIIll)
            if IlIlllIIIllIlllIII in IlIlIllIllIIIIIIIl and 'mResumedActivity' in IlIlIllIllIIIIIIIl:
                IIIIIllIIIIllIlllI('DEBUG', 'Roblox is resumed and focused')
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            lllIIlllIlllIlIIII = IIIIIIIIIllIIllIII('ps -A', platform_info=IlIIlllIlIllIIIIll)
            if IlIlllIIIllIlllIII in lllIIlllIlllIlIIII:
                IIIIIllIIIIllIlllI('DEBUG', 'Roblox process found in all processes list')
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            if IIIIllIIIllIllIlIl < llIlIIIIIlIIIlIIIl - 1:
                llIIIIIlIllIII(lIIIlIIIlllIlllIll)
        except lllllllllllllII as lIlIIlIlIIllIllIIl:
            IIIIIllIIIIllIlllI('ERROR', f'Roblox running check error: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
            if IIIIllIIIllIllIlIl < llIlIIIIIlIIIlIIIl - 1:
                llIIIIIlIllIII(lIIIlIIIlllIlllIll)
    IIIIIllIIIIllIlllI('DEBUG', 'Roblox process not found')
    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def lIIlIlllIIIlIIlIIl(IlIlIIIllIllllIlIl: llllIIllIllllI[IIIllIlIllIIll]=None) -> llllllllllllIIl:
    try:
        IIIIIllIIIIllIlllI('INFO', 'Closing Roblox...')
        IIIIIIIIIllIIllIII('input keyevent KEYCODE_HOME', platform_info=IlIIlllIlIllIIIIll)
        llIIIIIlIllIII(2)
        IIIIIIIIIllIIllIII(f'am force-stop {IlIlllIIIllIlllIII}', platform_info=IlIIlllIlIllIIIIll)
        llIIIIIlIllIII(2)
        if IlIIlllIlIllIIIIll and IlIIlllIlIllIIIIll['type'] in ['ugphone', 'vsphone', 'redfinger']:
            IIIIIIIIIllIIllIII(f'pkill -f {IlIlllIIIllIlllIII}', platform_info=IlIIlllIlIllIIIIll)
        else:
            IIIIIIIIIllIIllIII(f'killall -9 {IlIlllIIIllIlllIII}', platform_info=IlIIlllIlIllIIIIll)
        lIIllIllIlIlIlllll = IlIlIIIllIllllIlIl.get('force_kill_delay', 10) if IlIlIIIllIllllIlIl else 10
        llIIIIIlIllIII(lIIllIllIlIlIlllll)
        if IIllIlllIIlIIIIIIl():
            IIIIIllIIIIllIlllI('WARNING', 'Roblox still running, clearing cache...')
            IIIIIIIIIllIIllIII(f'pm clear {IlIlllIIIllIlllIII}', platform_info=IlIIlllIlIllIIIIll)
            llIIIIIlIllIII(5)
        llIllllllIlIlIllIl = not IIllIlllIIlIIIIIIl()
        if llIllllllIlIlIllIl:
            IIIIIllIIIIllIlllI('SUCCESS', 'Roblox closed successfully')
        else:
            IIIIIllIIIIllIlllI('ERROR', 'Failed to close Roblox completely')
        return llIllllllIlIlIllIl
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Failed to close Roblox: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def lIIlIllIllIlIllIll() -> lllllllllllIIIl:
    try:
        lIlllIIIIIllIlIllI = IIIIIIIIIllIIllIII(f"dumpsys package {IlIlllIIIllIlllIII} | grep -A 5 'android.intent.action.MAIN'", platform_info=IlIIlllIlIllIIIIll)
        lIIIIIlllIIlIIlIlI = IIlIlIllIlIlII('com\\.roblox\\.client/(\\.[A-Za-z0-9.]+)', lIlllIIIIIllIlIllI)
        if lIIIIIlllIIlIIlIlI:
            IIIIlIlIIIlIIIlIII = lIIIIIlllIIlIIlIlI.group(1)
            IIIIIllIIIIllIlllI('DEBUG', f'Detected main activity: {IIIIlIlIIIlIIIlIII}')
            return IIIIlIlIIIlIIIlIII
        IIlIIIIllIlIlIlllI = ['.startup.ActivitySplash', '.MainActivity', '.HomeActivity']
        for IlllIIllIIIlIlIlIl in IIlIIIIllIlIlIlllI:
            lIIlIlllIIllIIIllI = IIIIIIIIIllIIllIII(f'dumpsys package {IlIlllIIIllIlllIII} | grep {IlllIIllIIIlIlIlIl}', platform_info=IlIIlllIlIllIIIIll)
            if IlllIIllIIIlIlIlIl in lIIlIlllIIllIIIllI:
                return IlllIIllIIIlIlIlIl
        return '.MainActivity'
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('WARNING', f'Main activity detection error: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        return '.MainActivity'

def IllIIlIlIllIIlIIlI(llIIlllllllIlIIIII: lllllllllllIIIl, IIIlIIlIllIllIllll: lllllllllllIIIl='') -> lllllllllllIIIl:
    try:
        if IIIlIIlIllIllIllll:
            if not IIIlIIlIllIllIllll.startswith(('http://', 'https://')):
                IIIlIIlIllIllIllll = f'https://{IIIlIIlIllIllIllll}'
            IIIIIllIIIIllIlllI('INFO', f'Using provided private server URL: {IIIlIIlIllIllIllll}')
            return IIIlIIlIllIllIllll
        lIIlIIIIlIIIlIIIII = f'roblox://experiences/start?placeId={llIIlllllllIlIIIII}'
        IIIIIllIIIIllIlllI('INFO', f'Built game deep link URL: {lIIlIIIIlIIIlIIIII}')
        return lIIlIIIIlIIIlIIIII
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'URL build error: {lIlIIlIlIIllIllIIl}')
        return f'roblox://experiences/start?placeId={llIIlllllllIlIIIII}'

def llllIIllIllllIIlIl(IllllllIIlllIIllII: lllllllllllIIIl) -> llllIIllIllllI[lllllllllllIIIl]:
    try:
        llllIlIIlIIllllIII = ['privateServerLinkCode=([^&]+)', 'share\\?code=([^&]+)', 'linkCode=([^&]+)', 'code=([^&]+)']
        for lllIllIllIlllIlIIl in llllIlIIlIIllllIII:
            lIIIIIlllIIlIIlIlI = IIlIlIllIlIlII(lllIllIllIlllIlIIl, IllllllIIlllIIllII)
            if lIIIIIlllIIlIIlIlI:
                return lIIIIIlllIIlIIlIlI.group(1)
        for lIlIlIIllIlIIlIIll in ['privateServerLinkCode=', 'share?code=', '&linkCode=', '=']:
            if lIlIlIIllIlIIlIIll in IllllllIIlllIIllII:
                IIllllIIlllIIIllIl = IllllllIIlllIIllII.split(lIlIlIIllIlIIlIIll)[1].split('&')[0].strip()
                if IIllllIIlllIIIllIl:
                    return IIllllIIlllIIIllIl
        return None
    except:
        return None

def llIlIlllIIllIlllIl() -> lIIIIlllllIlIl[lllllllllllIIIl]:
    IIllllllIIlIIllIII = []
    for llllIIIlIIIlllIlll in IIlIlIIlllIIllllIl:
        lIlllIIIIIllIlIllI = IIIIIIIIIllIIllIII(f'pm list packages {llllIIIlIIIlllIlll}', platform_info=IlIIlllIlIllIIIIll)
        if llllIIIlIIIlllIlll in lIlllIIIIIllIlIllI:
            IIllllllIIlIIllIII.append(llllIIIlIIIlllIlll)
    return IIllllllIIlIIllIII

def IllllIlllIlIlIlllI(llIIlllllllIlIIIII: lllllllllllIIIl, IIIlIIlIllIllIllll: lllllllllllIIIl='') -> llllllllllllIIl:
    try:
        if IIIlIIlIllIllIllll:
            IIIIIllIIIIllIlllI('INFO', 'Skipping deep link for private server, using browser method')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        IIIIIllIIIIllIlllI('INFO', f'Launching via deep link: Game ID {llIIlllllllIlIIIII}')
        lIIlIIIIlIIIlIIIII = IllIIlIlIllIIlIIlI(llIIlllllllIlIIIII, IIIlIIlIllIllIllll)
        lIIlllIIIlllllllll = f'am start -a android.intent.action.VIEW -d "{lIIlIIIIlIIIlIIIII}"'
        IIIllIllIllIlIlIlI = IIIIIIIIIllIIllIII(lIIlllIIIlllllllll, platform_info=IlIIlllIlIllIIIIll)
        lIllllIIIlIIlIlIII = IlIllIIIllIlIl()
        while IlIllIIIllIlIl() - lIllllIIIlIIlIlIII < 120:
            if IIllIlllIIlIIIIIIl():
                IIIIIllIIIIllIlllI('SUCCESS', 'Roblox launched via deep link')
                llIIIIIlIllIII(10)
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIIIIIlIllIII(3)
        IIIIIllIIIIllIlllI('WARNING', 'Deep link launched but Roblox not running after extended wait')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Deep link launch failed: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def lIlIlIllIlllIlIIIl(llIIlllllllIlIIIII: lllllllllllIIIl, IIIlIIlIllIllIllll: lllllllllllIIIl='', IlIlIIIllIllllIlIl: llllIIllIllllI[IIIllIlIllIIll]=None) -> llllllllllllIIl:
    try:
        if not IIIlIIlIllIllIllll:
            IIIIIllIIIIllIlllI('WARNING', 'No private server link provided for browser launch')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        IIIIIllIIIIllIlllI('INFO', f'Launching via browser: Game ID {llIIlllllllIlIIIII}')
        lIIlIIIIlIIIlIIIII = IllIIlIlIllIIlIIlI(llIIlllllllIlIIIII, IIIlIIlIllIllIllll)
        lIIIllIllIlllIIIIl = IlIlIIIllIllllIlIl.get('browser_preference', 'auto') if IlIlIIIllIllllIlIl else 'auto'
        IIllllllIIlIIllIII = llIlIlllIIllIlllIl()
        if lIIIllIllIlllIIIIl != 'auto' and lIIIllIllIlllIIIIl in IIllllllIIlIIllIII:
            lIIlllIIIlllllllll = f'am start -a android.intent.action.VIEW -d "{lIIlIIIIlIIIlIIIII}" {lIIIllIllIlllIIIIl}'
        elif IIllllllIIlIIllIII:
            lIIlllIIIlllllllll = f'am start -a android.intent.action.VIEW -d "{lIIlIIIIlIIIlIIIII}" {IIllllllIIlIIllIII[0]}'
        else:
            lIIlllIIIlllllllll = f'am start -a android.intent.action.VIEW -d "{lIIlIIIIlIIIlIIIII}"'
        IIIllIllIllIlIlIlI = IIIIIIIIIllIIllIII(lIIlllIIIlllllllll, platform_info=IlIIlllIlIllIIIIll)
        lIllllIIIlIIlIlIII = IlIllIIIllIlIl()
        while IlIllIIIllIlIl() - lIllllIIIlIIlIlIII < 120:
            if IIllIlllIIlIIIIIIl():
                IIIIIllIIIIllIlllI('SUCCESS', 'Roblox launched via browser')
                llIIIIIlIllIII(10)
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            llIIIIIlIllIII(3)
        IIIIIllIIIIllIlllI('WARNING', 'Browser launch initiated but Roblox not running after extended wait')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Browser launch failed: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def lIIIIllIllIlIIIIII(llIIlllllllIlIIIII: lllllllllllIIIl, IIIlIIlIllIllIllll: lllllllllllIIIl='') -> llllllllllllIIl:
    try:
        if not IIllIlllIIlIIIIIIl():
            IIIIIllIIIIllIlllI('DEBUG', 'Roblox not running - not in game')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        if IlIIlllIlIllIIIIll and IlIIlllIlIllIIIIll['type'] in ['ugphone', 'vsphone', 'redfinger']:
            IlIlIllIllIIIIIIIl = IIIIIIIIIllIIllIII("dumpsys activity | grep -A 10 -B 5 'mResumedActivity'", platform_info=IlIIlllIlIllIIIIll)
            if IlIlllIIIllIlllIII in IlIlIllIllIIIIIIIl and 'mResumedActivity' in IlIlIllIllIIIIIIIl:
                IIIIIllIIIIllIlllI('DEBUG', 'Roblox is resumed and focused - likely in game')
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            IlIIllIIIlIlIIllIl = IIIIIIIIIllIIllIII("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'", platform_info=IlIIlllIlIllIIIIll)
            if IlIlllIIIllIlllIII in IlIIllIIIlIlIIllIl:
                IIIIIllIIIIllIlllI('DEBUG', 'Roblox is in focus - likely in game')
                return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            IIIIIllIIIIllIlllI('DEBUG', 'Assuming in game due to Roblox running on cloud phone')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
        lllIlIIlllIlllIIII = IIIIIIIIIllIIllIII(f"dumpsys gfxinfo {IlIlllIIIllIlllIII} | grep -i 'draw\\|render\\|texture'", platform_info=IlIIlllIlIllIIIIll)
        if lllIlIIlllIlllIIII and ('draw' in lllIlIIlllIlllIIII.lower() or 'render' in lllIlIIlllIlllIIII.lower()):
            IIIIIllIIIIllIlllI('DEBUG', 'Game rendering detected - likely in game')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
        llIllllIllllllllll = IIIIIIIIIllIIllIII(f"dumpsys activity processes {IlIlllIIIllIlllIII} | grep -E 'state\\|procstate'", platform_info=IlIIlllIlIllIIIIll)
        if llIllllIllllllllll and ('foreground' in llIllllIllllllllll.lower() or 'top' in llIllllIllllllllll.lower()):
            IIIIIllIIIIllIlllI('DEBUG', 'Roblox in foreground state - likely in game')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
        IIIIIIIIIllIIllIII('logcat -c', platform_info=IlIIlllIlIllIIIIll)
        llIIIIIlIllIII(2)
        llllIllllIlIIIlIII = [f'place.*{llIIlllllllIlIIIII}', f'game.*{llIIlllllllIlIIIII}', f'join.*{llIIlllllllIlIIIII}', 'loading.*complete', 'game.*start', 'experience.*load', 'character.*load', 'player.*join', 'render.*start', 'physics.*start', 'workspace.*load', 'joined game', 'successfully joined']
        if IIIlIIlIllIllIllll:
            IIllllIIlllIIIllIl = llllIIllIllllIIlIl(IIIlIIlIllIllIllll)
            if IIllllIIlllIIIllIl:
                llllIllllIlIIIlIII.extend([f'privateServer.*{IIllllIIlllIIIllIl}', f'linkCode.*{IIllllIIlllIIIllIl}', 'private server.*joined'])
        llIIlllllIlIIIlIII = f"logcat -d | grep -iE '{'|'.join(llllIllllIlIIIlIII)}' | grep -v su | head -20"
        lIIlIIlIIIlllllIIl = IIIIIIIIIllIIllIII(llIIlllllIlIIIlIII, platform_info=IlIIlllIlIllIIIIll)
        if lIIlIIlIIIlllllIIl.strip():
            IIIIIllIIIIllIlllI('DEBUG', f'Game activity logs found: {lIIlIIlIIIlllllIIl.strip()}')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
        IllIllIlllIIIIIIll = IIIIIIIIIllIIllIII(f"dumpsys meminfo {IlIlllIIIllIlllIII} | grep 'TOTAL'", platform_info=IlIIlllIlIllIIIIll)
        if IllIllIlllIIIIIIll:
            try:
                llIIlllllllllIlIll = lllllllllllIIlI(''.join(lllllllllllllll(lllllllllllIIIl.isdigit, IllIllIlllIIIIIIll.split()[0])))
                if llIIlllllllllIlIll > 500000:
                    IIIIIllIIIIllIlllI('DEBUG', f'High memory usage ({llIIlllllllllIlIll} KB) - likely in game')
                    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            except:
                pass
        IIIIIllIIIIllIlllI('DEBUG', 'No strong indicators of being in game found')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Game detection error: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def lllIIllIIlIlIIIIll() -> lIIIIlllllIlIl[lllllllllllIIIl]:
    try:
        lIIlIlllIIIIlIllIl = ['error code[:\\s]*(\\d+)', 'error.*code[:\\s]*(\\d+)', 'code[:\\s]*(\\d+).*error', 'err.*code[:\\s]*(\\d+)', 'error\\s+(\\d+)', 'code\\s+(\\d+).*failed', 'failed.*code\\s+(\\d+)']
        lIIllIlIlIlIlIIIlI = []
        lIIlllIlIlllIlIlll = IIIIIIIIIllIIllIII('logcat -d | grep -i error | grep -v su | head -20', platform_info=IlIIlllIlIllIIIIll)
        for lllIllIllIlllIlIIl in lIIlIlllIIIIlIllIl:
            llllIlIIllIlIIIlII = lIlIIlllllIIlI(lllIllIllIlllIlIIl, lIIlllIlIlllIlIlll, IIIlIIIIIlIIlI)
            lIIllIlIlIlIlIIIlI.extend(llllIlIIllIlIIIlII)
        IIllIlllllIllIlIlI = IIIIIIIIIllIIllIII('logcat -d | grep -i roblox | grep -i error | grep -v su | head -10', platform_info=IlIIlllIlIllIIIIll)
        for lllIllIllIlllIlIIl in lIIlIlllIIIIlIllIl:
            llllIlIIllIlIIIlII = lIlIIlllllIIlI(lllIllIllIlllIlIIl, IIllIlllllIllIlIlI, IIIlIIIIIlIIlI)
            lIIllIlIlIlIlIIIlI.extend(llllIlIIllIlIIIlII)
        return llllllllllllIlI(lllllllllllIIll(lIIllIlIlIlIlIIIlI))
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Error code detection failed: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        return []

def lIIIllllllllIIlIlI(IlIlIIIllIllllIlIl: llllIIllIllllI[IIIllIlIllIIll]=None) -> llllIIllIllllI[lllllllllllIIIl]:
    try:
        if not IlIlIIIllIllllIlIl or not IlIlIIIllIllllIlIl.get('error_detection', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)):
            return None
        lIlIIIlIIlIIIlIIlI = IIIIIIIIIllIIllIII('uiautomator dump /sdcard/ui_dump.xml && cat /sdcard/ui_dump.xml', platform_info=IlIIlllIlIllIIIIll)
        llllllIlIlllIIIllI = ['error', 'crash', 'disconnect', 'kicked', 'banned', 'failed', 'unable', 'sorry', 'oops', 'problem', 'restart', 'rejoin', 'retry', 'close', 'exit', 'unexpected client', 'exploiting', 'same account', 'idle', 'anti-cheat', 'connection lost', 'reconnect']
        if lllllllllllIllI((lIIlIIIllllIllIIIl in lIlIIIlIIlIIIlIIlI.lower() for lIIlIIIllllIllIIIl in llllllIlIlllIIIllI)):
            IIIIIllIIIIllIlllI('WARNING', 'Error dialog detected in UI')
            return 'ui_error'
        lIIIIlllIllIIIIIlI = IIIIIIIIIllIIllIII("dumpsys activity | grep -i 'anr'", platform_info=IlIIlllIlIllIIIIll)
        if lIIIIlllIllIIIIIlI and IlIlllIIIllIlllIII in lIIIIlllIllIIIIIlI:
            IIIIIllIIIIllIlllI('WARNING', f'ANR detected: {lIIIIlllIllIIIIIlI.strip()}')
            return 'frozen'
        if IlIIlllIlIllIIIIll.get('has_root'):
            lIlIIIlIllIlllIlIl = IIIIIIIIIllIIllIII('ls -l /data/anr/ | grep anr', platform_info=IlIIlllIlIllIIIIll)
            if lIlIIIlIllIlllIlIl and IlIlllIIIllIlllIII in lIlIIIlIllIlllIlIl:
                IIIIIllIIIIllIlllI('WARNING', 'ANR trace files detected for Roblox')
                return 'frozen'
        IIIIIIIIIllIIllIII('logcat -c', platform_info=IlIIlllIlIllIIIIll)
        llIIIIIlIllIII(1)
        IIIlllIllIllIllllI = ['fatal', 'exception', 'sigsegv', 'segmentation', 'native crash', 'system_server', 'am_crash', 'beginning of crash', 'backtrace', 'unexpected client', 'kicked', 'banned', 'disconnected']
        IIlIIlIlIIlIIlIIII = IIIIIIIIIllIIllIII(f"logcat -d | grep -iE '{'|'.join(IIIlllIllIllIllllI)}' | grep -v su | head -10", platform_info=IlIIlllIlIllIIIIll)
        if IIlIIlIlIIlIIlIIII.strip():
            IIIIIllIIIIllIlllI('WARNING', f'Crash detected in logs: {IIlIIlIlIIlIIlIIII.strip()}')
            return 'crash'
        llIlIllIlllIIllIll = IIIIIIIIIllIIllIII("logcat -d | grep -iE 'timeout|disconnect|network|connection|idle' | grep -v su | head -5", platform_info=IlIIlllIlIllIIIIll)
        if llIlIllIlllIIllIll.strip():
            IIIIIllIIIIllIlllI('WARNING', f'Network issues: {llIlIllIlllIIllIll.strip()}')
            return 'network_error'
        lIIllIlIlIlIlIIIlI = lllIIllIIlIlIIIIll()
        if lIIllIlIlIlIlIIIlI:
            for IIllllIIlllIIIllIl in lIIllIlIlIlIlIIIlI:
                if IIllllIIlllIIIllIl not in IIllllIlIlIlllllII:
                    IIIIIllIIIIllIlllI('WARNING', f'Roblox error code detected: {IIllllIIlllIIIllIl}')
                    IIIllIIlIllIIIlllI = IllIIIllllIlllIIIl.get(IIllllIIlllIIIllIl, {'name': 'Unknown error', 'solution': 'Check logs', 'wait_time': 30})
                    IIIIIllIIIIllIlllI('INFO', f"Error {IIllllIIlllIIIllIl}: {IIIllIIlIllIIIlllI['name']} - {IIIllIIlIllIIIlllI['solution']}")
                    IIllllIlIlIlllllII.add(IIllllIIlllIIIllIl)
            return 'roblox_error'
        return None
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Error state check failed: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        return None

def IllllIllIllIlIllll(IlIlIIIllIllllIlIl: IIIllIlIllIIll) -> llllllllllllIIl:
    global lIIllllIllIlllIlll, lIIllllllIllIlllIl, IIlllIIllIlIIIllII, IIlIllllIlllllIlll
    llIIlllllllIlIIIII = IlIlIIIllIllllIlIl.get('game_id')
    IIIlIIlIllIllIllll = IlIlIIIllIllllIlIl.get('private_server', '')
    if not llIIlllllllIlIIIII:
        IIIIIllIIIIllIlllI('ERROR', 'No game ID specified in config')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    llIlllIlllIlllIlIl = IlIllIIIllIlIl()
    if llIlllIlllIlllIlIl - IIlllIIllIlIIIllII < 10:
        lIlIIlllIllIIlIlll = 10 - (llIlllIlllIlllIlIl - IIlllIIllIlIIIllII)
        IIIIIllIIIIllIlllI('INFO', f'Waiting {lIlIIlllIllIIlIlll:.1f} seconds after recent error...')
        llIIIIIlIllIII(lIlIIlllIllIIlIlll)
    if IIllIlllIIlIIIIIIl() and lIIIIllIllIlIIIIII(llIIlllllllIlIIIII, IIIlIIlIllIllIllll) and (not lIIIllllllllIIlIlI(IlIlIIIllIllllIlIl)):
        IIIIIllIIIIllIlllI('SUCCESS', f'Already joined in game {llIIlllllllIlIIIII} - no need to relaunch')
        lIIllllIllIlllIlll = IlIllIIIllIlIl()
        lIIllllllIllIlllIl = 0
        IIlIllllIlllllIlll = 'in_game'
        lIIllllllIIlIlIlll(IlIlIIIllIllllIlIl.get('discord_webhook'), f'Successfully rejoined game {llIIlllllllIlIIIII}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    IIIIIllIIIIllIlllI('INFO', f'Attempting to join game {llIIlllllllIlIIIII}')
    if not lIIlIlllIIIlIIlIIl(IlIlIIIllIllllIlIl):
        IIIIIllIIIIllIlllI('WARNING', 'Failed to close Roblox properly')
    llIIIIIlIllIII(3)
    llIllllllIlIlIllIl = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    if IIIlIIlIllIllIllll:
        IIIIIllIIIIllIlllI('INFO', 'Trying launch method: launch_via_browser')
        if lIlIlIllIlllIlIIIl(llIIlllllllIlIIIII, IIIlIIlIllIllIllll, IlIlIIIllIllllIlIl):
            if lllIlllllIIllIlIll(IlIlIIIllIllllIlIl, timeout=180):
                lIIllllIllIlllIlll = IlIllIIIllIlIl()
                IIIIIllIIIIllIlllI('SUCCESS', 'Successfully joined game using browser')
                llIllllllIlIlIllIl = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            else:
                IIIIIllIIIIllIlllI('WARNING', 'Game join timeout with browser launch')
        else:
            IIIIIllIIIIllIlllI('WARNING', 'Browser launch failed')
    else:
        IIIIIllIIIIllIlllI('INFO', 'Trying launch method: launch_via_deep_link')
        if IllllIlllIlIlIlllI(llIIlllllllIlIIIII, IIIlIIlIllIllIllll):
            if lllIlllllIIllIlIll(IlIlIIIllIllllIlIl, timeout=180):
                lIIllllIllIlllIlll = IlIllIIIllIlIl()
                IIIIIllIIIIllIlllI('SUCCESS', 'Successfully joined game using deep link')
                llIllllllIlIlIllIl = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            else:
                IIIIIllIIIIllIlllI('WARNING', 'Game join timeout with deep link')
        else:
            IIIIIllIIIIllIlllI('WARNING', 'Deep link launch failed')
    if llIllllllIlIlIllIl:
        lIIllllllIllIlllIl = 0
        IIlIllllIlllllIlll = 'in_game'
        lIIllllllIIlIlIlll(IlIlIIIllIllllIlIl.get('discord_webhook'), f'Successfully rejoined game {llIIlllllllIlIIIII}')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    else:
        lIIllllllIllIlllIl += 1
        IIlllIIllIlIIIllII = IlIllIIIllIlIl()
        IIIIIllIIIIllIlllI('ERROR', 'Game join attempt failed')
        return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def lllIlllllIIllIlIll(IlIlIIIllIllllIlIl: IIIllIlIllIIll, lIIllIlIlIIIlIIlIl: lllllllllllIIlI=180) -> llllllllllllIIl:
    lIllllIIIlIIlIlIII = IlIllIIIllIlIl()
    llIIlllllllIlIIIII = IlIlIIIllIllllIlIl.get('game_id')
    IIIlIIlIllIllIllll = IlIlIIIllIllllIlIl.get('private_server', '')
    llIIlIlIIllIIIIlll = IlIlIIIllIllllIlIl.get('game_load_delay', 90)
    IIIIIllIIIIllIlllI('INFO', f'Waiting {llIIlIlIIllIIIIlll} seconds for game to load before checking...')
    llIIIIIlIllIII(llIIlIlIIllIIIIlll)
    while IlIllIIIllIlIl() - lIllllIIIlIIlIlIII < lIIllIlIlIIIlIIlIl:
        if lIIIIllIllIlIIIIII(llIIlllllllIlIIIII, IIIlIIlIllIllIllll):
            IIIIIllIIIIllIlllI('SUCCESS', f'Detected successful join in game {llIIlllllllIlIIIII}')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
        lIlIIIIIIIIIIIIIlI = lIIIllllllllIIlIlI(IlIlIIIllIllllIlIl)
        if lIlIIIIIIIIIIIIIlI:
            IIIIIllIIIIllIlllI('WARNING', f'Detected error during join: {lIlIIIIIIIIIIIIIlI}')
            return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        llIIIIIlIllIII(5)
    IIIIIllIIIIllIlllI('INFO', 'Game join timeout, checking error states')
    lIlIIIIIIIIIIIIIlI = lIIIllllllllIIlIlI(IlIlIIIllIllllIlIl)
    if lIlIIIIIIIIIIIIIlI:
        IIIIIllIIIIllIlllI('WARNING', f'Detected error during join: {lIlIIIIIIIIIIIIIlI}')
    return llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

def IIIlIlIIIlIIlllIlI(IlIlIIIllIllllIlIl: IIIllIlIllIIll) -> None:
    global llIIIlIlllIIIlllII, lIIllllIllIlllIlll, lIIllllllIllIlllIl, lllIlllIlllIlIIIll, IIlIllllIlllllIlll
    llIIIlIlllIIIlllII = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    IIIIIllIIIIllIlllI('SUCCESS', 'Automation started successfully!')
    IIlIllllIIIlIllIIl = IlIlIIIllIllllIlIl.get('max_retries', 5)
    lIlIIlIIIIlllIlIIl = IlIlIIIllIllllIlIl.get('game_verification_interval', 300)
    IIIIIIlIIIllIllIII = IlIlIIIllIllllIlIl.get('check_delay', 60)
    if IlIlIIIllIllllIlIl.get('performance_mode', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)):
        IIIIIIlIIIllIllIII *= 2
        lIlIIlIIIIlllIlIIl *= 2
    while llIIIlIlllIIIlllII:
        try:
            llIIlllllllIlIIIII = IlIlIIIllIllllIlIl.get('game_id')
            llIlllIlllIlllIlIl = IlIllIIIllIlIl()
            if lllIlllIlllIlIIIll > 0 and llIlllIlllIlllIlIl - lllIlllIlllIlIIIll >= lIlIIlIIIIlllIlIIl:
                IIIIIllIIIIllIlllI('INFO', 'Periodic game verification check...')
                IIllIIlIIIIIllIlII = lIIIIllIllIlIIIIII(llIIlllllllIlIIIII, IlIlIIIllIllllIlIl.get('private_server', ''))
                if not IIllIIlIIIIIllIlII:
                    IIIIIllIIIIllIlllI('WARNING', 'No longer in target game during periodic check - rejoining...')
                    if IllllIllIllIlIllll(IlIlIIIllIllllIlIl):
                        lIIllllllIllIlllIl = 0
                    else:
                        lIIllllllIllIlllIl += 1
                else:
                    IIIIIllIIIIllIlllI('INFO', 'Still in correct game - continuing...')
                    lIIllllllIllIlllIl = 0
                lllIlllIlllIlIIIll = llIlllIlllIlllIlIl
                continue
            llIlIIIIlllllllIll = IIllIlllIIlIIIIIIl()
            IIllIIlIIIIIllIlII = lIIIIllIllIlIIIIII(llIIlllllllIlIIIII, IlIlIIIllIllllIlIl.get('private_server', '')) if llIlIIIIlllllllIll else llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
            lIlIIIIIIIIIIIIIlI = lIIIllllllllIIlIlI(IlIlIIIllIllllIlIl) if llIlIIIIlllllllIll else None
            if not llIlIIIIlllllllIll:
                if IIlIllllIlllllIlll == 'in_game':
                    IIIIIllIIIIllIlllI('WARNING', 'Crash detected - Roblox stopped running while in game')
                    lIIllllllIIlIlIlll(IlIlIIIllIllllIlIl.get('discord_webhook'), f'Crash detected in game {llIIlllllllIlIIIII}. Rejoining now.')
                    IIlIllllIlllllIlll = 'not_running'
                    if IllllIllIllIlIllll(IlIlIIIllIllllIlIl):
                        lIIllllllIllIlllIl = 0
                        lllIlllIlllIlIIIll = llIlllIlllIlllIlIl
                    else:
                        lIIllllllIllIlllIl += 1
                else:
                    IIIIIllIIIIllIlllI('INFO', 'Roblox not running - launching...')
                    if IllllIllIllIlIllll(IlIlIIIllIllllIlIl):
                        lIIllllllIllIlllIl = 0
                        lllIlllIlllIlIIIll = llIlllIlllIlllIlIl
                    else:
                        lIIllllllIllIlllIl += 1
            elif lIlIIIIIIIIIIIIIlI:
                IIIIIllIIIIllIlllI('WARNING', f'Error detected ({lIlIIIIIIIIIIIIIlI}) - restarting...')
                lIIllllllIIlIlIlll(IlIlIIIllIllllIlIl.get('discord_webhook'), f'Error {lIlIIIIIIIIIIIIIlI} detected in game {llIIlllllllIlIIIII}. Rejoining now.')
                IIlIllllIlllllIlll = 'error'
                if IllllIllIllIlIllll(IlIlIIIllIllllIlIl):
                    lIIllllllIllIlllIl = 0
                    lllIlllIlllIlIIIll = llIlllIlllIlllIlIl
                else:
                    lIIllllllIllIlllIl += 1
            elif not IIllIIlIIIIIllIlII:
                IIIIIllIIIIllIlllI('INFO', 'Not in target game - rejoining...')
                if IllllIllIllIlIllll(IlIlIIIllIllllIlIl):
                    lIIllllllIllIlllIl = 0
                    lllIlllIlllIlIIIll = llIlllIlllIlllIlIl
                else:
                    lIIllllllIllIlllIl += 1
            else:
                IIIIIllIIIIllIlllI('INFO', f'Already in game {llIIlllllllIlIIIII} and running normally - monitoring...')
                lIIllllllIllIlllIl = 0
                IIlIllllIlllllIlll = 'in_game'
                if lllIlllIlllIlIIIll == 0:
                    lllIlllIlllIlIIIll = llIlllIlllIlllIlIl
            if lIIllllllIllIlllIl >= IIlIllllIIIlIllIIl:
                IIIIIllIIIIllIlllI('ERROR', f'Too many consecutive failures ({lIIllllllIllIlllIl}) - continuing anyway...')
                lIIllllllIllIlllIl = 0
            IIIIIllIIIIllIlllI('INFO', f'Waiting {IIIIIIlIIIllIllIII} seconds before next check...')
            IllllIIlllIIIllllI = IllIllIIIlllll(0.8, 1.2) * IIIIIIlIIIllIllIII
            llIIIIIlIllIII(IllllIIlllIIIllllI)
        except llllllllllllIll:
            IIIIIllIIIIllIlllI('INFO', 'Automation interrupted by user')
            break
        except lllllllllllllII as lIlIIlIlIIllIllIIl:
            IIIIIllIIIIllIlllI('ERROR', f'Automation loop error: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
            llIIIIIlIllIII(10)
    llIIIlIlllIIIlllII = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    IIIIIllIIIIllIlllI('INFO', 'Automation stopped')

def lIlIIlIlllllIlIIII() -> None:
    IIlllllllIIIll('clear' if lIIIlIIlIlllII == 'posix' else 'cls')
    llllllllllllIII(f"\n{lIIllllllIlIllllll['HEADER']}{'=' * 50}")
    llllllllllllIII(f' ENHANCED ROBLOX AUTOMATION TOOL')
    llllllllllllIII(f"{'=' * 50}{lIIllllllIlIllllll['RESET']}")
    if IlIIlllIlIllIIIIll:
        llllllllllllIII(f"{lIIllllllIlIllllll['INFO']}Platform: {IlIIlllIlIllIIIIll['name']} ({IlIIlllIlIllIIIIll['type']}){lIIllllllIlIllllll['RESET']}")
        llllllllllllIII(f"{lIIllllllIlIllllll['INFO']}Root Access: {('Yes' if IlIIlllIlIllIIIIll.get('has_root') else 'Limited')}{lIIllllllIlIllllll['RESET']}")
    llllllllllllIII(f"\n{lIIllllllIlIllllll['CYAN']}1.{lIIllllllIlIllllll['RESET']} Configure Settings")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}2.{lIIllllllIlIllllll['RESET']} Start Automation")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}3.{lIIllllllIlIllllll['RESET']} Stop Automation")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}4.{lIIllllllIlIllllll['RESET']} Test Game Join")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}5.{lIIllllllIlIllllll['RESET']} View Current Config")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}6.{lIIllllllIlIllllll['RESET']} System Information")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}7.{lIIllllllIlIllllll['RESET']} Exit")
    if llIIIlIlllIIIlllII:
        llllllllllllIII(f"\n{lIIllllllIlIllllll['SUCCESS']}Status: Automation is RUNNING{lIIllllllIlIllllll['RESET']}")
    else:
        llllllllllllIII(f"\n{lIIllllllIlIllllll['WARNING']}Status: Automation is STOPPED{lIIllllllIlIllllll['RESET']}")
    if lIIllllIllIlllIlll:
        IlIIIIlllIIlIlIlll = IIIlIIIIllllIl.fromtimestamp(lIIllllIllIlllIlll).strftime('%Y-%m-%d %H:%M:%S')
        llllllllllllIII(f"{lIIllllllIlIllllll['INFO']}Last Game Join: {IlIIIIlllIIlIlIlll}{lIIllllllIlIllllll['RESET']}")
    if IIllllIlIlIlllllII:
        llllllllllllIII(f"{lIIllllllIlIllllll['WARNING']}Detected Error Codes: {', '.join(IIllllIlIlIlllllII)}{lIIllllllIlIllllll['RESET']}")

def IllllIlIIIIlIlIlIl() -> None:
    IlIlIIIllIllllIlIl = lIllIIIlIlIIIIlllI()
    llllllllllllIII(f"\n{lIIllllllIlIllllll['HEADER']}=== CONFIGURATION SETUP ==={lIIllllllIlIllllll['RESET']}")
    IIIIIlIIIIIIlllIIl = IlIlIIIllIllllIlIl.get('game_id', '')
    llllllllllllIII(f"\nCurrent Game ID: {(IIIIIlIIIIIIlllIIl if IIIIIlIIIIIIlllIIl else 'Not set')}")
    IIIlIIlIIIllIlIlII = lllllllllllIlIl('Enter new Game ID (or press Enter to keep current): ').strip()
    if IIIlIIlIIIllIlIlII:
        IlIlIIIllIllllIlIl['game_id'] = IIIlIIlIIIllIlIlII
    IlllIIlIlllIlIlIlI = IlIlIIIllIllllIlIl.get('private_server', '')
    llllllllllllIII(f"\nCurrent Private Server: {(IlllIIlIlllIlIlIlI if IlllIIlIlllIlIlIlI else 'Not set')}")
    llllllllllllIII('Enter the full private server URL')
    IllllIIlllIIIllIlI = lllllllllllIlIl('Enter Private Server link (or press Enter to keep current): ').strip()
    if IllllIIlllIIIllIlI:
        IlIlIIIllIllllIlIl['private_server'] = IllllIIlllIIIllIlI
    IlIlIlIIllIIlIlllI = IlIlIIIllIllllIlIl.get('check_delay', 60)
    llllllllllllIII(f'\nCurrent Check Delay: {IlIlIlIIllIIlIlllI} seconds')
    IIlIIllIIIllIIlIll = lllllllllllIlIl('Enter new Check Delay in seconds (or press Enter to keep current): ').strip()
    if IIlIIllIIIllIIlIll and IIlIIllIIIllIIlIll.isdigit():
        IlIlIIIllIllllIlIl['check_delay'] = lllllllllllIIlI(IIlIIllIIIllIIlIll)
    llllIllIllIlIllllI = IlIlIIIllIllllIlIl.get('game_load_delay', 90)
    llllllllllllIII(f'\nCurrent Game Load Delay: {llllIllIllIlIllllI} seconds')
    llllllllllllIII("This is how long to wait after launching before checking if you're in the game")
    IlIlIIllIlIIIlllII = lllllllllllIlIl('Enter new Game Load Delay in seconds (or press Enter to keep current): ').strip()
    if IlIlIIllIlIIIlllII and IlIlIIllIlIIIlllII.isdigit():
        IlIlIIIllIllllIlIl['game_load_delay'] = lllllllllllIIlI(IlIlIIllIlIIIlllII)
    lIIIIIIIIlIllIIllI = IlIlIIIllIllllIlIl.get('game_verification_interval', 300)
    llllllllllllIII(f'\nCurrent Game Verification Interval: {lIIIIIIIIlIllIIllI} seconds')
    llllllllllllIII("This is how often to check if you're still in the correct game (5 minutes = 300 seconds)")
    llIIIlIIIIlIlllIII = lllllllllllIlIl('Enter new Game Verification Interval in seconds (or press Enter to keep current): ').strip()
    if llIIIlIIIIlIlllIII and llIIIlIIIIlIlllIII.isdigit():
        IlIlIIIllIllllIlIl['game_verification_interval'] = lllllllllllIIlI(llIIIlIIIIlIlllIII)
    lllIlIlIlllllIlIIl = IlIlIIIllIllllIlIl.get('max_retries', 3)
    llllllllllllIII(f'\nCurrent Max Retries: {lllIlIlIlllllIlIIl}')
    llIIIlIIllIIIIlIlI = lllllllllllIlIl('Enter new Max Retries (or press Enter to keep current): ').strip()
    if llIIIlIIllIIIIlIlI and llIIIlIIllIIIIlIlI.isdigit():
        IlIlIIIllIllllIlIl['max_retries'] = lllllllllllIIlI(llIIIlIIllIIIIlIlI)
    lIlIllIIIlllIIlIIl = IlIlIIIllIllllIlIl.get('auto_rejoin', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    llllllllllllIII(f"\nCurrent Auto Rejoin: {('Enabled' if lIlIllIIIlllIIlIIl else 'Disabled')}")
    IlllllIlllIIIIlllI = lllllllllllIlIl('Enable Auto Rejoin? (y/n, or press Enter to keep current): ').strip().lower()
    if IlllllIlllIIIIlllI in ['y', 'yes']:
        IlIlIIIllIllllIlIl['auto_rejoin'] = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    elif IlllllIlllIIIIlllI in ['n', 'no']:
        IlIlIIIllIllllIlIl['auto_rejoin'] = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    IIllllllIIlIIllIII = llIlIlllIIllIlllIl()
    IllllllllIIIIlIIIl = IlIlIIIllIllllIlIl.get('browser_preference', 'auto')
    llllllllllllIII(f'\nCurrent Browser Preference: {IllllllllIIIIlIIIl}')
    llllllllllllIII(f"Available browsers: {(', '.join(IIllllllIIlIIllIII) if IIllllllIIlIIllIII else 'None detected')}")
    llllllllllllIII("Enter browser package name or 'auto' for automatic selection")
    IIlIIIIIIlIllIIIlI = lllllllllllIlIl('Enter Browser Preference (or press Enter to keep current): ').strip()
    if IIlIIIIIIlIllIIIlI:
        IlIlIIIllIllllIlIl['browser_preference'] = IIlIIIIIIlIllIIIlI
    IlIllIIIlllllIlIII = IlIlIIIllIllllIlIl.get('error_detection', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    llllllllllllIII(f"\nCurrent Error Detection: {('Enabled' if IlIllIIIlllllIlIII else 'Disabled')}")
    IllIllllIIIIlllIll = lllllllllllIlIl('Enable Error Detection? (y/n, or press Enter to keep current): ').strip().lower()
    if IllIllllIIIIlllIll in ['y', 'yes']:
        IlIlIIIllIllllIlIl['error_detection'] = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    elif IllIllllIIIIlllIll in ['n', 'no']:
        IlIlIIIllIllllIlIl['error_detection'] = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    lllIllllllIIlIIlll = IlIlIIIllIllllIlIl.get('performance_mode', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0))
    llllllllllllIII(f"\nCurrent Performance Mode: {('Enabled' if lllIllllllIIlIIlll else 'Disabled')}")
    IllIIIllIIIIlIIIIl = lllllllllllIlIl('Enable Performance Mode (lower CPU)? (y/n, or press Enter to keep current): ').strip().lower()
    if IllIIIllIIIIlIIIIl in ['y', 'yes']:
        IlIlIIIllIllllIlIl['performance_mode'] = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    elif IllIIIllIIIIlIIIIl in ['n', 'no']:
        IlIlIIIllIllllIlIl['performance_mode'] = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    IIlIllIIlIIIlllllI = IlIlIIIllIllllIlIl.get('discord_webhook', '')
    llllllllllllIII(f"\nCurrent Discord Webhook: {(IIlIllIIlIIIlllllI if IIlIllIIlIIIlllllI else 'Not set')}")
    IlIllIlllIllIIIIlI = lllllllllllIlIl('Enter Discord Webhook URL (or press Enter to keep current): ').strip()
    if IlIllIlllIllIIIIlI:
        IlIlIIIllIllllIlIl['discord_webhook'] = IlIllIlllIllIIIIlI
    if IIIIlIIlIIllIIlIlI(IlIlIIIllIllllIlIl):
        IIIIIllIIIIllIlllI('SUCCESS', 'Configuration saved successfully!')
    else:
        IIIIIllIIIIllIlllI('ERROR', 'Failed to save configuration!')
    lllllllllllIlIl('\nPress Enter to continue...')

def lIllIIIlllllIIlIll() -> None:
    IlIlIIIllIllllIlIl = lIllIIIlIlIIIIlllI()
    llllllllllllIII(f"\n{lIIllllllIlIllllll['HEADER']}=== CURRENT CONFIGURATION ==={lIIllllllIlIllllll['RESET']}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Game ID:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('game_id', 'Not set')}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Private Server:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('private_server', 'Not set')}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Check Delay:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('check_delay', 60)} seconds")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Game Load Delay:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('game_load_delay', 90)} seconds")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Game Verification Interval:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('game_verification_interval', 300)} seconds")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Max Retries:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('max_retries', 3)}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Auto Rejoin:{lIIllllllIlIllllll['RESET']} {('Enabled' if IlIlIIIllIllllIlIl.get('auto_rejoin', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)) else 'Disabled')}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Browser Preference:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('browser_preference', 'auto')}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Error Detection:{lIIllllllIlIllllll['RESET']} {('Enabled' if IlIlIIIllIllllIlIl.get('error_detection', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)) else 'Disabled')}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Performance Mode:{lIIllllllIlIllllll['RESET']} {('Enabled' if IlIlIIIllIllllIlIl.get('performance_mode', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)) else 'Disabled')}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Discord Webhook:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('discord_webhook', 'Not set')}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Game Validation:{lIIllllllIlIllllll['RESET']} {('Enabled' if IlIlIIIllIllllIlIl.get('game_validation', llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)) else 'Disabled')}")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Launch Delay:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('launch_delay', 300)} seconds")
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Retry Delay:{lIIllllllIlIllllll['RESET']} {IlIlIIIllIllllIlIl.get('retry_delay', 15)} seconds")
    lllllllllllIlIl('\nPress Enter to continue...')

def IIIIlIllllIIIIIIlI() -> None:
    IlIlIIIllIllllIlIl = lIllIIIlIlIIIIlllI()
    llIIlllllllIlIIIII = IlIlIIIllIllllIlIl.get('game_id')
    if not llIIlllllllIlIIIII:
        IIIIIllIIIIllIlllI('ERROR', 'No game ID configured. Please configure settings first.')
        lllllllllllIlIl('Press Enter to continue...')
        return
    IIIIIllIIIIllIlllI('INFO', f'Testing game join for Game ID: {llIIlllllllIlIIIII}')
    IIIIIllIIIIllIlllI('INFO', 'This will close Roblox and attempt to join the game...')
    IllIIllIIIIllIIllI = lllllllllllIlIl('Continue with test? (y/n): ').strip().lower()
    if IllIIllIIIIllIIllI not in ['y', 'yes']:
        return
    llIllllllIlIlIllIl = IllllIllIllIlIllll(IlIlIIIllIllllIlIl)
    if llIllllllIlIlIllIl:
        IIIIIllIIIIllIlllI('SUCCESS', 'Game join test completed successfully!')
    else:
        IIIIIllIIIIllIlllI('ERROR', 'Game join test failed!')
    lllllllllllIlIl('\nPress Enter to continue...')

def lllIlllIlllIIllIII() -> None:
    llllllllllllIII(f"\n{lIIllllllIlIllllll['HEADER']}=== SYSTEM INFORMATION ==={lIIllllllIlIllllll['RESET']}")
    if IlIIlllIlIllIIIIll:
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Platform Type:{lIIllllllIlIllllll['RESET']} {IlIIlllIlIllIIIIll['type']}")
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Platform Name:{lIIllllllIlIllllll['RESET']} {IlIIlllIlIllIIIIll['name']}")
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Root Access:{lIIllllllIlIllllll['RESET']} {('Available' if IlIIlllIlIllIIIIll.get('has_root') else 'Limited')}")
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}ADB Support:{lIIllllllIlIllllll['RESET']} {('Yes' if IlIIlllIlIllIIIIll.get('use_adb') else 'No')}")
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Shell Prefix:{lIIllllllIlIllllll['RESET']} {IlIIlllIlIllIIIIll.get('shell_prefix', 'None')}")
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Process Check Method:{lIIllllllIlIllllll['RESET']} {IlIIlllIlIllIIIIll.get('process_check_method', 'Unknown')}")
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Browser Launch Method:{lIIllllllIlIllllll['RESET']} {IlIIlllIlIllIIIIll.get('browser_launch', 'Unknown')}")
    lllIIlllIIIIIlIlll = lllllllIlIIIIIIlII()
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Roblox Installed:{lIIllllllIlIllllll['RESET']} {('Yes' if lllIIlllIIIIIlIlll else 'No')}")
    if lllIIlllIIIIIlIlll:
        llIlIIIIlllllllIll = IIllIlllIIlIIIIIIl()
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Roblox Running:{lIIllllllIlIllllll['RESET']} {('Yes' if llIlIIIIlllllllIll else 'No')}")
    IIllllllIIlIIllIII = llIlIlllIIllIlllIl()
    llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Available Browsers:{lIIllllllIlIllllll['RESET']} {(', '.join(IIllllllIIlIIllIII) if IIllllllIIlIIllIII else 'None')}")
    try:
        IIIIlIIlllIIllIllI = IIIIIIIIIllIIllIII('getprop ro.build.version.release', platform_info=IlIIlllIlIllIIIIll)
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Android Version:{lIIllllllIlIllllll['RESET']} {(IIIIlIIlllIIllIllI if IIIIlIIlllIIllIllI else 'Unknown')}")
    except:
        pass
    try:
        IlllIlllIlIlllIllI = IIIIIIIIIllIIllIII('getprop ro.product.model', platform_info=IlIIlllIlIllIIIIll)
        llllllllllllIII(f"{lIIllllllIlIllllll['CYAN']}Device Model:{lIIllllllIlIllllll['RESET']} {(IlllIlllIlIlllIllI if IlllIlllIlIlllIllI else 'Unknown')}")
    except:
        pass
    lllllllllllIlIl('\nPress Enter to continue...')

def llIllIlIIllIllIIIl() -> None:
    global IlIIlllIlIllIIIIll, llIIIlIlllIIIlllII
    try:
        IIlllllllIIIll('clear' if lIIIlIIlIlllII == 'posix' else 'cls')
        llllllllllllIII(f"{lIIllllllIlIllllll['HEADER']}")
        llllllllllllIII('╔══════════════════════════════════════════════════════════════╗')
        llllllllllllIII('║           ENHANCED ROBLOX AUTOMATION TOOL                    ║')
        llllllllllllIII('║        Supports: UGPHONE, VSPHONE, REDFINGER                 ║')
        llllllllllllIII('║            Standard Android & Emulators                      ║')
        llllllllllllIII('╚══════════════════════════════════════════════════════════════╝')
        llllllllllllIII(f"{lIIllllllIlIllllll['RESET']}")
        lIIIlIlllIIllIllIl = IIlIllIllIllIlIIIl()
        IlIIlllIlIllIIIIll = lIIIlIlllIIllIllIl.llIIIIIllIllIlIIlI()
        if not lllllllIlIIIIIIlII():
            IIIIIllIIIIllIlllI('ERROR', 'Roblox is not installed or not accessible!')
            IIIIIllIIIIllIlllI('INFO', 'Please install Roblox and ensure proper permissions.')
            IlIllIlllIIIll(1)
        lIllIlllIllIllIIlI = None
        while llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            try:
                lIlIIlIlllllIlIIII()
                llIlIlllIIIIllIlIl = lllllllllllIlIl(f"\n{lIIllllllIlIllllll['CYAN']}Enter your choice (1-7): {lIIllllllIlIllllll['RESET']}").strip()
                if llIlIlllIIIIllIlIl == '1':
                    IllllIlIIIIlIlIlIl()
                elif llIlIlllIIIIllIlIl == '2':
                    if llIIIlIlllIIIlllII:
                        IIIIIllIIIIllIlllI('WARNING', 'Automation is already running!')
                        lllllllllllIlIl('Press Enter to continue...')
                    else:
                        IlIlIIIllIllllIlIl = lIllIIIlIlIIIIlllI()
                        if not IlIlIIIllIllllIlIl.get('game_id'):
                            IIIIIllIIIIllIlllI('ERROR', 'No game ID configured! Please configure settings first.')
                            lllllllllllIlIl('Press Enter to continue...')
                        else:
                            lIllIlllIllIllIIlI = lIllllllIIIlll(target=IIIlIlIIIlIIlllIlI, args=(IlIlIIIllIllllIlIl,), daemon=llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                            lIllIlllIllIllIIlI.start()
                elif llIlIlllIIIIllIlIl == '3':
                    if llIIIlIlllIIIlllII:
                        IIIIIllIIIIllIlllI('INFO', 'Stopping automation...')
                        llIIIlIlllIIIlllII = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
                        if lIllIlllIllIllIIlI:
                            lIllIlllIllIllIIlI.join(timeout=5)
                        IIIIIllIIIIllIlllI('SUCCESS', 'Automation stopped!')
                    else:
                        IIIIIllIIIIllIlllI('WARNING', 'Automation is not running!')
                    lllllllllllIlIl('Press Enter to continue...')
                elif llIlIlllIIIIllIlIl == '4':
                    IIIIlIllllIIIIIIlI()
                elif llIlIlllIIIIllIlIl == '5':
                    lIllIIIlllllIIlIll()
                elif llIlIlllIIIIllIlIl == '6':
                    lllIlllIlllIIllIII()
                elif llIlIlllIIIIllIlIl == '7':
                    if llIIIlIlllIIIlllII:
                        IIIIIllIIIIllIlllI('INFO', 'Stopping automation before exit...')
                        llIIIlIlllIIIlllII = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
                        if lIllIlllIllIllIIlI:
                            lIllIlllIllIllIIlI.join(timeout=5)
                    IIIIIllIIIIllIlllI('INFO', 'Thank you for using Enhanced Roblox Automation Tool!')
                    break
                else:
                    IIIIIllIIIIllIlllI('WARNING', 'Invalid choice! Please enter 1-7.')
                    lllllllllllIlIl('Press Enter to continue...')
            except llllllllllllIll:
                IIIIIllIIIIllIlllI('INFO', '\nExiting...')
                if llIIIlIlllIIIlllII:
                    llIIIlIlllIIIlllII = llllllllllllIIl(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
                break
            except lllllllllllllII as lIlIIlIlIIllIllIIl:
                IIIIIllIIIIllIlllI('ERROR', f'Menu error: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
                lllllllllllIlIl('Press Enter to continue...')
    except lllllllllllllII as lIlIIlIlIIllIllIIl:
        IIIIIllIIIIllIlllI('ERROR', f'Critical error: {lllllllllllIIIl(lIlIIlIlIIllIllIIl)}')
        IlIllIlllIIIll(1)
if lllllllllllllIl == '__main__':
    llIllIlIIllIllIIIl()
