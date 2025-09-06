#!/usr/bin/env python3
'\nEnhanced Roblox Automation Tool (Rejoiner.py)\nSupports: UGPHONE, VSPHONE, REDFINGER, Standard Android/Emulators\nAuthor: Optimized for global device support and easy configuration\n'
_c='android.intent.action.VIEW'
_b='game_verification_interval'
_a='performance_mode'
_Z='browser_preference'
_Y='max_retries'
_X='\nPress Enter to continue...'
_W='Not set'
_V='clear'
_U='packages'
_T='list'
_S='game_load_delay'
_R='check_delay'
_Q='pm'
_P='ps'
_O='auto'
_N='Press Enter to continue...'
_M='HEADER'
_L=None
_K='game_id'
_J='private_server'
_I='DEBUG'
_H='CYAN'
_G='SUCCESS'
_F='ERROR'
_E='WARNING'
_D=True
_C='RESET'
_B=False
_A='INFO'
import requests,time,os,json,subprocess,urllib.parse,re,threading,sys,logging,random
from datetime import datetime
from typing import Dict,List,Optional,Any
from queue import Queue
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler('/sdcard/roblox_automation.log'),logging.StreamHandler()])
logger=logging.getLogger('Rejoiner')
COLORS={_C:'\x1b[0m',_A:'\x1b[94m',_G:'\x1b[92m',_E:'\x1b[93m',_F:'\x1b[91m','BOLD':'\x1b[1m',_H:'\x1b[96m',_M:'\x1b[95m',_I:'\x1b[90m'}
CONFIG_FILE='/sdcard/roblox_config.json'
ROBLOX_PACKAGE='com.roblox.client'
BROWSER_PACKAGES=['com.android.chrome','com.sec.android.app.sbrowser','com.google.android.webview','org.mozilla.firefox','com.opera.browser','com.brave.browser','com.microsoft.emmx','com.vivaldi.browser']
automation_running=_B
platform_info=_L
last_game_join_time=_L
error_codes_detected=set()
consecutive_failures=0
last_error_time=0
last_game_verification_time=0
last_crash_time=0
last_discord_alert=0
def print_formatted(level,message):B=message;A=level;C=datetime.now().strftime('%Y-%m-%d %H:%M:%S');D={_A:_A,_G:'OK',_E:'WARN',_F:_F,_M:'====',_I:_I}.get(A,A);E=COLORS.get(A,COLORS[_C]);print(f"{E}{C} [{D}] {B}{COLORS[_C]}");logger.log(getattr(logging,A.upper(),logging.INFO),B)
def safe_input(prompt,timeout=30):
	'Input with timeout to prevent freezing';C=prompt
	try:
		B=Queue()
		def D():
			try:A=input(C);B.put(A)
			except:B.put(_L)
		A=threading.Thread(target=D);A.daemon=_D;A.start();A.join(timeout)
		if A.is_alive():print_formatted(_E,'Input timeout - returning empty');return''
		return B.get()or''
	except:
		try:return input(C)
		except:return''
def run_shell_command(command,timeout=15,platform_info=_L):
	A=command
	try:
		if isinstance(A,str):A=A.split()
		B=subprocess.run(A,capture_output=_D,text=_D,timeout=timeout)
		if B.stderr and'permission denied'not in B.stderr.lower():print_formatted(_I,f"Command stderr: {B.stderr.strip()}")
		return B.stdout.strip()
	except subprocess.TimeoutExpired:print_formatted(_E,f"Command timeout: {A}");return''
	except Exception as C:print_formatted(_F,f"Command failed: {A} - {str(C)}");return''
def load_config():
	A={_K:'',_J:'',_R:60,_Y:3,'auto_rejoin':_D,_Z:_O,'error_detection':_D,_a:_B,_S:90,'discord_webhook':'','webhook_alerts':_B,_b:300,'minimal_ui':_D,'reduced_logging':_B,'extended_timeouts':_B,'setup_completed':_B}
	try:
		if not os.path.exists(CONFIG_FILE):
			with open(CONFIG_FILE,'w')as B:json.dump(A,B,indent=4)
			run_shell_command(f"chmod 644 {CONFIG_FILE}");print_formatted(_A,'Created new config file');return A
		with open(CONFIG_FILE,'r')as B:
			C=json.load(B)
			for(D,E)in A.items():
				if D not in C:C[D]=E
			return C
	except Exception as F:print_formatted(_F,f"Config load error: {F}");return A
def save_config(config):
	try:
		with open(CONFIG_FILE,'w')as A:json.dump(config,A,indent=4)
		run_shell_command(f"chmod 644 {CONFIG_FILE}");print_formatted(_G,'Config saved');return _D
	except Exception as B:print_formatted(_F,f"Config save error: {B}");return _B
def is_roblox_running(retries=1,delay=2):
	'Improved Roblox detection that works on all devices';B=delay;A=retries
	for C in range(A):
		try:
			F=run_shell_command(['pidof',ROBLOX_PACKAGE])
			if F.strip():print_formatted(_I,'Roblox PID found via pidof');return _D
			try:
				G=[[_P,'-A','-o','pid,comm'],[_P,'-A'],[_P]]
				for H in G:
					try:
						D=run_shell_command(H)
						if D and ROBLOX_PACKAGE in D:print_formatted(_I,'Roblox process found via ps');return _D
					except:continue
			except:pass
			try:
				E=run_shell_command([_Q,_T,_U,'running'])
				if E and ROBLOX_PACKAGE in E:print_formatted(_I,'Roblox found in running services');return _D
			except:pass
			if C<A-1:time.sleep(B)
		except Exception as I:
			print_formatted(_F,f"Roblox running check error: {str(I)}")
			if C<A-1:time.sleep(B)
	print_formatted(_I,'Roblox not found');return _B
def close_roblox(config=_L):
	A=config
	try:
		print_formatted(_A,'Closing Roblox...');C=[['am','force-stop',ROBLOX_PACKAGE],['pkill','-f',ROBLOX_PACKAGE],['killall',ROBLOX_PACKAGE]]
		for D in C:
			try:run_shell_command(D);time.sleep(2)
			except:continue
		run_shell_command(['input','keyevent','KEYCODE_HOME']);time.sleep(2);E=A.get('force_kill_delay',10)if A else 10;time.sleep(E)
		if is_roblox_running():print_formatted(_E,'Roblox still running, clearing cache...');run_shell_command([_Q,_V,ROBLOX_PACKAGE]);time.sleep(5)
		B=not is_roblox_running()
		if B:print_formatted(_G,'Roblox closed successfully')
		else:print_formatted(_F,'Failed to close Roblox completely')
		return B
	except Exception as F:print_formatted(_F,f"Failed to close Roblox: {str(F)}");return _B
def is_in_game(game_id,private_server=''):
	'Simplified game detection that works without dumpsys';F='TOTAL'
	try:
		if not is_roblox_running():print_formatted(_I,'Roblox not running - not in game');return _B
		try:
			B=run_shell_command(['dumpsys','meminfo',ROBLOX_PACKAGE])
			if B:
				if F in B:
					G=[A for A in B.split('\n')if F in A][0]
					try:
						E=int(''.join(filter(str.isdigit,G.split()[0])))
						if E>300000:print_formatted(_I,f"High memory usage ({E} KB) - likely in game");return _D
					except:pass
		except:pass
		try:
			C=run_shell_command([_P,'-A','-o','pid,state,comm'])
			if C and ROBLOX_PACKAGE in C:
				H=C.split('\n')
				for A in H:
					if ROBLOX_PACKAGE in A and('R'in A or'S'in A or'Foreground'in A):print_formatted(_I,'Roblox in active state - likely in game');return _D
		except:pass
		try:
			D=run_shell_command(['logcat','-d','-s','Unity'])
			if D and('Loading'in D or'LevelLoad'in D):print_formatted(_I,'Game loading detected in logs');return _D
		except:pass
		print_formatted(_I,'No strong indicators of being in game found');return _B
	except Exception as I:print_formatted(_F,f"Game detection error: {str(I)}");return _B
def launch_via_deep_link(game_id,private_server=''):
	A=game_id
	try:
		if private_server:print_formatted(_A,'Skipping deep link for private server, using browser method');return _B
		print_formatted(_A,f"Launching via deep link: Game ID {A}");B=f"roblox://experiences/start?placeId={A}";E=run_shell_command(['am','start','-a',_c,'-d',B]);C=time.time()
		while time.time()-C<120:
			if is_roblox_running():print_formatted(_G,'Roblox launched via deep link');time.sleep(10);return _D
			time.sleep(3)
		print_formatted(_E,'Deep link launched but Roblox not running after extended wait');return _B
	except Exception as D:print_formatted(_F,f"Deep link launch failed: {str(D)}");return _B
def launch_via_browser(game_id,private_server='',config=_L):
	F=config;E=private_server
	try:
		if not E:print_formatted(_E,'No private server link provided for browser launch');return _B
		print_formatted(_A,f"Launching via browser: Game ID {game_id}");B=F.get(_Z,_O)if F else _O;A=[]
		for C in BROWSER_PACKAGES:
			G=run_shell_command([_Q,_T,_U,C])
			if C in G:A.append(C)
		D=['am','start','-a',_c,'-d',E]
		if B!=_O and B in A:D.append(B)
		elif A:D.append(A[0])
		J=run_shell_command(D);H=time.time()
		while time.time()-H<120:
			if is_roblox_running():print_formatted(_G,'Roblox launched via browser');time.sleep(10);return _D
			time.sleep(3)
		print_formatted(_E,'Browser launch initiated but Roblox not running after extended wait');return _B
	except Exception as I:print_formatted(_F,f"Browser launch failed: {str(I)}");return _B
def attempt_game_join(config):
	A=config;global last_game_join_time,consecutive_failures,last_error_time;C=A.get(_K);B=A.get(_J,'')
	if not C and not B:print_formatted(_F,'No game ID or private server specified in config');return _B
	E=time.time()
	if E-last_error_time<10:F=10-(E-last_error_time);print_formatted(_A,f"Waiting {F:.1f} seconds after recent error...");time.sleep(F)
	if is_roblox_running()and is_in_game(C,B):print_formatted(_G,'Already in game - no need to relaunch');last_game_join_time=time.time();consecutive_failures=0;return _D
	print_formatted(_A,'Attempting to join game')
	if not close_roblox(A):print_formatted(_E,'Failed to close Roblox properly')
	time.sleep(3);D=_B
	if B:
		print_formatted(_A,'Trying launch method: browser')
		if launch_via_browser(C,B,A):
			if wait_for_game_join(A,timeout=180):last_game_join_time=time.time();print_formatted(_G,'Successfully joined game using browser');D=_D
			else:print_formatted(_E,'Game join timeout with browser launch')
		else:print_formatted(_E,'Browser launch failed')
	else:
		print_formatted(_A,'Trying launch method: deep link')
		if launch_via_deep_link(C,B):
			if wait_for_game_join(A,timeout=180):last_game_join_time=time.time();print_formatted(_G,'Successfully joined game using deep link');D=_D
			else:print_formatted(_E,'Game join timeout with deep link')
		else:print_formatted(_E,'Deep link launch failed')
	if D:consecutive_failures=0;return _D
	else:consecutive_failures+=1;last_error_time=time.time();print_formatted(_F,'Game join attempt failed');return _B
def wait_for_game_join(config,timeout=180):
	A=config;C=time.time();D=A.get(_K);E=A.get(_J,'');B=A.get(_S,90);print_formatted(_A,f"Waiting {B} seconds for game to load before checking...");time.sleep(B)
	while time.time()-C<timeout:
		if is_in_game(D,E):print_formatted(_G,'Detected successful join in game');return _D
		time.sleep(5)
	print_formatted(_A,'Game join timeout');return _B
def automation_loop(config):
	A=config;global automation_running,last_game_join_time,consecutive_failures,last_game_verification_time;automation_running=_D;print_formatted(_G,'Automation started successfully!');E=A.get(_Y,3);K=A.get(_b,300);F=A.get(_a,_B)
	while automation_running:
		try:
			G=A.get(_K);C=time.time();D=is_roblox_running();H=is_in_game(G,A.get(_J,''))if D else _B
			if not D:
				print_formatted(_A,'Roblox not running - launching...')
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=C
				else:consecutive_failures+=1
			elif not H:
				print_formatted(_A,'Not in target game - rejoining...')
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=C
				else:consecutive_failures+=1
			else:
				print_formatted(_A,'Already in game and running normally - monitoring...');consecutive_failures=0
				if last_game_verification_time==0:last_game_verification_time=C
			if consecutive_failures>=E:print_formatted(_E,f"Multiple consecutive failures ({consecutive_failures}) - but continuing to try...");consecutive_failures=0
			B=A.get(_R,60)
			if F:B=max(B,120);print_formatted(_A,f"Performance mode - waiting {B} seconds before next check...")
			else:print_formatted(_A,f"Waiting {B} seconds before next check...")
			I=random.uniform(.8,1.2)*B;time.sleep(I)
		except KeyboardInterrupt:print_formatted(_A,'Automation interrupted by user');break
		except Exception as J:print_formatted(_F,f"Automation loop error: {str(J)}");time.sleep(10)
	automation_running=_B;print_formatted(_A,'Automation stopped')
def display_menu():
	try:os.system(_V if os.name=='posix'else'cls')
	except:pass
	print(f"\n{COLORS[_M]}{'='*40}");print(f" ROBLOX AUTOMATION TOOL");print(f"{'='*40}{COLORS[_C]}");print(f"\n{COLORS[_H]}1.{COLORS[_C]} Configure");print(f"{COLORS[_H]}2.{COLORS[_C]} Start");print(f"{COLORS[_H]}3.{COLORS[_C]} Stop");print(f"{COLORS[_H]}4.{COLORS[_C]} Test Join");print(f"{COLORS[_H]}5.{COLORS[_C]} Config");print(f"{COLORS[_H]}6.{COLORS[_C]} System Info");print(f"{COLORS[_H]}7.{COLORS[_C]} Exit")
	if automation_running:print(f"\n{COLORS[_G]}Status: RUNNING{COLORS[_C]}")
	else:print(f"\n{COLORS[_E]}Status: STOPPED{COLORS[_C]}")
def configure_settings():
	A=load_config();print(f"\n{COLORS[_M]}=== QUICK CONFIGURATION ==={COLORS[_C]}");C=A.get(_K,'');D=A.get(_J,'')
	if D:print(f"\n{COLORS[_H]}Current Private Server:{COLORS[_C]} {D}")
	else:print(f"\n{COLORS[_H]}Current Game ID:{COLORS[_C]} {C if C else _W}")
	print('\n1. Enter Game ID');print('2. Enter Private Server Link');print('3. Back to Main Menu');B=safe_input(f"\n{COLORS[_H]}Select option (1-3): {COLORS[_C]}")
	if B=='1':
		E=safe_input('Enter Game ID: ').strip()
		if E:A[_K]=E;A[_J]='';print_formatted(_G,'Game ID set successfully!')
	elif B=='2':
		print('\nEnter Private Server Link');F=safe_input('Private Server Link: ').strip()
		if F:A[_J]=F;print_formatted(_G,'Private Server link set successfully!')
	if B in['1','2']:save_config(A)
	input(_X)
def view_current_config():A=load_config();print(f"\n{COLORS[_M]}=== CURRENT CONFIGURATION ==={COLORS[_C]}");print(f"{COLORS[_H]}Game ID:{COLORS[_C]} {A.get(_K,_W)}");print(f"{COLORS[_H]}Private Server:{COLORS[_C]} {A.get(_J,_W)}");print(f"{COLORS[_H]}Check Delay:{COLORS[_C]} {A.get(_R,60)} seconds");print(f"{COLORS[_H]}Game Load Delay:{COLORS[_C]} {A.get(_S,90)} seconds");input(_X)
def test_game_join():
	A=load_config();B=A.get(_K);C=A.get(_J,'')
	if not B and not C:print_formatted(_F,'No game ID or private server configured.');input(_N);return
	print_formatted(_A,'Testing game join');print_formatted(_A,'This will close Roblox and attempt to join the game...');D=safe_input('Continue with test? (y/n): ').strip().lower()
	if D not in['y','yes']:return
	E=attempt_game_join(A)
	if E:print_formatted(_G,'Game join test completed successfully!')
	else:print_formatted(_F,'Game join test failed!')
	input(_X)
def main():
	global automation_running
	try:
		try:os.system(_V if os.name=='posix'else'cls')
		except:pass
		print(f"{COLORS[_M]}ROBLOX AUTOMATION TOOL{COLORS[_C]}");print(f"{COLORS[_A]}Initializing...{COLORS[_C]}")
		try:
			E=run_shell_command([_Q,_T,_U,ROBLOX_PACKAGE])
			if ROBLOX_PACKAGE not in E:print_formatted(_E,'Roblox not found! Please install it from Google Play.')
		except:print_formatted(_E,'Could not verify Roblox installation')
		A=_L
		while _D:
			try:
				display_menu();B=safe_input(f"\n{COLORS[_H]}Choice (1-7): {COLORS[_C]}",30)
				if B=='1':configure_settings()
				elif B=='2':
					if automation_running:print_formatted(_E,'Automation is already running!');input(_N)
					else:
						C=load_config()
						if not C.get(_K)and not C.get(_J):print_formatted(_F,'No game ID or private server configured!');input(_N)
						else:A=threading.Thread(target=automation_loop,args=(C,),daemon=_D);A.start()
				elif B=='3':
					if automation_running:
						print_formatted(_A,'Stopping automation...');automation_running=_B
						if A:A.join(timeout=5)
						print_formatted(_G,'Automation stopped!')
					else:print_formatted(_E,'Automation is not running!')
					input(_N)
				elif B=='4':test_game_join()
				elif B=='5':view_current_config()
				elif B=='6':print_formatted(_A,'System info not available in simplified version');input(_N)
				elif B=='7':
					if automation_running:
						print_formatted(_A,'Stopping automation before exit...');automation_running=_B
						if A:A.join(timeout=5)
					print_formatted(_A,'Thank you for using Roblox Automation Tool!');break
				else:print_formatted(_E,'Invalid choice! Please enter 1-7.');input(_N)
			except KeyboardInterrupt:
				print_formatted(_A,'\nExiting...')
				if automation_running:automation_running=_B
				break
			except Exception as D:print_formatted(_F,f"Menu error: {str(D)}");time.sleep(2)
	except Exception as D:
		print_formatted(_F,f"Critical error: {str(D)}")
		try:
			if automation_running:
				automation_running=_B
				if A:A.join(timeout=3)
		except:pass
		sys.exit(1)
if __name__=='__main__':main()
