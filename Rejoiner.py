#!/usr/bin/env python3
'\nEnhanced Roblox Automation Tool (Rejoiner.py)\nSupports: UGPHONE, VSPHONE, REDFINGER, Standard Android/Emulators\nAuthor: Optimized for game monitoring and private server joining\n'
_A3='logcat -c'
_A2='mResumedActivity'
_A1="dumpsys activity | grep -A 10 -B 5 'mResumedActivity'"
_A0='force_kill_delay'
_z='retry_delay'
_y='launch_delay'
_x='game_validation'
_w='%Y-%m-%d %H:%M:%S'
_v='\nPress Enter to continue...'
_u='yes'
_t='Yes'
_s='in_game'
_r='test'
_q='echo test'
_p='-c'
_o='ps_grep'
_n='Unknown'
_m='game_verification_interval'
_l='game_load_delay'
_k='browser_preference'
_j='auto_rejoin'
_i='max_retries'
_h='check_delay'
_g='Press Enter to continue...'
_f='Not set'
_e='auto'
_d='performance_mode'
_c='error_detection'
_b='redfinger'
_a='vsphone'
_Z='ugphone'
_Y='browser_launch'
_X='use_adb'
_W='wait_time'
_V='Disabled'
_U='Enabled'
_T='process_check_method'
_S='solution'
_R='HEADER'
_Q='discord_webhook'
_P='private_server'
_O='has_root'
_N='game_id'
_M='shell_prefix'
_L='type'
_K=None
_J='SUCCESS'
_I='name'
_H='DEBUG'
_G='ERROR'
_F='WARNING'
_E='CYAN'
_D='INFO'
_C='RESET'
_B=False
_A=True
import requests,time,os,json,subprocess,urllib.parse,re,threading,sys,logging,random
from datetime import datetime
from typing import Dict,List,Optional,Any
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler('/sdcard/roblox_automation.log'),logging.StreamHandler()])
logger=logging.getLogger('Rejoiner')
COLORS={_C:'\x1b[0m',_D:'\x1b[94m',_J:'\x1b[92m',_F:'\x1b[93m',_G:'\x1b[91m','BOLD':'\x1b[1m',_E:'\x1b[96m',_R:'\x1b[95m',_H:'\x1b[90m'}
CONFIG_FILE='/sdcard/roblox_config.json'
ROBLOX_PACKAGE='com.roblox.client'
BROWSER_PACKAGES=['com.android.chrome','com.sec.android.app.sbrowser','com.google.android.webview','org.mozilla.firefox','com.opera.browser','com.brave.browser','com.microsoft.emmx','com.vivaldi.browser']
ROBLOX_ERROR_DATABASE={'267':{_I:'Cannot rejoin game',_S:'Wait 30 seconds before retry',_W:30},'279':{_I:'Server full',_S:'Try different server or wait',_W:15},'292':{_I:'Kicked from game',_S:'Check if banned, wait 5 minutes',_W:300},'529':{_I:'Connection lost',_S:'Check network, restart if persistent',_W:10},'601':{_I:'Place unavailable',_S:'Game might be updating, check later',_W:60}}
automation_running=_B
platform_info=_K
last_game_join_time=_K
error_codes_detected=set()
consecutive_failures=0
last_error_time=0
last_game_verification_time=0
last_known_state='unknown'
class PlatformDetector:
	def __init__(A):A.detected_platform=_K
	def detect_platform(A):
		F='standard';E='pidof';D='su -c';C='intent';B='special_commands'
		try:
			if A._is_ugphone():A.detected_platform={_L:_Z,_I:'UGPHONE',_O:A._check_root_ugphone(),_X:_B,_M:'',B:_A,_T:_o,_Y:C};print_formatted(_D,f"Platform detected: {A.detected_platform[_I]}");return A.detected_platform
			if A._is_vsphone():A.detected_platform={_L:_a,_I:'VSPHONE',_O:A._check_root_vsphone(),_X:_B,_M:'',B:_A,_T:_o,_Y:C};print_formatted(_D,f"Platform detected: {A.detected_platform[_I]}");return A.detected_platform
			if A._is_redfinger():A.detected_platform={_L:_b,_I:'REDFINGER',_O:A._check_root_redfinger(),_X:_A,_M:D,B:_B,_T:E,_Y:C};print_formatted(_D,f"Platform detected: {A.detected_platform[_I]}");return A.detected_platform
			A.detected_platform={_L:F,_I:'Standard Android',_O:A._check_root_standard(),_X:_A,_M:D,B:_B,_T:E,_Y:C};print_formatted(_D,f"Platform detected: {A.detected_platform[_I]}");return A.detected_platform
		except Exception as G:print_formatted(_G,f"Platform detection error: {str(G)}");A.detected_platform={_L:F,_I:'Standard Android (Fallback)',_O:_B,_X:_B,_M:'',B:_B,_T:_o,_Y:C};return A.detected_platform
	def _is_ugphone(A):
		try:
			B=['/system/bin/ugphone','/system/app/UGPhone','/data/local/tmp/ugphone','/system/priv-app/UGPhone','/system/framework/ugphone.jar','/system/etc/ugphone','/vendor/bin/ugphone','/system/bin/ug_phone']
			for C in B:
				if os.path.exists(C):return _A
			D=A._get_build_prop();E=[_Z,'ug_phone','cloudphone','universal.global.phone','ugcloud']
			for F in E:
				if F.lower()in D.lower():return _A
			G=A._get_env_vars()
			if any(_Z in A.lower()for A in G):return _A
			H=A._get_running_processes()
			if any(_Z in A.lower()for A in H):return _A
			return _B
		except:return _B
	def _is_vsphone(A):
		try:
			B=['/system/bin/vsphone','/system/app/VSPhone','/data/local/tmp/vsphone','/system/priv-app/VSPhone','/system/framework/vsphone.jar','/system/etc/vsphone','/vendor/bin/vsphone','/system/bin/vs_phone']
			for C in B:
				if os.path.exists(C):return _A
			D=A._get_build_prop();E=[_a,'vs_phone','virtualphone','virtual.space','vspace']
			for F in E:
				if F.lower()in D.lower():return _A
			G=A._get_env_vars()
			if any(_a in A.lower()for A in G):return _A
			H=A._get_running_processes()
			if any(_a in A.lower()for A in H):return _A
			return _B
		except:return _B
	def _is_redfinger(A):
		try:
			B=['/system/bin/redfinger','/system/app/RedFinger','/data/local/tmp/redfinger','/system/priv-app/RedFinger','/system/framework/redfinger.jar','/system/etc/redfinger','/vendor/bin/redfinger','/system/bin/red_finger']
			for C in B:
				if os.path.exists(C):return _A
			D=A._get_build_prop();E=[_b,'red_finger','redcloud','red.finger','rfcloud']
			for F in E:
				if F.lower()in D.lower():return _A
			G=A._get_env_vars()
			if any(_b in A.lower()for A in G):return _A
			H=A._get_running_processes()
			if any(_b in A.lower()for A in H):return _A
			return _B
		except:return _B
	def _get_build_prop(B):
		try:A=subprocess.run(['cat','/system/build.prop'],capture_output=_A,text=_A,timeout=5);return A.stdout
		except:return''
	def _get_env_vars(B):
		try:A=subprocess.run(['env'],capture_output=_A,text=_A,timeout=5);return A.stdout.split('\n')
		except:return[]
	def _get_running_processes(B):
		try:A=subprocess.run(['ps','-A'],capture_output=_A,text=_A,timeout=5);return A.stdout.split('\n')
		except:return[]
	def _check_root_standard(B):
		try:A=subprocess.run(['su',_p,_q],capture_output=_A,text=_A,timeout=5);return _r in A.stdout
		except:return _B
	def _check_root_ugphone(A):
		try:
			if A._check_root_standard():return _A
			B=subprocess.run(['ugphone_su',_p,_q],capture_output=_A,text=_A,timeout=5);return _r in B.stdout
		except:return _B
	def _check_root_vsphone(A):
		try:
			if A._check_root_standard():return _A
			B=subprocess.run(['vsphone_su',_p,_q],capture_output=_A,text=_A,timeout=5);return _r in B.stdout
		except:return _B
	def _check_root_redfinger(A):
		try:
			if A._check_root_standard():return _A
			B=subprocess.run(['redfinger_su',_p,_q],capture_output=_A,text=_A,timeout=5);return _r in B.stdout
		except:return _B
def print_formatted(level,message):B=message;A=level;C=datetime.now().strftime(_w);D={_D:_D,_J:'OK',_F:'WARN',_G:_G,_R:'====',_H:_H}.get(A,A);E=COLORS.get(A,COLORS[_C]);print(f"{E}{C} [{D}] {B}{COLORS[_C]}");logger.log(getattr(logging,A.upper(),logging.INFO),B)
def run_shell_command(command,timeout=10,platform_info=_K):
	B=platform_info;A=command
	try:
		if B and B.get(_M):
			if B[_M]:D=B[_M].split()+[A]
			else:D=A.split()
		else:D=A.split()
		C=subprocess.run(D,capture_output=_A,text=_A,timeout=timeout)
		if C.stderr and'permission denied'not in C.stderr.lower():print_formatted(_H,f"Command stderr: {C.stderr.strip()}")
		return C.stdout.strip()
	except subprocess.TimeoutExpired:print_formatted(_F,f"Command timeout: {A}");return''
	except Exception as E:print_formatted(_G,f"Command failed: {A} - {str(E)}");return''
def load_config():
	A={'accounts':[],_N:'',_P:'',_h:60,'active_account':'','check_method':'both',_i:3,_x:_A,_y:300,_z:15,_A0:10,'minimize_crashes':_A,'launch_attempts':1,'cooldown_period':120,_j:_A,'ui_timeout':30,'verbose_logging':_A,_k:_e,_c:_A,_d:_B,_l:90,_m:300,'error_wait_times':{'267':30,'279':15,'292':300,'529':10,'601':60},_Q:''}
	try:
		if not os.path.exists(CONFIG_FILE):
			with open(CONFIG_FILE,'w')as B:json.dump(A,B,indent=4)
			run_shell_command(f"chmod 644 {CONFIG_FILE}",platform_info=platform_info);print_formatted(_D,'Created new config file');return A
		with open(CONFIG_FILE,'r')as B:
			C=json.load(B)
			for(D,E)in A.items():
				if D not in C:C[D]=E
			return C
	except Exception as F:print_formatted(_G,f"Config load error: {F}");return A
def save_config(config):
	try:
		with open(CONFIG_FILE,'w')as A:json.dump(config,A,indent=4)
		run_shell_command(f"chmod 644 {CONFIG_FILE}",platform_info=platform_info);print_formatted(_J,'Config saved');return _A
	except Exception as B:print_formatted(_G,f"Config save error: {B}");return _B
def send_discord_alert(webhook_url,message):
	A=webhook_url
	if not A:return
	try:
		C={'content':message};B=requests.post(A,json=C)
		if B.status_code!=204:print_formatted(_F,f"Discord alert failed: {B.status_code}")
	except Exception as D:print_formatted(_G,f"Discord alert error: {str(D)}")
def verify_roblox_installation():
	B='versionName='
	try:
		C=run_shell_command(f"pm list packages {ROBLOX_PACKAGE}",platform_info=platform_info)
		if ROBLOX_PACKAGE not in C:print_formatted(_G,'Roblox not installed.');return _B
		A=run_shell_command(f"dumpsys package {ROBLOX_PACKAGE} | grep versionName",platform_info=platform_info)
		if A:D=A.split(B)[1].split()[0]if B in A else _n;print_formatted(_D,f"Roblox version: {D}")
		return _A
	except Exception as E:print_formatted(_G,f"Roblox verification error: {E}");return _B
def is_roblox_running(retries=2,delay=1):
	B=delay;A=retries
	for C in range(A):
		try:
			if platform_info and platform_info.get(_T)==_o:
				E=run_shell_command(f"ps -A | grep {ROBLOX_PACKAGE} | grep -v grep",platform_info=platform_info)
				if E.strip():print_formatted(_H,'Roblox process found via ps+grep');return _A
			else:
				F=run_shell_command(f"pidof {ROBLOX_PACKAGE}",platform_info=platform_info)
				if F.strip():print_formatted(_H,'Roblox PID found via pidof');return _A
			D=run_shell_command(_A1,platform_info=platform_info)
			if ROBLOX_PACKAGE in D and _A2 in D:print_formatted(_H,'Roblox is resumed and focused');return _A
			G=run_shell_command('ps -A',platform_info=platform_info)
			if ROBLOX_PACKAGE in G:print_formatted(_H,'Roblox process found in all processes list');return _A
			if C<A-1:time.sleep(B)
		except Exception as H:
			print_formatted(_G,f"Roblox running check error: {str(H)}")
			if C<A-1:time.sleep(B)
	print_formatted(_H,'Roblox process not found');return _B
def close_roblox(config=_K):
	A=config
	try:
		print_formatted(_D,'Closing Roblox...');run_shell_command('input keyevent KEYCODE_HOME',platform_info=platform_info);time.sleep(2);run_shell_command(f"am force-stop {ROBLOX_PACKAGE}",platform_info=platform_info);time.sleep(2)
		if platform_info and platform_info[_L]in[_Z,_a,_b]:run_shell_command(f"pkill -f {ROBLOX_PACKAGE}",platform_info=platform_info)
		else:run_shell_command(f"killall -9 {ROBLOX_PACKAGE}",platform_info=platform_info)
		C=A.get(_A0,10)if A else 10;time.sleep(C)
		if is_roblox_running():print_formatted(_F,'Roblox still running, clearing cache...');run_shell_command(f"pm clear {ROBLOX_PACKAGE}",platform_info=platform_info);time.sleep(5)
		B=not is_roblox_running()
		if B:print_formatted(_J,'Roblox closed successfully')
		else:print_formatted(_G,'Failed to close Roblox completely')
		return B
	except Exception as D:print_formatted(_G,f"Failed to close Roblox: {str(D)}");return _B
def get_main_activity():
	B='.MainActivity'
	try:
		E=run_shell_command(f"dumpsys package {ROBLOX_PACKAGE} | grep -A 5 'android.intent.action.MAIN'",platform_info=platform_info);C=re.search('com\\.roblox\\.client/(\\.[A-Za-z0-9.]+)',E)
		if C:D=C.group(1);print_formatted(_H,f"Detected main activity: {D}");return D
		F=['.startup.ActivitySplash',B,'.HomeActivity']
		for A in F:
			G=run_shell_command(f"dumpsys package {ROBLOX_PACKAGE} | grep {A}",platform_info=platform_info)
			if A in G:return A
		return B
	except Exception as H:print_formatted(_F,f"Main activity detection error: {str(H)}");return B
def build_game_url(game_id,private_server=''):
	B=game_id;A=private_server
	try:
		if A:
			if not A.startswith(('http://','https://')):A=f"https://{A}"
			print_formatted(_D,f"Using provided private server URL: {A}");return A
		C=f"roblox://experiences/start?placeId={B}";print_formatted(_D,f"Built game deep link URL: {C}");return C
	except Exception as D:print_formatted(_G,f"URL build error: {D}");return f"roblox://experiences/start?placeId={B}"
def extract_private_server_code(link):
	A=link
	try:
		E=['privateServerLinkCode=([^&]+)','share\\?code=([^&]+)','linkCode=([^&]+)','code=([^&]+)']
		for F in E:
			B=re.search(F,A)
			if B:return B.group(1)
		for C in['privateServerLinkCode=','share?code=','&linkCode=','=']:
			if C in A:
				D=A.split(C)[1].split('&')[0].strip()
				if D:return D
		return
	except:return
def get_available_browsers():
	B=[]
	for A in BROWSER_PACKAGES:
		C=run_shell_command(f"pm list packages {A}",platform_info=platform_info)
		if A in C:B.append(A)
	return B
def launch_via_deep_link(game_id,private_server=''):
	B=private_server;A=game_id
	try:
		if B:print_formatted(_D,'Skipping deep link for private server, using browser method');return _B
		print_formatted(_D,f"Launching via deep link: Game ID {A}");C=build_game_url(A,B);D=f'am start -a android.intent.action.VIEW -d "{C}"';G=run_shell_command(D,platform_info=platform_info);E=time.time()
		while time.time()-E<120:
			if is_roblox_running():print_formatted(_J,'Roblox launched via deep link');time.sleep(10);return _A
			time.sleep(3)
		print_formatted(_F,'Deep link launched but Roblox not running after extended wait');return _B
	except Exception as F:print_formatted(_G,f"Deep link launch failed: {str(F)}");return _B
def launch_via_browser(game_id,private_server='',config=_K):
	G=config;F=private_server;E=game_id
	try:
		if not F:print_formatted(_F,'No private server link provided for browser launch');return _B
		print_formatted(_D,f"Launching via browser: Game ID {E}");A=build_game_url(E,F);B=G.get(_k,_e)if G else _e;C=get_available_browsers()
		if B!=_e and B in C:D=f'am start -a android.intent.action.VIEW -d "{A}" {B}'
		elif C:D=f'am start -a android.intent.action.VIEW -d "{A}" {C[0]}'
		else:D=f'am start -a android.intent.action.VIEW -d "{A}"'
		J=run_shell_command(D,platform_info=platform_info);H=time.time()
		while time.time()-H<120:
			if is_roblox_running():print_formatted(_J,'Roblox launched via browser');time.sleep(10);return _A
			time.sleep(3)
		print_formatted(_F,'Browser launch initiated but Roblox not running after extended wait');return _B
	except Exception as I:print_formatted(_G,f"Browser launch failed: {str(I)}");return _B
def is_in_game(game_id,private_server=''):
	E=private_server;A=game_id
	try:
		if not is_roblox_running():print_formatted(_H,'Roblox not running - not in game');return _B
		if platform_info and platform_info[_L]in[_Z,_a,_b]:
			F=run_shell_command(_A1,platform_info=platform_info)
			if ROBLOX_PACKAGE in F and _A2 in F:print_formatted(_H,'Roblox is resumed and focused - likely in game');return _A
			K=run_shell_command("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'",platform_info=platform_info)
			if ROBLOX_PACKAGE in K:print_formatted(_H,'Roblox is in focus - likely in game');return _A
			print_formatted(_H,'Assuming in game due to Roblox running on cloud phone');return _A
		B=run_shell_command(f"dumpsys gfxinfo {ROBLOX_PACKAGE} | grep -i 'draw\\|render\\|texture'",platform_info=platform_info)
		if B and('draw'in B.lower()or'render'in B.lower()):print_formatted(_H,'Game rendering detected - likely in game');return _A
		C=run_shell_command(f"dumpsys activity processes {ROBLOX_PACKAGE} | grep -E 'state\\|procstate'",platform_info=platform_info)
		if C and('foreground'in C.lower()or'top'in C.lower()):print_formatted(_H,'Roblox in foreground state - likely in game');return _A
		run_shell_command(_A3,platform_info=platform_info);time.sleep(2);G=[f"place.*{A}",f"game.*{A}",f"join.*{A}",'loading.*complete','game.*start','experience.*load','character.*load','player.*join','render.*start','physics.*start','workspace.*load','joined game','successfully joined']
		if E:
			D=extract_private_server_code(E)
			if D:G.extend([f"privateServer.*{D}",f"linkCode.*{D}",'private server.*joined'])
		L=f"logcat -d | grep -iE '{'|'.join(G)}' | grep -v su | head -20";H=run_shell_command(L,platform_info=platform_info)
		if H.strip():print_formatted(_H,f"Game activity logs found: {H.strip()}");return _A
		I=run_shell_command(f"dumpsys meminfo {ROBLOX_PACKAGE} | grep 'TOTAL'",platform_info=platform_info)
		if I:
			try:
				J=int(''.join(filter(str.isdigit,I.split()[0])))
				if J>500000:print_formatted(_H,f"High memory usage ({J} KB) - likely in game");return _A
			except:pass
		print_formatted(_H,'No strong indicators of being in game found');return _B
	except Exception as M:print_formatted(_G,f"Game detection error: {str(M)}");return _B
def detect_roblox_error_codes():
	try:
		D=['error code[:\\s]*(\\d+)','error.*code[:\\s]*(\\d+)','code[:\\s]*(\\d+).*error','err.*code[:\\s]*(\\d+)','error\\s+(\\d+)','code\\s+(\\d+).*failed','failed.*code\\s+(\\d+)'];A=[];E=run_shell_command('logcat -d | grep -i error | grep -v su | head -20',platform_info=platform_info)
		for B in D:C=re.findall(B,E,re.IGNORECASE);A.extend(C)
		F=run_shell_command('logcat -d | grep -i roblox | grep -i error | grep -v su | head -10',platform_info=platform_info)
		for B in D:C=re.findall(B,F,re.IGNORECASE);A.extend(C)
		return list(set(A))
	except Exception as G:print_formatted(_G,f"Error code detection failed: {str(G)}");return[]
def check_error_states(config=_K):
	M='frozen';L='unexpected client';K='banned';J='kicked';I='crash';C=config
	try:
		if not C or not C.get(_c,_A):return
		N=run_shell_command('uiautomator dump /sdcard/ui_dump.xml && cat /sdcard/ui_dump.xml',platform_info=platform_info);O=['error',I,'disconnect',J,K,'failed','unable','sorry','oops','problem','restart','rejoin','retry','close','exit',L,'exploiting','same account','idle','anti-cheat','connection lost','reconnect']
		if any(A in N.lower()for A in O):print_formatted(_F,'Error dialog detected in UI');return'ui_error'
		B=run_shell_command("dumpsys activity | grep -i 'anr'",platform_info=platform_info)
		if B and ROBLOX_PACKAGE in B:print_formatted(_F,f"ANR detected: {B.strip()}");return M
		if platform_info.get(_O):
			D=run_shell_command('ls -l /data/anr/ | grep anr',platform_info=platform_info)
			if D and ROBLOX_PACKAGE in D:print_formatted(_F,'ANR trace files detected for Roblox');return M
		run_shell_command(_A3,platform_info=platform_info);time.sleep(1);P=['fatal','exception','sigsegv','segmentation','native crash','system_server','am_crash','beginning of crash','backtrace',L,J,K,'disconnected'];E=run_shell_command(f"logcat -d | grep -iE '{'|'.join(P)}' | grep -v su | head -10",platform_info=platform_info)
		if E.strip():print_formatted(_F,f"Crash detected in logs: {E.strip()}");return I
		F=run_shell_command("logcat -d | grep -iE 'timeout|disconnect|network|connection|idle' | grep -v su | head -5",platform_info=platform_info)
		if F.strip():print_formatted(_F,f"Network issues: {F.strip()}");return'network_error'
		G=detect_roblox_error_codes()
		if G:
			for A in G:
				if A not in error_codes_detected:print_formatted(_F,f"Roblox error code detected: {A}");H=ROBLOX_ERROR_DATABASE.get(A,{_I:'Unknown error',_S:'Check logs',_W:30});print_formatted(_D,f"Error {A}: {H[_I]} - {H[_S]}");error_codes_detected.add(A)
			return'roblox_error'
		return
	except Exception as Q:print_formatted(_G,f"Error state check failed: {str(Q)}");return
def attempt_game_join(config):
	A=config;global last_game_join_time,consecutive_failures,last_error_time,last_known_state;B=A.get(_N);C=A.get(_P,'')
	if not B:print_formatted(_G,'No game ID specified in config');return _B
	E=time.time()
	if E-last_error_time<10:F=10-(E-last_error_time);print_formatted(_D,f"Waiting {F:.1f} seconds after recent error...");time.sleep(F)
	if is_roblox_running()and is_in_game(B,C)and not check_error_states(A):print_formatted(_J,f"Already joined in game {B} - no need to relaunch");last_game_join_time=time.time();consecutive_failures=0;last_known_state=_s;send_discord_alert(A.get(_Q),f"Successfully rejoined game {B}");return _A
	print_formatted(_D,f"Attempting to join game {B}")
	if not close_roblox(A):print_formatted(_F,'Failed to close Roblox properly')
	time.sleep(3);D=_B
	if C:
		print_formatted(_D,'Trying launch method: launch_via_browser')
		if launch_via_browser(B,C,A):
			if wait_for_game_join(A,timeout=180):last_game_join_time=time.time();print_formatted(_J,'Successfully joined game using browser');D=_A
			else:print_formatted(_F,'Game join timeout with browser launch')
		else:print_formatted(_F,'Browser launch failed')
	else:
		print_formatted(_D,'Trying launch method: launch_via_deep_link')
		if launch_via_deep_link(B,C):
			if wait_for_game_join(A,timeout=180):last_game_join_time=time.time();print_formatted(_J,'Successfully joined game using deep link');D=_A
			else:print_formatted(_F,'Game join timeout with deep link')
		else:print_formatted(_F,'Deep link launch failed')
	if D:consecutive_failures=0;last_known_state=_s;send_discord_alert(A.get(_Q),f"Successfully rejoined game {B}");return _A
	else:consecutive_failures+=1;last_error_time=time.time();print_formatted(_G,'Game join attempt failed');return _B
def wait_for_game_join(config,timeout=180):
	A=config;E=time.time();C=A.get(_N);F=A.get(_P,'');D=A.get(_l,90);print_formatted(_D,f"Waiting {D} seconds for game to load before checking...");time.sleep(D)
	while time.time()-E<timeout:
		if is_in_game(C,F):print_formatted(_J,f"Detected successful join in game {C}");return _A
		B=check_error_states(A)
		if B:print_formatted(_F,f"Detected error during join: {B}");return _B
		time.sleep(5)
	print_formatted(_D,'Game join timeout, checking error states');B=check_error_states(A)
	if B:print_formatted(_F,f"Detected error during join: {B}")
	return _B
def automation_loop(config):
	A=config;global automation_running,last_game_join_time,consecutive_failures,last_game_verification_time,last_known_state;automation_running=_A;print_formatted(_J,'Automation started successfully!');I=A.get(_i,5);H=A.get(_m,300);D=A.get(_h,60)
	if A.get(_d,_B):D*=2;H*=2
	while automation_running:
		try:
			C=A.get(_N);B=time.time()
			if last_game_verification_time>0 and B-last_game_verification_time>=H:
				print_formatted(_D,'Periodic game verification check...');E=is_in_game(C,A.get(_P,''))
				if not E:
					print_formatted(_F,'No longer in target game during periodic check - rejoining...')
					if attempt_game_join(A):consecutive_failures=0
					else:consecutive_failures+=1
				else:print_formatted(_D,'Still in correct game - continuing...');consecutive_failures=0
				last_game_verification_time=B;continue
			F=is_roblox_running();E=is_in_game(C,A.get(_P,''))if F else _B;G=check_error_states(A)if F else _K
			if not F:
				if last_known_state==_s:
					print_formatted(_F,'Crash detected - Roblox stopped running while in game');send_discord_alert(A.get(_Q),f"Crash detected in game {C}. Rejoining now.");last_known_state='not_running'
					if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=B
					else:consecutive_failures+=1
				else:
					print_formatted(_D,'Roblox not running - launching...')
					if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=B
					else:consecutive_failures+=1
			elif G:
				print_formatted(_F,f"Error detected ({G}) - restarting...");send_discord_alert(A.get(_Q),f"Error {G} detected in game {C}. Rejoining now.");last_known_state='error'
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=B
				else:consecutive_failures+=1
			elif not E:
				print_formatted(_D,'Not in target game - rejoining...')
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=B
				else:consecutive_failures+=1
			else:
				print_formatted(_D,f"Already in game {C} and running normally - monitoring...");consecutive_failures=0;last_known_state=_s
				if last_game_verification_time==0:last_game_verification_time=B
			if consecutive_failures>=I:print_formatted(_G,f"Too many consecutive failures ({consecutive_failures}) - continuing anyway...");consecutive_failures=0
			print_formatted(_D,f"Waiting {D} seconds before next check...");J=random.uniform(.8,1.2)*D;time.sleep(J)
		except KeyboardInterrupt:print_formatted(_D,'Automation interrupted by user');break
		except Exception as K:print_formatted(_G,f"Automation loop error: {str(K)}");time.sleep(10)
	automation_running=_B;print_formatted(_D,'Automation stopped')
def display_menu():
	os.system('clear'if os.name=='posix'else'cls');print(f"\n{COLORS[_R]}{'='*50}");print(f" ENHANCED ROBLOX AUTOMATION TOOL");print(f"{'='*50}{COLORS[_C]}")
	if platform_info:print(f"{COLORS[_D]}Platform: {platform_info[_I]} ({platform_info[_L]}){COLORS[_C]}");print(f"{COLORS[_D]}Root Access: {_t if platform_info.get(_O)else'Limited'}{COLORS[_C]}")
	print(f"\n{COLORS[_E]}1.{COLORS[_C]} Configure Settings");print(f"{COLORS[_E]}2.{COLORS[_C]} Start Automation");print(f"{COLORS[_E]}3.{COLORS[_C]} Stop Automation");print(f"{COLORS[_E]}4.{COLORS[_C]} Test Game Join");print(f"{COLORS[_E]}5.{COLORS[_C]} View Current Config");print(f"{COLORS[_E]}6.{COLORS[_C]} System Information");print(f"{COLORS[_E]}7.{COLORS[_C]} Exit")
	if automation_running:print(f"\n{COLORS[_J]}Status: Automation is RUNNING{COLORS[_C]}")
	else:print(f"\n{COLORS[_F]}Status: Automation is STOPPED{COLORS[_C]}")
	if last_game_join_time:A=datetime.fromtimestamp(last_game_join_time).strftime(_w);print(f"{COLORS[_D]}Last Game Join: {A}{COLORS[_C]}")
	if error_codes_detected:print(f"{COLORS[_F]}Detected Error Codes: {', '.join(error_codes_detected)}{COLORS[_C]}")
def configure_settings():
	G='no';F='n';A=load_config();print(f"\n{COLORS[_R]}=== CONFIGURATION SETUP ==={COLORS[_C]}");H=A.get(_N,'');print(f"\nCurrent Game ID: {H if H else _f}");I=input('Enter new Game ID (or press Enter to keep current): ').strip()
	if I:A[_N]=I
	J=A.get(_P,'');print(f"\nCurrent Private Server: {J if J else _f}");print('Enter the full private server URL');K=input('Enter Private Server link (or press Enter to keep current): ').strip()
	if K:A[_P]=K
	S=A.get(_h,60);print(f"\nCurrent Check Delay: {S} seconds");B=input('Enter new Check Delay in seconds (or press Enter to keep current): ').strip()
	if B and B.isdigit():A[_h]=int(B)
	T=A.get(_l,90);print(f"\nCurrent Game Load Delay: {T} seconds");print("This is how long to wait after launching before checking if you're in the game");C=input('Enter new Game Load Delay in seconds (or press Enter to keep current): ').strip()
	if C and C.isdigit():A[_l]=int(C)
	U=A.get(_m,300);print(f"\nCurrent Game Verification Interval: {U} seconds");print("This is how often to check if you're still in the correct game (5 minutes = 300 seconds)");D=input('Enter new Game Verification Interval in seconds (or press Enter to keep current): ').strip()
	if D and D.isdigit():A[_m]=int(D)
	V=A.get(_i,3);print(f"\nCurrent Max Retries: {V}");E=input('Enter new Max Retries (or press Enter to keep current): ').strip()
	if E and E.isdigit():A[_i]=int(E)
	W=A.get(_j,_A);print(f"\nCurrent Auto Rejoin: {_U if W else _V}");L=input('Enable Auto Rejoin? (y/n, or press Enter to keep current): ').strip().lower()
	if L in['y',_u]:A[_j]=_A
	elif L in[F,G]:A[_j]=_B
	M=get_available_browsers();X=A.get(_k,_e);print(f"\nCurrent Browser Preference: {X}");print(f"Available browsers: {', '.join(M)if M else'None detected'}");print("Enter browser package name or 'auto' for automatic selection");N=input('Enter Browser Preference (or press Enter to keep current): ').strip()
	if N:A[_k]=N
	Y=A.get(_c,_A);print(f"\nCurrent Error Detection: {_U if Y else _V}");O=input('Enable Error Detection? (y/n, or press Enter to keep current): ').strip().lower()
	if O in['y',_u]:A[_c]=_A
	elif O in[F,G]:A[_c]=_B
	Z=A.get(_d,_B);print(f"\nCurrent Performance Mode: {_U if Z else _V}");P=input('Enable Performance Mode (lower CPU)? (y/n, or press Enter to keep current): ').strip().lower()
	if P in['y',_u]:A[_d]=_A
	elif P in[F,G]:A[_d]=_B
	Q=A.get(_Q,'');print(f"\nCurrent Discord Webhook: {Q if Q else _f}");R=input('Enter Discord Webhook URL (or press Enter to keep current): ').strip()
	if R:A[_Q]=R
	if save_config(A):print_formatted(_J,'Configuration saved successfully!')
	else:print_formatted(_G,'Failed to save configuration!')
	input(_v)
def view_current_config():A=load_config();print(f"\n{COLORS[_R]}=== CURRENT CONFIGURATION ==={COLORS[_C]}");print(f"{COLORS[_E]}Game ID:{COLORS[_C]} {A.get(_N,_f)}");print(f"{COLORS[_E]}Private Server:{COLORS[_C]} {A.get(_P,_f)}");print(f"{COLORS[_E]}Check Delay:{COLORS[_C]} {A.get(_h,60)} seconds");print(f"{COLORS[_E]}Game Load Delay:{COLORS[_C]} {A.get(_l,90)} seconds");print(f"{COLORS[_E]}Game Verification Interval:{COLORS[_C]} {A.get(_m,300)} seconds");print(f"{COLORS[_E]}Max Retries:{COLORS[_C]} {A.get(_i,3)}");print(f"{COLORS[_E]}Auto Rejoin:{COLORS[_C]} {_U if A.get(_j,_A)else _V}");print(f"{COLORS[_E]}Browser Preference:{COLORS[_C]} {A.get(_k,_e)}");print(f"{COLORS[_E]}Error Detection:{COLORS[_C]} {_U if A.get(_c,_A)else _V}");print(f"{COLORS[_E]}Performance Mode:{COLORS[_C]} {_U if A.get(_d,_B)else _V}");print(f"{COLORS[_E]}Discord Webhook:{COLORS[_C]} {A.get(_Q,_f)}");print(f"{COLORS[_E]}Game Validation:{COLORS[_C]} {_U if A.get(_x,_A)else _V}");print(f"{COLORS[_E]}Launch Delay:{COLORS[_C]} {A.get(_y,300)} seconds");print(f"{COLORS[_E]}Retry Delay:{COLORS[_C]} {A.get(_z,15)} seconds");input(_v)
def test_game_join():
	A=load_config();B=A.get(_N)
	if not B:print_formatted(_G,'No game ID configured. Please configure settings first.');input(_g);return
	print_formatted(_D,f"Testing game join for Game ID: {B}");print_formatted(_D,'This will close Roblox and attempt to join the game...');C=input('Continue with test? (y/n): ').strip().lower()
	if C not in['y',_u]:return
	D=attempt_game_join(A)
	if D:print_formatted(_J,'Game join test completed successfully!')
	else:print_formatted(_G,'Game join test failed!')
	input(_v)
def show_system_info():
	F='None';A='No';print(f"\n{COLORS[_R]}=== SYSTEM INFORMATION ==={COLORS[_C]}")
	if platform_info:print(f"{COLORS[_E]}Platform Type:{COLORS[_C]} {platform_info[_L]}");print(f"{COLORS[_E]}Platform Name:{COLORS[_C]} {platform_info[_I]}");print(f"{COLORS[_E]}Root Access:{COLORS[_C]} {'Available'if platform_info.get(_O)else'Limited'}");print(f"{COLORS[_E]}ADB Support:{COLORS[_C]} {_t if platform_info.get(_X)else A}");print(f"{COLORS[_E]}Shell Prefix:{COLORS[_C]} {platform_info.get(_M,F)}");print(f"{COLORS[_E]}Process Check Method:{COLORS[_C]} {platform_info.get(_T,_n)}");print(f"{COLORS[_E]}Browser Launch Method:{COLORS[_C]} {platform_info.get(_Y,_n)}")
	B=verify_roblox_installation();print(f"{COLORS[_E]}Roblox Installed:{COLORS[_C]} {_t if B else A}")
	if B:G=is_roblox_running();print(f"{COLORS[_E]}Roblox Running:{COLORS[_C]} {_t if G else A}")
	C=get_available_browsers();print(f"{COLORS[_E]}Available Browsers:{COLORS[_C]} {', '.join(C)if C else F}")
	try:D=run_shell_command('getprop ro.build.version.release',platform_info=platform_info);print(f"{COLORS[_E]}Android Version:{COLORS[_C]} {D if D else _n}")
	except:pass
	try:E=run_shell_command('getprop ro.product.model',platform_info=platform_info);print(f"{COLORS[_E]}Device Model:{COLORS[_C]} {E if E else _n}")
	except:pass
	input(_v)
def main():
	global platform_info,automation_running
	try:
		os.system('clear'if os.name=='posix'else'cls');print(f"{COLORS[_R]}");print('╔══════════════════════════════════════════════════════════════╗');print('║ ENHANCED ROBLOX AUTOMATION TOOL ║');print('║ Supports: UGPHONE, VSPHONE, REDFINGER ║');print('║ Standard Android & Emulators ║');print('╚══════════════════════════════════════════════════════════════╝');print(f"{COLORS[_C]}");E=PlatformDetector();platform_info=E.detect_platform()
		if not verify_roblox_installation():print_formatted(_G,'Roblox is not installed or not accessible!');print_formatted(_D,'Please install Roblox and ensure proper permissions.');sys.exit(1)
		B=_K
		while _A:
			try:
				display_menu();A=input(f"\n{COLORS[_E]}Enter your choice (1-7): {COLORS[_C]}").strip()
				if A=='1':configure_settings()
				elif A=='2':
					if automation_running:print_formatted(_F,'Automation is already running!');input(_g)
					else:
						D=load_config()
						if not D.get(_N):print_formatted(_G,'No game ID configured! Please configure settings first.');input(_g)
						else:B=threading.Thread(target=automation_loop,args=(D,),daemon=_A);B.start()
				elif A=='3':
					if automation_running:
						print_formatted(_D,'Stopping automation...');automation_running=_B
						if B:B.join(timeout=5)
						print_formatted(_J,'Automation stopped!')
					else:print_formatted(_F,'Automation is not running!')
					input(_g)
				elif A=='4':test_game_join()
				elif A=='5':view_current_config()
				elif A=='6':show_system_info()
				elif A=='7':
					if automation_running:
						print_formatted(_D,'Stopping automation before exit...');automation_running=_B
						if B:B.join(timeout=5)
					print_formatted(_D,'Thank you for using Enhanced Roblox Automation Tool!');break
				else:print_formatted(_F,'Invalid choice! Please enter 1-7.');input(_g)
			except KeyboardInterrupt:
				print_formatted(_D,'\nExiting...')
				if automation_running:automation_running=_B
				break
			except Exception as C:print_formatted(_G,f"Menu error: {str(C)}");input(_g)
	except Exception as C:print_formatted(_G,f"Critical error: {str(C)}");sys.exit(1)
if __name__=='__main__':main()
