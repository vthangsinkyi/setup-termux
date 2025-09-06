#!/usr/bin/env python3
'\nEnhanced Roblox Automation Tool (Rejoiner.py)\nSupports: UGPHONE, VSPHONE, REDFINGER, LD Player, MUMU, Standard Android/Emulators\nAuthor: Optimized for global device support and easy configuration\n'
_A5='Private Server Link: '
_A4='Enter Game ID: '
_A3='logcat -c'
_A2='reduced_logging'
_A1='auto_rejoin'
_A0='game_verification_interval'
_z='error_detection'
_y='browser_preference'
_x='max_retries'
_w='browser_launch'
_v='process_check_method'
_u='use_adb'
_t='\nPress Enter to continue...'
_s='error'
_r='warning'
_q='success'
_p='test'
_o='echo test'
_n='-c'
_m='has_root'
_l='standard'
_k='Disabled'
_j='Enabled'
_i='Not set'
_h='Unknown'
_g='auto'
_f='Press Enter to continue...'
_e='info'
_d='webhook_alerts'
_c='discord_webhook'
_b='shell_prefix'
_a='nox'
_Z='bluestacks'
_Y='mumu'
_X='wait_time'
_W='ldplayer'
_V='solution'
_U='type'
_T='redfinger'
_S='vsphone'
_R='ugphone'
_Q='HEADER'
_P='game_load_delay'
_O='check_delay'
_N='performance_mode'
_M='game_id'
_L=None
_K='private_server'
_J='DEBUG'
_I='name'
_H='SUCCESS'
_G='ERROR'
_F='WARNING'
_E='INFO'
_D='CYAN'
_C='RESET'
_B=False
_A=True
import requests,time,os,json,subprocess,urllib.parse,re,threading,sys,logging,random
from datetime import datetime
from typing import Dict,List,Optional,Any
from queue import Queue
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler('/sdcard/roblox_automation.log'),logging.StreamHandler()])
logger=logging.getLogger('Rejoiner')
COLORS={_C:'\x1b[0m',_E:'\x1b[94m',_H:'\x1b[92m',_F:'\x1b[93m',_G:'\x1b[91m','BOLD':'\x1b[1m',_D:'\x1b[96m',_Q:'\x1b[95m',_J:'\x1b[90m'}
CONFIG_FILE='/sdcard/roblox_config.json'
ROBLOX_PACKAGE='com.roblox.client'
BROWSER_PACKAGES=['com.android.chrome','com.sec.android.app.sbrowser','com.google.android.webview','org.mozilla.firefox','com.opera.browser','com.brave.browser','com.microsoft.emmx','com.vivaldi.browser']
ROBLOX_ERROR_DATABASE={'267':{_I:'Cannot rejoin game',_V:'Wait 30 seconds before retry',_X:30},'279':{_I:'Server full',_V:'Try different server or wait',_X:15},'292':{_I:'Kicked from game',_V:'Check if banned, wait 5 minutes',_X:300},'529':{_I:'Connection lost',_V:'Check network, restart if persistent',_X:10},'601':{_I:'Place unavailable',_V:'Game might be updating, check later',_X:60}}
automation_running=_B
platform_info=_L
last_game_join_time=0
error_codes_detected=set()
consecutive_failures=0
last_error_time=0
last_game_verification_time=0
last_crash_time=0
last_discord_alert=0
class PlatformDetector:
	def __init__(A):A.detected_platform=_L
	def detect_platform(A):
		'Enhanced platform detection with global support';K='intent';J='pidof';I='su -c';H='special_commands';G='Standard Android';B='root_check';L={_R:{_I:'UGPHONE',B:A._check_root_ugphone},_S:{_I:'VSPHONE',B:A._check_root_vsphone},_T:{_I:'REDFINGER',B:A._check_root_redfinger},_W:{_I:'LD Player',B:A._check_root_standard},_Y:{_I:'MUMU Player',B:A._check_root_standard},_Z:{_I:'BlueStacks',B:A._check_root_standard},_a:{_I:'Nox Player',B:A._check_root_standard},_l:{_I:G,B:A._check_root_standard}}
		for(C,F)in L.items():
			D=getattr(A,f"_is_{C}",_L)
			if D and callable(D)and D():E=F[B]();return{_U:C,_I:F[_I],_m:E,_u:C in[_l,_W,_Y,_Z,_a],_b:I if E else'',H:C in[_R,_S,_T],_v:J if E else'ps_grep',_w:K}
		return{_U:_l,_I:G,_m:A._check_root_standard(),_u:_A,_b:I if A._check_root_standard()else'',H:_B,_v:J,_w:K}
	def _is_ugphone(A):
		try:
			B=['/system/bin/ugphone','/system/app/UGPhone','/data/local/tmp/ugphone','/system/priv-app/UGPhone','/system/framework/ugphone.jar','/system/etc/ugphone','/vendor/bin/ugphone','/system/bin/ug_phone']
			for C in B:
				if os.path.exists(C):return _A
			D=A._get_build_prop();E=[_R,'ug_phone','cloudphone','universal.global.phone','ugcloud']
			for F in E:
				if F.lower()in D.lower():return _A
			G=A._get_env_vars()
			if any(_R in A.lower()for A in G):return _A
			H=A._get_running_processes()
			if any(_R in A.lower()for A in H):return _A
			return _B
		except:return _B
	def _is_vsphone(A):
		try:
			B=['/system/bin/vsphone','/system/app/VSPhone','/data/local/tmp/vsphone','/system/priv-app/VSPhone','/system/framework/vsphone.jar','/system/etc/vsphone','/vendor/bin/vsphone','/system/bin/vs_phone']
			for C in B:
				if os.path.exists(C):return _A
			D=A._get_build_prop();E=[_S,'vs_phone','virtualphone','virtual.space','vspace']
			for F in E:
				if F.lower()in D.lower():return _A
			G=A._get_env_vars()
			if any(_S in A.lower()for A in G):return _A
			H=A._get_running_processes()
			if any(_S in A.lower()for A in H):return _A
			return _B
		except:return _B
	def _is_redfinger(A):
		try:
			B=['/system/bin/redfinger','/system/app/RedFinger','/data/local/tmp/redfinger','/system/priv-app/RedFinger','/system/framework/redfinger.jar','/system/etc/redfinger','/vendor/bin/redfinger','/system/bin/red_finger']
			for C in B:
				if os.path.exists(C):return _A
			D=A._get_build_prop();E=[_T,'red_finger','redcloud','red.finger','rfcloud']
			for F in E:
				if F.lower()in D.lower():return _A
			G=A._get_env_vars()
			if any(_T in A.lower()for A in G):return _A
			H=A._get_running_processes()
			if any(_T in A.lower()for A in H):return _A
			return _B
		except:return _B
	def _is_ldplayer(A):
		C='dnplayer'
		try:
			D=[_W,'ld_main','ldconsole',C,'/data/data/com.ldplayer','/data/data/com.ludashi'];E=A._get_running_processes()
			if any(_W in A.lower()for A in E):return _A
			for F in D:
				if os.path.exists(F):return _A
			B=A._get_build_prop()
			if _W in B.lower()or C in B.lower():return _A
			return _B
		except:return _B
	def _is_mumu(A):
		C='nemu'
		try:
			D=[_Y,C,'/data/data/com.microvirt','/data/data/com.microvirt.memuplay'];E=A._get_running_processes()
			if any(_Y in A.lower()for A in E):return _A
			for F in D:
				if os.path.exists(F):return _A
			B=A._get_build_prop()
			if _Y in B.lower()or C in B.lower():return _A
			return _B
		except:return _B
	def _is_bluestacks(A):
		try:
			B=[_Z,'bst','hd-player','hd-player64','/data/data/com.bluestacks','/data/data/com.bluestacks.appplayer'];C=A._get_running_processes()
			if any(_Z in A.lower()for A in C):return _A
			for D in B:
				if os.path.exists(D):return _A
			E=A._get_build_prop()
			if _Z in E.lower():return _A
			return _B
		except:return _B
	def _is_nox(A):
		try:
			B=[_a,'Nox','NoxPlayer','/data/data/com.nox','/data/data/com.nox.app.player'];C=A._get_running_processes()
			if any(_a in A.lower()for A in C):return _A
			for D in B:
				if os.path.exists(D):return _A
			E=A._get_build_prop()
			if _a in E.lower():return _A
			return _B
		except:return _B
	def _get_build_prop(B):
		try:A=subprocess.run(['cat','/system/build.prop'],capture_output=_A,text=_A,timeout=5);return A.stdout
		except:return''
	def _get_env_vars(B):
		try:A=subprocess.run(['env'],capture_output=_A,text=_A,timeout=5);return A.stdout.split('\n')
		except:return[]
	def _get_running_processes(B):
		try:A=subprocess.run(['ps'],capture_output=_A,text=_A,timeout=5);return A.stdout.split('\n')
		except:return[]
	def _check_root_standard(B):
		try:A=subprocess.run(['su',_n,_o],capture_output=_A,text=_A,timeout=5);return _p in A.stdout
		except:return _B
	def _check_root_ugphone(A):
		try:
			if A._check_root_standard():return _A
			B=subprocess.run(['ugphone_su',_n,_o],capture_output=_A,text=_A,timeout=5);return _p in B.stdout
		except:return _B
	def _check_root_vsphone(A):
		try:
			if A._check_root_standard():return _A
			B=subprocess.run(['vsphone_su',_n,_o],capture_output=_A,text=_A,timeout=5);return _p in B.stdout
		except:return _B
	def _check_root_redfinger(A):
		try:
			if A._check_root_standard():return _A
			B=subprocess.run(['redfinger_su',_n,_o],capture_output=_A,text=_A,timeout=5);return _p in B.stdout
		except:return _B
def print_formatted(level,message):B=message;A=level;C=datetime.now().strftime('%Y-%m-%d %H:%M:%S');D={_E:_E,_H:'OK',_F:'WARN',_G:_G,_Q:'====',_J:_J}.get(A,A);E=COLORS.get(A,COLORS[_C]);print(f"{E}{C} [{D}] {B}{COLORS[_C]}");logger.log(getattr(logging,A.upper(),logging.INFO),B)
def safe_input(prompt,timeout=30):
	C=prompt
	try:
		B=Queue()
		def D():
			try:A=input(C);B.put(A)
			except:B.put(_L)
		A=threading.Thread(target=D);A.daemon=_A;A.start();A.join(timeout)
		if A.is_alive():print_formatted(_F,'Input timeout - returning empty');return''
		return B.get()or''
	except:
		try:return input(C)
		except:return''
def run_shell_command(command,timeout=15,platform_info=_L):
	E=timeout;B=platform_info;A=command
	try:
		if B and B.get(_U)in[_W,_Y]:E=20
		if B and B.get(_b):
			if B[_b]:D=B[_b].split()+[A]
			else:D=A.split()
		elif A.startswith('ps -A'):D=['ps']
		else:D=A.split()
		C=subprocess.run(D,capture_output=_A,text=_A,timeout=E)
		if C.stderr and'permission denied'not in C.stderr.lower():
			if'garbage option'not in C.stderr.lower():print_formatted(_J,f"Command stderr: {C.stderr.strip()}")
		return C.stdout.strip()
	except subprocess.TimeoutExpired:print_formatted(_F,f"Command timeout: {A}");return''
	except Exception as F:
		if'dumpsys'not in A:print_formatted(_G,f"Command failed: {A} - {str(F)}")
		return''
def load_config():
	A={_M:'',_K:'',_O:60,_x:3,_A1:_A,_y:_g,_z:_A,_N:_B,_P:90,_c:'',_d:_B,_A0:300,'minimal_ui':_A,_A2:_B,'extended_timeouts':_B,'setup_completed':_B}
	try:
		if not os.path.exists(CONFIG_FILE):
			with open(CONFIG_FILE,'w')as B:json.dump(A,B,indent=4)
			run_shell_command(f"chmod 644 {CONFIG_FILE}",platform_info=platform_info);print_formatted(_E,'Created new config file');return A
		with open(CONFIG_FILE,'r')as B:
			C=json.load(B)
			for(D,E)in A.items():
				if D not in C:C[D]=E
			return C
	except Exception as F:print_formatted(_G,f"Config load error: {F}");return A
def save_config(config):
	try:
		with open(CONFIG_FILE,'w')as A:json.dump(config,A,indent=4)
		run_shell_command(f"chmod 644 {CONFIG_FILE}",platform_info=platform_info);print_formatted(_H,'Config saved');return _A
	except Exception as B:print_formatted(_G,f"Config save error: {B}");return _B
def send_discord_alert(config,message,level=_e):
	A=config;global last_discord_alert
	try:
		B=A.get(_c,'')
		if not B or not A.get(_d,_A):return
		C=time.time()
		if C-last_discord_alert<60:return
		E={_e:3447003,_q:3066993,_r:16776960,_s:15158332}.get(level,3447003);F={'title':'Roblox Automation Alert','description':message,'color':E,'timestamp':datetime.utcnow().isoformat(),'footer':{'text':f"Automation Tool - {platform_info[_I]if platform_info else'Unknown Platform'}"}};G={'embeds':[F],'username':'Roblox Automation Bot'};D=requests.post(B,json=G,timeout=10)
		if D.status_code==204:print_formatted(_E,'Discord alert sent successfully');last_discord_alert=C
		else:print_formatted(_F,f"Discord webhook returned status {D.status_code}")
	except Exception as H:print_formatted(_J,f"Discord webhook error: {str(H)}")
def auto_detect_optimizations():
	H='comprehensive';D='detection_method';A={_O:60,_P:90,_N:_B,D:H}
	try:
		B=4
		try:E=run_shell_command('cat /proc/cpuinfo | grep processor | wc -l');B=int(E.strip())if E.strip().isdigit()else 4
		except:pass
		C=2
		try:
			F=run_shell_command('cat /proc/meminfo | grep MemTotal')
			if F:I=int(''.join(filter(str.isdigit,F.split()[1])));C=I/1024/1024
		except:pass
		G=_B
		try:J=run_shell_command('cat /system/build.prop').lower();K=['bliss','andy','genymotion',_W,_a,'memu',_Z];G=any(A in J for A in K)
		except:pass
		if C<2 or B<4 or G:A[_N]=_A;A[_O]=90;A[_P]=120;A[D]='basic';print_formatted(_E,'Low-end device detected - enabling performance mode')
		if C>=4 and B>=6:A[_N]=_B;A[_O]=45;A[_P]=60;A[D]=H;print_formatted(_E,'High-end device detected - enabling enhanced monitoring')
	except Exception as L:print_formatted(_J,f"Auto-detection error: {str(L)}")
	return A
def apply_auto_optimizations(config):
	A=config;B=auto_detect_optimizations()
	if A.get(_O)is _L:A[_O]=B[_O]
	if A.get(_P)is _L:A[_P]=B[_P]
	if A.get(_N)is _L:A[_N]=B[_N]
	return A
def check_termux_stability():
	try:
		A=run_shell_command('echo stability_test',timeout=5)
		if'stability_test'not in A:print_formatted(_F,'Termux stability issues detected');return _B
		return _A
	except:print_formatted(_F,'Termux stability check failed');return _B
def verify_roblox_installation():
	B='versionName='
	try:
		C=run_shell_command(f"pm list packages {ROBLOX_PACKAGE}",platform_info=platform_info)
		if ROBLOX_PACKAGE not in C:print_formatted(_G,'Roblox not installed.');return _B
		A=run_shell_command(f"dumpsys package {ROBLOX_PACKAGE} | grep versionName",platform_info=platform_info)
		if A:D=A.split(B)[1].split()[0]if B in A else _h;print_formatted(_E,f"Roblox version: {D}")
		return _A
	except Exception as E:print_formatted(_G,f"Roblox verification error: {E}");return _B
def is_roblox_running(retries=1,delay=2):
	B=delay;A=retries
	for C in range(A):
		try:
			G=[lambda:run_shell_command(f"pidof {ROBLOX_PACKAGE}"),lambda:run_shell_command(f"ps | grep {ROBLOX_PACKAGE}"),lambda:run_shell_command(f"pm list packages | grep {ROBLOX_PACKAGE}")]
			for H in G:
				try:
					D=H()
					if D and ROBLOX_PACKAGE in D:print_formatted(_J,'Roblox process found');return _A
				except:continue
			if platform_info and platform_info.get(_U)in[_R,_S,_T]:
				E=run_shell_command(f"logcat -d | grep {ROBLOX_PACKAGE} | head -10")
				if E and ROBLOX_PACKAGE in E:print_formatted(_J,'Roblox found via logcat');return _A
			if platform_info and platform_info.get(_U)in[_l]:
				F=run_shell_command(f"ps | grep {ROBLOX_PACKAGE[:8]}")
				if F and ROBLOX_PACKAGE[:8]in F:print_formatted(_J,'Roblox found via partial match');return _A
			if C<A-1:time.sleep(B)
		except Exception as I:
			print_formatted(_G,f"Roblox running check error: {str(I)}")
			if C<A-1:time.sleep(B)
	print_formatted(_J,'Roblox not found');return _B
def close_roblox(config=_L):
	A=config
	try:
		print_formatted(_E,'Closing Roblox...');run_shell_command('input keyevent KEYCODE_HOME',platform_info=platform_info);time.sleep(2);run_shell_command(f"am force-stop {ROBLOX_PACKAGE}",platform_info=platform_info);time.sleep(2)
		if platform_info and platform_info[_U]in[_R,_S,_T]:run_shell_command(f"pkill -f {ROBLOX_PACKAGE}",platform_info=platform_info)
		else:run_shell_command(f"killall -9 {ROBLOX_PACKAGE}",platform_info=platform_info)
		C=A.get('force_kill_delay',10)if A else 10;time.sleep(C)
		if is_roblox_running():print_formatted(_F,'Roblox still running, clearing cache...');run_shell_command(f"pm clear {ROBLOX_PACKAGE}",platform_info=platform_info);time.sleep(5)
		B=not is_roblox_running()
		if B:print_formatted(_H,'Roblox closed successfully')
		else:print_formatted(_G,'Failed to close Roblox completely')
		return B
	except Exception as D:print_formatted(_G,f"Failed to close Roblox: {str(D)}");return _B
def get_main_activity():
	B='.MainActivity'
	try:
		E=run_shell_command(f"dumpsys package {ROBLOX_PACKAGE} | grep -A 5 'android.intent.action.MAIN'",platform_info=platform_info);C=re.search('com\\.roblox\\.client/(\\.[A-Za-z0-9.]+)',E)
		if C:D=C.group(1);print_formatted(_J,f"Detected main activity: {D}");return D
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
			print_formatted(_E,f"Using provided private server URL: {A}");return A
		C=f"roblox://experiences/start?placeId={B}";print_formatted(_E,f"Built game deep link URL: {C}");return C
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
		if B:print_formatted(_E,'Skipping deep link for private server, using browser method');return _B
		print_formatted(_E,f"Launching via deep link: Game ID {A}");C=build_game_url(A,B);D=f'am start -a android.intent.action.VIEW -d "{C}"';G=run_shell_command(D,platform_info=platform_info);E=time.time()
		while time.time()-E<120:
			if is_roblox_running():print_formatted(_H,'Roblox launched via deep link');time.sleep(10);return _A
			time.sleep(3)
		print_formatted(_F,'Deep link launched but Roblox not running after extended wait');return _B
	except Exception as F:print_formatted(_G,f"Deep link launch failed: {str(F)}");return _B
def launch_via_browser(game_id,private_server='',config=_L):
	G=config;F=private_server;E=game_id
	try:
		if not F:print_formatted(_F,'No private server link provided for browser launch');return _B
		print_formatted(_E,f"Launching via browser: Game ID {E}");A=build_game_url(E,F);B=G.get(_y,_g)if G else _g;C=get_available_browsers()
		if B!=_g and B in C:D=f'am start -a android.intent.action.VIEW -d "{A}" {B}'
		elif C:D=f'am start -a android.intent.action.VIEW -d "{A}" {C[0]}'
		else:D=f'am start -a android.intent.action.VIEW -d "{A}"'
		J=run_shell_command(D,platform_info=platform_info);H=time.time()
		while time.time()-H<120:
			if is_roblox_running():print_formatted(_H,'Roblox launched via browser');time.sleep(10);return _A
			time.sleep(3)
		print_formatted(_F,'Browser launch initiated but Roblox not running after extended wait');return _B
	except Exception as I:print_formatted(_G,f"Browser launch failed: {str(I)}");return _B
def is_in_game(game_id,private_server=''):
	C=private_server;A=game_id
	try:
		if not is_roblox_running():print_formatted(_J,'Roblox not running - not in game');return _B
		if platform_info and platform_info[_U]in[_R,_S,_T]:
			D=run_shell_command(f"logcat -d | grep {ROBLOX_PACKAGE} | head -10")
			if D and ROBLOX_PACKAGE in D:print_formatted(_J,'Roblox active in logcat - likely in game');return _A
			return _B
		run_shell_command(_A3,platform_info=platform_info);time.sleep(1);E=[f"place.*{A}",f"game.*{A}",f"join.*{A}",'loading.*complete','game.*start','experience.*load','character.*load','player.*join','render.*start','physics.*start','workspace.*load','joined game','successfully joined']
		if C:
			B=extract_private_server_code(C)
			if B:E.extend([f"privateServer.*{B}",f"linkCode.*{B}",'private server.*joined'])
		I=f"logcat -d | grep -iE '{'|'.join(E)}' | grep -v su | head -20";F=run_shell_command(I,platform_info=platform_info)
		if F.strip():print_formatted(_J,f"Game activity logs found: {F.strip()}");return _A
		G=run_shell_command(f"dumpsys meminfo {ROBLOX_PACKAGE} | grep 'TOTAL'")
		if G:
			try:
				H=int(''.join(filter(str.isdigit,G.split()[0])))
				if H>500000:print_formatted(_J,f"High memory usage ({H} KB) - likely in game");return _A
			except:pass
		print_formatted(_J,'No strong indicators of being in game found');return _B
	except Exception as J:print_formatted(_G,f"Game detection error: {str(J)}");return _B
def detect_roblox_error_codes():
	try:
		D=['error code[:\\s]*(\\d+)','error.*code[:\\s]*(\\d+)','code[:\\s]*(\\d+).*error','err.*code[:\\s]*(\\d+)','error\\s+(\\d+)','code\\s+(\\d+).*failed','failed.*code\\s+(\\d+)'];A=[];E=run_shell_command('logcat -d | grep -i error | grep -v su | head -20',platform_info=platform_info)
		for B in D:C=re.findall(B,E,re.IGNORECASE);A.extend(C)
		F=run_shell_command('logcat -d | grep -i roblox | grep -i error | grep -v su | head -10',platform_info=platform_info)
		for B in D:C=re.findall(B,F,re.IGNORECASE);A.extend(C)
		return list(set(A))
	except Exception as G:print_formatted(_G,f"Error code detection failed: {str(G)}");return[]
def check_error_states(config=_L):
	M='frozen';L='unexpected client';K='banned';J='kicked';I='crash';C=config
	try:
		if not C or not C.get(_z,_A):return
		N=run_shell_command('uiautomator dump /sdcard/ui_dump.xml && cat /sdcard/ui_dump.xml',platform_info=platform_info);O=[_s,I,'disconnect',J,K,'failed','unable','sorry','oops','problem','restart','rejoin','retry','close','exit',L,'exploiting','same account','idle','anti-cheat','connection lost','reconnect']
		if any(A in N.lower()for A in O):print_formatted(_F,'Error dialog detected in UI');return'ui_error'
		B=run_shell_command("dumpsys activity | grep -i 'anr'",platform_info=platform_info)
		if B and ROBLOX_PACKAGE in B:print_formatted(_F,f"ANR detected: {B.strip()}");return M
		if platform_info.get(_m):
			D=run_shell_command('ls -l /data/anr/ | grep anr',platform_info=platform_info)
			if D and ROBLOX_PACKAGE in D:print_formatted(_F,'ANR trace files detected for Roblox');return M
		run_shell_command(_A3,platform_info=platform_info);time.sleep(1);P=['fatal','exception','sigsegv','segmentation','native crash','system_server','am_crash','beginning of crash','backtrace',L,J,K,'disconnected'];E=run_shell_command(f"logcat -d | grep -iE '{'|'.join(P)}' | grep -v su | head -10",platform_info=platform_info)
		if E.strip():print_formatted(_F,f"Crash detected in logs: {E.strip()}");return I
		F=run_shell_command("logcat -d | grep -iE 'timeout|disconnect|network|connection|idle' | grep -v su | head -5",platform_info=platform_info)
		if F.strip():print_formatted(_F,f"Network issues: {F.strip()}");return'network_error'
		G=detect_roblox_error_codes()
		if G:
			for A in G:
				if A not in error_codes_detected:print_formatted(_F,f"Roblox error code detected: {A}");H=ROBLOX_ERROR_DATABASE.get(A,{_I:'Unknown error',_V:'Check logs',_X:30});print_formatted(_E,f"Error {A}: {H[_I]} - {H[_V]}");error_codes_detected.add(A)
			return'roblox_error'
		return
	except Exception as Q:print_formatted(_G,f"Error state check failed: {str(Q)}");return
def detect_crash(config):
	global last_crash_time
	try:
		if not is_roblox_running():
			A=time.time()
			if A-last_game_join_time<300 and A-last_crash_time>30:
				B=run_shell_command("logcat -d | grep -i 'crash\\|fatal\\|exception' | grep -i roblox | head -5",platform_info=platform_info)
				if B.strip():print_formatted(_F,f"Crash detected: {B.strip()}");send_discord_alert(config,f"🚨 Roblox crashed unexpectedly\n```{B.strip()}```",_s);last_crash_time=A;return _A
		return _B
	except Exception as C:print_formatted(_G,f"Crash detection error: {str(C)}");return _B
def attempt_game_join(config):
	A=config;global last_game_join_time,consecutive_failures,last_error_time;C=A.get(_M);B=A.get(_K,'')
	if not C and not B:print_formatted(_G,'No game ID or private server specified in config');return _B
	E=time.time()
	if E-last_error_time<10:F=10-(E-last_error_time);print_formatted(_E,f"Waiting {F:.1f} seconds after recent error...");time.sleep(F)
	if is_roblox_running()and is_in_game(C,B)and not check_error_states(A):print_formatted(_H,f"Already joined in game - no need to relaunch");last_game_join_time=time.time();consecutive_failures=0;return _A
	print_formatted(_E,f"Attempting to join game")
	if not close_roblox(A):print_formatted(_F,'Failed to close Roblox properly')
	time.sleep(3);D=_B
	if B:
		print_formatted(_E,'Trying launch method: launch_via_browser')
		if launch_via_browser(C,B,A):
			if wait_for_game_join(A,timeout=180):last_game_join_time=time.time();print_formatted(_H,'Successfully joined game using browser');send_discord_alert(A,f"✅ Successfully joined game via browser",_q);D=_A
			else:print_formatted(_F,'Game join timeout with browser launch')
		else:print_formatted(_F,'Browser launch failed')
	else:
		print_formatted(_E,'Trying launch method: launch_via_deep_link')
		if launch_via_deep_link(C,B):
			if wait_for_game_join(A,timeout=180):last_game_join_time=time.time();print_formatted(_H,'Successfully joined game using deep link');send_discord_alert(A,f"✅ Successfully joined game via deep link",_q);D=_A
			else:print_formatted(_F,'Game join timeout with deep link')
		else:print_formatted(_F,'Deep link launch failed')
	if D:consecutive_failures=0;return _A
	else:consecutive_failures+=1;last_error_time=time.time();print_formatted(_G,'Game join attempt failed');send_discord_alert(A,f"❌ Failed to join game (Attempt {consecutive_failures})",_s);return _B
def wait_for_game_join(config,timeout=180):
	A=config;D=time.time();E=A.get(_M);F=A.get(_K,'');C=A.get(_P,90);print_formatted(_E,f"Waiting {C} seconds for game to load before checking...");time.sleep(C)
	while time.time()-D<timeout:
		if is_in_game(E,F):print_formatted(_H,f"Detected successful join in game");return _A
		B=check_error_states(A)
		if B:print_formatted(_F,f"Detected error during join: {B}");return _B
		time.sleep(5)
	print_formatted(_E,'Game join timeout, checking error states');B=check_error_states(A)
	if B:print_formatted(_F,f"Detected error during join: {B}")
	return _B
def automation_loop(config):
	J='🔄 Not in target game - rejoining...';I='N/A';A=config;global automation_running,last_game_join_time,consecutive_failures,last_game_verification_time;automation_running=_A;print_formatted(_H,'Starting Roblox auto-rejoin...');print_formatted(_E,f"Target: Game ID {A.get(_M,I)} | Private Server {A.get(_K,I)}");send_discord_alert(A,'🚀 Roblox auto-rejoin started!',_e);K=A.get(_x,3);L=A.get(_A0,300);M=A.get(_N,_B);C=A.get(_A2,_B)
	while automation_running:
		try:
			H=A.get(_M);B=time.time()
			if not C:print_formatted(_E,'Checking game status...')
			if detect_crash(A):
				print_formatted(_F,'Crash detected - attempting to rejoin...')
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=B
				else:consecutive_failures+=1
				continue
			if last_game_verification_time>0 and B-last_game_verification_time>=L:
				print_formatted(_E,'Verifying game status...');E=is_in_game(H,A.get(_K,''))
				if not E:
					print_formatted(_F,'Not in target game - attempting to rejoin...');send_discord_alert(A,J,_r)
					if attempt_game_join(A):consecutive_failures=0
					else:consecutive_failures+=1
				else:
					if not C:print_formatted(_E,'Confirmed in correct game - continuing...')
					consecutive_failures=0
				last_game_verification_time=B;continue
			F=is_roblox_running();E=is_in_game(H,A.get(_K,''))if F else _B;G=check_error_states(A)if F else _L
			if not F:
				print_formatted(_E,'Roblox not running - launching...');send_discord_alert(A,'🔌 Roblox not running - launching...',_e)
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=B
				else:consecutive_failures+=1
			elif G:
				print_formatted(_F,f"Error detected ({G}) - restarting...");send_discord_alert(A,f"⚠️ Error detected ({G}) - restarting...",_r)
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=B
				else:consecutive_failures+=1
			elif not E:
				print_formatted(_E,'Not in target game - rejoining...');send_discord_alert(A,J,_e)
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=B
				else:consecutive_failures+=1
			else:
				if not C:print_formatted(_E,'In game and running normally - monitoring...')
				consecutive_failures=0
				if last_game_verification_time==0:last_game_verification_time=B
			if consecutive_failures>=K:print_formatted(_F,f"Reached {consecutive_failures} failures - continuing to retry...");send_discord_alert(A,f"🔁 Reached {consecutive_failures} failures - continuing...",_r);consecutive_failures=0
			D=A.get(_O,60)
			if M:
				D=max(D,120)
				if not C:print_formatted(_E,f"Performance mode - waiting {D} seconds...")
			elif not C:print_formatted(_E,f"Waiting {D} seconds...")
			time.sleep(random.uniform(.8,1.2)*D)
		except KeyboardInterrupt:print_formatted(_E,'Automation interrupted by user');break
		except Exception as N:print_formatted(_G,f"Automation loop error: {str(N)}");time.sleep(10)
	automation_running=_B;print_formatted(_E,'Auto-rejoin stopped');send_discord_alert(A,'🛑 Auto-rejoin stopped',_e)
def display_menu():
	try:
		if os.name=='posix':os.system('clear')
		else:os.system('cls')
	except:pass
	print(f"\n{COLORS[_Q]}{'='*40}");print(f" ROBLOX AUTOMATION TOOL");print(f"{'='*40}{COLORS[_C]}")
	if platform_info:print(f"{COLORS[_E]}Platform: {platform_info[_I]}{COLORS[_C]}")
	print(f"\n{COLORS[_D]}1.{COLORS[_C]} Configure");print(f"{COLORS[_D]}2.{COLORS[_C]} Start");print(f"{COLORS[_D]}3.{COLORS[_C]} Stop");print(f"{COLORS[_D]}4.{COLORS[_C]} Test Join");print(f"{COLORS[_D]}5.{COLORS[_C]} Config");print(f"{COLORS[_D]}6.{COLORS[_C]} System Info");print(f"{COLORS[_D]}7.{COLORS[_C]} Exit")
	if automation_running:print(f"\n{COLORS[_H]}Status: RUNNING{COLORS[_C]}")
	else:print(f"\n{COLORS[_F]}Status: STOPPED{COLORS[_C]}")
def first_time_setup():
	print(f"\n{COLORS[_Q]}=== WELCOME TO ROBLOX AUTOMATION TOOL ==={COLORS[_C]}");print("\nLet's get you set up in just a few steps!");A=load_config();print(f"\n{COLORS[_D]}STEP 1: Configure your game{COLORS[_C]}");print('1. Join by Game ID (public servers)');print('2. Join by Private Server Link');B=safe_input(f"\n{COLORS[_D]}Select option (1-2): {COLORS[_C]}")
	if B=='1':
		C=safe_input(_A4).strip()
		if C:A[_M]=C;A[_K]=''
	elif B=='2':
		print('\nPaste your private server link below:');print('Example: https://www.roblox.com/games/...?privateServerLinkCode=...');D=safe_input(_A5).strip()
		if D:A[_K]=D;A[_M]=''
	print(f"\n{COLORS[_D]}STEP 2: Discord notifications (optional){COLORS[_C]}");F=safe_input('Enable Discord notifications? (y/n): ').strip().lower()
	if F in['y','yes']:
		E=safe_input('Enter Discord webhook URL: ').strip()
		if E:A[_c]=E;A[_d]=_A
	print(f"\n{COLORS[_D]}STEP 3: Performance optimization{COLORS[_C]}");print('The tool will automatically optimize for your device.');A=apply_auto_optimizations(A)
	if save_config(A):print_formatted(_H,'Setup completed successfully!');print('\nYou can always change these settings from the main menu.');return _A
	return _B
def configure_settings():
	A=load_config();print(f"\n{COLORS[_Q]}=== QUICK CONFIGURATION ==={COLORS[_C]}");D=A.get(_M,'');E=A.get(_K,'')
	if E:print(f"\n{COLORS[_D]}Current Private Server:{COLORS[_C]} {E}")
	else:print(f"\n{COLORS[_D]}Current Game ID:{COLORS[_C]} {D if D else _i}")
	print('\n1. Enter Game ID');print('2. Enter Private Server Link');print('3. Configure Discord Webhook');print('4. Advanced Settings (Optional)');print('5. Back to Main Menu');B=safe_input(f"\n{COLORS[_D]}Select option (1-5): {COLORS[_C]}")
	if B=='1':
		F=safe_input(_A4).strip()
		if F:A[_M]=F;A[_K]='';print_formatted(_H,'Game ID set successfully!')
	elif B=='2':
		print('\nEnter Private Server Link:');G=safe_input(_A5).strip()
		if G:A[_K]=G;print_formatted(_H,'Private Server link set successfully!')
	elif B=='3':
		H=A.get(_c,'');print(f"\n{COLORS[_D]}Current Discord Webhook:{COLORS[_C]} {'Set'if H else _i}");print('\n1. Enter Webhook URL');print('2. Test Webhook');print('3. Disable Webhook');print('4. Back');C=safe_input(f"\n{COLORS[_D]}Select option (1-4): {COLORS[_C]}")
		if C=='1':
			I=safe_input('Enter Discord Webhook URL: ').strip()
			if I:A[_c]=I;A[_d]=_A;print_formatted(_H,'Webhook configured successfully!')
		elif C=='2'and H:send_discord_alert(A,'🔔 Webhook test successful! Your notifications are working.',_q);print_formatted(_H,'Webhook test sent!')
		elif C=='3':A[_d]=_B;print_formatted(_H,'Webhook notifications disabled!')
	elif B=='4':advanced_settings(A)
	if B in['1','2','3']:save_config(A)
	input(_t)
def advanced_settings(config):
	A=config;print(f"\n{COLORS[_Q]}=== ADVANCED SETTINGS ==={COLORS[_C]}");print(f"\n{COLORS[_D]}Performance Settings:{COLORS[_C]}");E=A.get(_N,_B);print(f"1. Performance Mode: {_j if E else _k}");print(f"\n{COLORS[_D]}Detection Settings:{COLORS[_C]}");F=A.get(_O,60);print(f"2. Check Delay: {F} seconds");G=A.get(_P,90);print(f"3. Game Load Delay: {G} seconds");D=safe_input(f"\n{COLORS[_D]}Select option to change (1-3) or Enter to go back: {COLORS[_C]}")
	if D=='1':A[_N]=not E;H='enabled'if A[_N]else'disabled';print_formatted(_H,f"Performance mode {H}!")
	elif D=='2':
		B=safe_input('Enter new check delay in seconds (30-300): ').strip()
		if B and B.isdigit():
			C=int(B)
			if 30<=C<=300:A[_O]=C;print_formatted(_H,f"Check delay set to {C} seconds!")
			else:print_formatted(_G,'Delay must be between 30-300 seconds!')
	elif D=='3':
		B=safe_input('Enter new game load delay in seconds (30-180): ').strip()
		if B and B.isdigit():
			C=int(B)
			if 30<=C<=180:A[_P]=C;print_formatted(_H,f"Game load delay set to {C} seconds!")
			else:print_formatted(_G,'Delay must be between 30-180 seconds!')
	save_config(A)
def view_current_config():A=load_config();print(f"\n{COLORS[_Q]}=== CURRENT CONFIGURATION ==={COLORS[_C]}");print(f"{COLORS[_D]}Game ID:{COLORS[_C]} {A.get(_M,_i)}");print(f"{COLORS[_D]}Private Server:{COLORS[_C]} {A.get(_K,_i)}");print(f"{COLORS[_D]}Check Delay:{COLORS[_C]} {A.get(_O,60)} seconds");print(f"{COLORS[_D]}Game Load Delay:{COLORS[_C]} {A.get(_P,90)} seconds");print(f"{COLORS[_D]}Game Verification Interval:{COLORS[_C]} {A.get(_A0,300)} seconds");print(f"{COLORS[_D]}Discord Webhook:{COLORS[_C]} {'Set'if A.get(_c)else _i}");print(f"{COLORS[_D]}Webhook Alerts:{COLORS[_C]} {_j if A.get(_d,_A)else _k}");print(f"{COLORS[_D]}Performance Mode:{COLORS[_C]} {_j if A.get(_N,_B)else _k}");print(f"{COLORS[_D]}Max Retries:{COLORS[_C]} {A.get(_x,3)}");print(f"{COLORS[_D]}Auto Rejoin:{COLORS[_C]} {_j if A.get(_A1,_A)else _k}");print(f"{COLORS[_D]}Browser Preference:{COLORS[_C]} {A.get(_y,_g)}");print(f"{COLORS[_D]}Error Detection:{COLORS[_C]} {_j if A.get(_z,_A)else _k}");input(_t)
def test_game_join():
	A=load_config();B=A.get(_M);C=A.get(_K,'')
	if not B and not C:print_formatted(_G,'No game ID or private server configured. Please configure settings first.');input(_f);return
	print_formatted(_E,f"Testing game join");print_formatted(_E,'This will close Roblox and attempt to join the game...');D=safe_input('Continue with test? (y/n): ').strip().lower()
	if D not in['y','yes']:return
	E=attempt_game_join(A)
	if E:print_formatted(_H,'Game join test completed successfully!')
	else:print_formatted(_G,'Game join test failed!')
	input(_t)
def show_system_info():
	G='None';B='No';A='Yes';print(f"\n{COLORS[_Q]}=== SYSTEM INFORMATION ==={COLORS[_C]}")
	if platform_info:print(f"{COLORS[_D]}Platform Type:{COLORS[_C]} {platform_info[_U]}");print(f"{COLORS[_D]}Platform Name:{COLORS[_C]} {platform_info[_I]}");print(f"{COLORS[_D]}Root Access:{COLORS[_C]} {'Available'if platform_info.get(_m)else'Limited'}");print(f"{COLORS[_D]}ADB Support:{COLORS[_C]} {A if platform_info.get(_u)else B}");print(f"{COLORS[_D]}Shell Prefix:{COLORS[_C]} {platform_info.get(_b,G)}");print(f"{COLORS[_D]}Process Check Method:{COLORS[_C]} {platform_info.get(_v,_h)}");print(f"{COLORS[_D]}Browser Launch Method:{COLORS[_C]} {platform_info.get(_w,_h)}")
	C=verify_roblox_installation();print(f"{COLORS[_D]}Roblox Installed:{COLORS[_C]} {A if C else B}")
	if C:H=is_roblox_running();print(f"{COLORS[_D]}Roblox Running:{COLORS[_C]} {A if H else B}")
	D=get_available_browsers();print(f"{COLORS[_D]}Available Browsers:{COLORS[_C]} {', '.join(D)if D else G}")
	try:E=run_shell_command('getprop ro.build.version.release',platform_info=platform_info);print(f"{COLORS[_D]}Android Version:{COLORS[_C]} {E if E else _h}")
	except:pass
	try:F=run_shell_command('getprop ro.product.model',platform_info=platform_info);print(f"{COLORS[_D]}Device Model:{COLORS[_C]} {F if F else _h}")
	except:pass
	input(_t)
def main():
	global platform_info,automation_running
	try:os.system('clear'if os.name=='posix'else'cls')
	except:pass
	print_formatted(_Q,'ROBLOX AUTO-REJOIN TOOL');print_formatted(_E,'Initializing system...')
	if not check_termux_stability():print_formatted(_F,'Termux stability issues - enabling compatibility mode')
	D=PlatformDetector();platform_info=D.detect_platform();print_formatted(_E,f"Detected platform: {platform_info[_I]}");A=load_config();A=apply_auto_optimizations(A);save_config(A)
	if not A.get(_M)and not A.get(_K):
		print_formatted(_E,'First-time setup required')
		if first_time_setup():A=load_config()
	if not verify_roblox_installation():print_formatted(_F,'Roblox not installed! Install it from Google Play.');input(_f)
	C=_L
	while _A:
		try:
			display_menu();B=safe_input(f"\n{COLORS[_D]}Choice (1-7): {COLORS[_C]}",30)
			if B=='1':configure_settings()
			elif B=='2':
				if automation_running:print_formatted(_F,'Auto-rejoin is already running!');input(_f)
				else:
					A=load_config()
					if not A.get(_M)and not A.get(_K):print_formatted(_G,'No game ID or private server configured!');input(_f)
					else:print_formatted(_E,'Starting auto-rejoin process...');C=threading.Thread(target=automation_loop,args=(A,),daemon=_A);C.start()
			elif B=='3':
				if automation_running:
					print_formatted(_E,'Stopping auto-rejoin...');automation_running=_B
					if C:C.join(timeout=5)
					print_formatted(_H,'Auto-rejoin stopped!')
				else:print_formatted(_F,'Auto-rejoin is not running!')
				input(_f)
			elif B=='4':test_game_join()
			elif B=='5':view_current_config()
			elif B=='6':show_system_info()
			elif B=='7':
				if automation_running:
					print_formatted(_E,'Stopping auto-rejoin before exit...');automation_running=_B
					if C:C.join(timeout=5)
				print_formatted(_E,'Exiting Roblox Auto-Rejoin Tool');break
			else:print_formatted(_F,'Invalid choice! Enter 1-7.');input(_f)
		except KeyboardInterrupt:
			print_formatted(_E,'Exiting...')
			if automation_running:automation_running=_B
			break
		except Exception as E:print_formatted(_G,f"Menu error: {str(E)}");time.sleep(2)
	sys.exit(0)
if __name__=='__main__':main()
