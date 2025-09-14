#!/usr/bin/env python3
'\nEnhanced Roblox Automation Tool\nReliable game rejoining with user identification and improved UI\n'
_l='Auto-detect'
_k='android.intent.action.VIEW'
_j='max_crash_recovery'
_i='game_verification_interval'
_h='browser_preference'
_g='Unknown'
_f='\x1b[96m'
_e='\x1b[93m'
_d='Not set'
_c='packages'
_b='list'
_a='clear'
_Z='auto'
_Y='Press Enter to continue...'
_X='\nPress Enter to continue...'
_W='pm'
_V='ps'
_U=None
_T='GAME'
_S='user_id'
_R='game_load_delay'
_Q='max_retries'
_P='check_delay'
_O='USER'
_N='crash_recovery'
_M='performance_mode'
_L='HEADER'
_K='private_server'
_J='game_id'
_I='DEBUG'
_H='ERROR'
_G='WARNING'
_F='CYAN'
_E='SUCCESS'
_D=True
_C='INFO'
_B=False
_A='RESET'
import requests,time,os,json,subprocess,urllib.parse,re,threading,sys,logging,random
from datetime import datetime
from typing import Dict,List,Optional,Any,Tuple
from queue import Queue
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler('/sdcard/roblox_rejoiner.log'),logging.StreamHandler()])
logger=logging.getLogger('Rejoiner')
COLORS={_A:'\x1b[0m',_C:'\x1b[94m',_E:'\x1b[92m',_G:_e,_H:'\x1b[91m','BOLD':'\x1b[1m',_F:_f,_L:'\x1b[95m',_I:'\x1b[90m',_O:_e,_T:_f}
CONFIG_FILE='/sdcard/roblox_config.json'
ROBLOX_PACKAGE='com.roblox.client'
BROWSER_PACKAGES=['com.android.chrome','com.sec.android.app.sbrowser','com.google.android.webview','org.mozilla.firefox','com.opera.browser','com.brave.browser','com.microsoft.emmx','com.vivaldi.browser']
automation_running=_B
platform_info=_U
last_game_join_time=_U
error_codes_detected=set()
consecutive_failures=0
last_error_time=0
last_game_verification_time=0
last_crash_time=0
last_discord_alert=0
current_username=_g
user_id_map={}
def print_formatted(level,message):B=message;A=level;C=datetime.now().strftime('%Y-%m-%d %H:%M:%S');D={_C:_C,_E:'OK',_G:'WARN',_H:_H,_L:'====',_I:_I,_O:_O,_T:_T}.get(A,A);E=COLORS.get(A,COLORS[_A]);print(f"{E}{C} [{D}] {B}{COLORS[_A]}");logger.log(getattr(logging,A.upper(),logging.INFO),B)
def safe_input(prompt,timeout=30):
	'Input with timeout to prevent freezing';C=prompt
	try:
		B=Queue()
		def D():
			try:A=input(C);B.put(A)
			except:B.put(_U)
		A=threading.Thread(target=D);A.daemon=_D;A.start();A.join(timeout)
		if A.is_alive():print_formatted(_G,'Input timeout - returning empty');return''
		return B.get()or''
	except:
		try:return input(C)
		except:return''
def run_shell_command(command,timeout=15):
	A=command
	try:
		if isinstance(A,str):A=A.split()
		B=subprocess.run(A,capture_output=_D,text=_D,timeout=timeout)
		if B.stderr and'permission denied'not in B.stderr.lower():print_formatted(_I,f"Command stderr: {B.stderr.strip()}")
		return B.stdout.strip()
	except subprocess.TimeoutExpired:print_formatted(_G,f"Command timeout: {A}");return''
	except Exception as C:print_formatted(_H,f"Command failed: {A} - {str(C)}");return''
def load_config():
	A={_J:'',_K:'',_P:60,_Q:3,'auto_rejoin':_D,_h:_Z,'error_detection':_D,_M:_B,_R:90,'discord_webhook':'','webhook_alerts':_B,_i:300,'minimal_ui':_D,'reduced_logging':_B,'extended_timeouts':_B,'setup_completed':_B,_S:'','detect_username':_D,'roblox_path':'/data/data/com.roblox.client',_N:_D,_j:5}
	try:
		if not os.path.exists(CONFIG_FILE):
			with open(CONFIG_FILE,'w')as B:json.dump(A,B,indent=4)
			run_shell_command(f"chmod 644 {CONFIG_FILE}");print_formatted(_C,'Created new config file');return A
		with open(CONFIG_FILE,'r')as B:
			C=json.load(B)
			for(D,E)in A.items():
				if D not in C:C[D]=E
			return C
	except Exception as F:print_formatted(_H,f"Config load error: {F}");return A
def save_config(config):
	try:
		with open(CONFIG_FILE,'w')as A:json.dump(config,A,indent=4)
		run_shell_command(f"chmod 644 {CONFIG_FILE}");print_formatted(_E,'Config saved');return _D
	except Exception as B:print_formatted(_H,f"Config save error: {B}");return _B
def get_roblox_users():
	'Get currently logged in Roblox users from device';F='name';C={}
	try:
		A='/data/data/com.roblox.client/files/accounts'
		if os.path.exists(A):
			for B in os.listdir(A):
				if B.isdigit():
					G=B;D=os.path.join(A,B,'user.info')
					if os.path.exists(D):
						try:
							with open(D,'r')as H:
								E=json.load(H)
								if F in E:C[G]=E[F]
						except:pass
		return C
	except Exception as I:print_formatted(_H,f"Error getting Roblox users: {I}");return{}
def detect_current_user():
	'Detect the currently active Roblox user';global user_id_map;user_id_map=get_roblox_users();B=load_config();A=B.get(_S,'')
	if A and A in user_id_map:return A,user_id_map[A]
	if user_id_map:
		for(C,D)in user_id_map.items():return C,D
	return'',_g
def is_roblox_running(retries=2,delay=1):
	'Improved Roblox detection that works on all devices';B=delay;A=retries
	for C in range(A):
		try:
			F=run_shell_command(['pidof',ROBLOX_PACKAGE])
			if F.strip():print_formatted(_I,'Roblox PID found via pidof');return _D
			G=[[_V,'-A'],[_V],[_V,'aux']]
			for H in G:
				try:
					D=run_shell_command(H)
					if D and ROBLOX_PACKAGE in D:print_formatted(_I,'Roblox process found via ps');return _D
				except:continue
			try:
				E=run_shell_command([_W,_b,_c,'running'])
				if E and ROBLOX_PACKAGE in E:print_formatted(_I,'Roblox found in running services');return _D
			except:pass
			if C<A-1:time.sleep(B)
		except Exception as I:
			print_formatted(_H,f"Roblox running check error: {str(I)}")
			if C<A-1:time.sleep(B)
	print_formatted(_I,'Roblox not found');return _B
def close_roblox():
	try:
		print_formatted(_C,'Closing Roblox...');B=[['am','force-stop',ROBLOX_PACKAGE],['pkill','-f',ROBLOX_PACKAGE],['killall',ROBLOX_PACKAGE]]
		for C in B:
			try:run_shell_command(C);time.sleep(2)
			except:continue
		run_shell_command(['input','keyevent','KEYCODE_HOME']);time.sleep(2)
		if is_roblox_running():print_formatted(_G,'Roblox still running, clearing cache...');run_shell_command([_W,_a,ROBLOX_PACKAGE]);time.sleep(5)
		A=not is_roblox_running()
		if A:print_formatted(_E,'Roblox closed successfully')
		else:print_formatted(_H,'Failed to close Roblox completely')
		return A
	except Exception as D:print_formatted(_H,f"Failed to close Roblox: {str(D)}");return _B
def is_in_game(game_id,private_server=''):
	'Enhanced game detection using multiple verification methods';M='TOTAL';L='grep';K='dumpsys';C=game_id
	try:
		if not is_roblox_running():print_formatted(_I,'Roblox not running - not in game');return _B
		A=0;N=5
		try:
			B=''
			try:B=run_shell_command([K,'meminfo',ROBLOX_PACKAGE])
			except:B=run_shell_command([_V,'-o','rss,comm','-A','|',L,ROBLOX_PACKAGE])
			if B:
				if M in B:
					O=[A for A in B.split('\n')if M in A][0]
					try:
						P=int(''.join(filter(str.isdigit,O.split()[0])))
						if P>300000:A+=1;print_formatted(_I,'Memory check passed')
					except:pass
		except Exception as D:print_formatted(_I,f"Memory check error: {str(D)}")
		try:
			E=run_shell_command([_V,'-A','-o','pid,state,comm'])
			if E and ROBLOX_PACKAGE in E:
				Q=E.split('\n')
				for F in Q:
					if ROBLOX_PACKAGE in F and('R'in F or'S'in F):A+=1;print_formatted(_I,'Process state check passed');break
		except:pass
		try:
			H=run_shell_command(['pidof',ROBLOX_PACKAGE])
			if H:
				G=run_shell_command(['logcat','-d','--pid',H,'-s','Unity','Roblox'])
				if G:
					R=['Loading','LevelLoad','PlaceId','Experience','Gameplay']
					for I in R:
						if I in G:A+=1;print_formatted(_I,f"Log indicator '{I}' found");break
					if C and C in G:A+=2;print_formatted(_I,f"Game ID {C} found in logs")
		except:pass
		try:
			J=run_shell_command([K,'SurfaceFlinger','|',L,ROBLOX_PACKAGE])
			if J and ROBLOX_PACKAGE in J:A+=1;print_formatted(_I,'SurfaceFlinger activity detected')
		except:pass
		print_formatted(_I,f"Game verification score: {A}/{N}");return A>=2
	except Exception as D:print_formatted(_H,f"Game detection error: {str(D)}");return _B
def launch_via_deep_link(game_id,private_server=''):
	A=game_id
	try:
		if private_server:print_formatted(_C,'Skipping deep link for private server, using browser method');return _B
		print_formatted(_C,f"Launching via deep link: Game ID {A}");B=f"roblox://experiences/start?placeId={A}";E=run_shell_command(['am','start','-a',_k,'-d',B]);C=time.time()
		while time.time()-C<120:
			if is_roblox_running():print_formatted(_E,'Roblox launched via deep link');time.sleep(15);return _D
			time.sleep(3)
		print_formatted(_G,'Deep link launched but Roblox not running after extended wait');return _B
	except Exception as D:print_formatted(_H,f"Deep link launch failed: {str(D)}");return _B
def launch_via_browser(game_id,private_server='',config=_U):
	F=config;E=private_server
	try:
		if not E:print_formatted(_G,'No private server link provided for browser launch');return _B
		print_formatted(_C,f"Launching via browser: Game ID {game_id}");B=F.get(_h,_Z)if F else _Z;A=[]
		for C in BROWSER_PACKAGES:
			G=run_shell_command([_W,_b,_c,C])
			if C in G:A.append(C)
		D=['am','start','-a',_k,'-d',E]
		if B!=_Z and B in A:D.append(B)
		elif A:D.append(A[0])
		J=run_shell_command(D);H=time.time()
		while time.time()-H<120:
			if is_roblox_running():print_formatted(_E,'Roblox launched via browser');time.sleep(15);return _D
			time.sleep(3)
		print_formatted(_G,'Browser launch initiated but Roblox not running after extended wait');return _B
	except Exception as I:print_formatted(_H,f"Browser launch failed: {str(I)}");return _B
def attempt_game_join(config):
	A=config;global last_game_join_time,consecutive_failures,last_error_time,current_username;C=A.get(_J);B=A.get(_K,'')
	if not C and not B:print_formatted(_H,'No game ID or private server specified in config');return _B
	H,E=detect_current_user();current_username=E;print_formatted(_O,f"Active user: {E} ({H})");F=time.time()
	if F-last_error_time<10:G=10-(F-last_error_time);print_formatted(_C,f"Waiting {G:.1f} seconds after recent error...");time.sleep(G)
	if is_roblox_running()and is_in_game(C,B):print_formatted(_E,'Already in game - no need to relaunch');last_game_join_time=time.time();consecutive_failures=0;return _D
	print_formatted(_C,'Attempting to join game')
	if not close_roblox():print_formatted(_G,'Failed to close Roblox properly')
	time.sleep(3);D=_B
	if B:
		print_formatted(_C,'Trying launch method: browser')
		if launch_via_browser(C,B,A):
			if wait_for_game_join(A,timeout=180):last_game_join_time=time.time();print_formatted(_E,'Successfully joined game using browser');D=_D
			else:print_formatted(_G,'Game join timeout with browser launch')
		else:print_formatted(_G,'Browser launch failed')
	else:
		print_formatted(_C,'Trying launch method: deep link')
		if launch_via_deep_link(C,B):
			if wait_for_game_join(A,timeout=180):last_game_join_time=time.time();print_formatted(_E,'Successfully joined game using deep link');D=_D
			else:print_formatted(_G,'Game join timeout with deep link')
		else:print_formatted(_G,'Deep link launch failed')
	if D:consecutive_failures=0;return _D
	else:consecutive_failures+=1;last_error_time=time.time();print_formatted(_H,'Game join attempt failed');return _B
def wait_for_game_join(config,timeout=180):
	A=config;C=time.time();D=A.get(_J);E=A.get(_K,'');B=A.get(_R,90);print_formatted(_C,f"Waiting {B} seconds for game to load before checking...");time.sleep(B)
	while time.time()-C<timeout:
		if is_in_game(D,E):print_formatted(_E,'Detected successful join in game');return _D
		time.sleep(5)
	print_formatted(_C,'Game join timeout');return _B
def automation_loop(config):
	A=config;global automation_running,last_game_join_time,consecutive_failures,last_game_verification_time;automation_running=_D;print_formatted(_E,'Automation started successfully!');M=A.get(_Q,3);N=A.get(_i,300);F=A.get(_M,_B);G=A.get(_N,_D);H=A.get(_j,5);B=0
	while automation_running:
		try:
			I=A.get(_J);D=time.time();E=is_roblox_running();J=is_in_game(I,A.get(_K,''))if E else _B
			if not E:
				print_formatted(_C,'Roblox not running - launching...')
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=D;B=0
				else:consecutive_failures+=1;B+=1
			elif not J:
				print_formatted(_C,'Not in target game - rejoining...')
				if attempt_game_join(A):consecutive_failures=0;last_game_verification_time=D;B=0
				else:consecutive_failures+=1;B+=1
			else:
				print_formatted(_C,'Already in game and running normally - monitoring...');consecutive_failures=0;B=0
				if last_game_verification_time==0:last_game_verification_time=D
			if G and B>=H:print_formatted(_G,f"Multiple crashes detected ({B}), performing recovery...");run_shell_command([_W,_a,ROBLOX_PACKAGE]);time.sleep(5);B=0
			C=A.get(_P,60)
			if F:C=max(C,120);print_formatted(_C,f"Performance mode - waiting {C} seconds before next check...")
			else:print_formatted(_C,f"Waiting {C} seconds before next check...")
			K=random.uniform(.8,1.2)*C;time.sleep(K)
		except KeyboardInterrupt:print_formatted(_C,'Automation interrupted by user');break
		except Exception as L:print_formatted(_H,f"Automation loop error: {str(L)}");time.sleep(10)
	automation_running=_B;print_formatted(_C,'Automation stopped')
def display_menu():
	try:os.system(_a if os.name=='posix'else'cls')
	except:pass
	A=load_config();B,C=detect_current_user();print(f"\n{COLORS[_L]}{'='*50}");print(f"        ROBLOX REJOINER");print(f"{'='*50}{COLORS[_A]}");print(f"\n{COLORS[_O]}Current User: {C} ({B}){COLORS[_A]}")
	if A.get(_K):print(f"{COLORS[_T]}Private Server: {A.get(_K)[:50]}...{COLORS[_A]}")
	elif A.get(_J):print(f"{COLORS[_T]}Game ID: {A.get(_J)}{COLORS[_A]}")
	else:print(f"{COLORS[_G]}No game configured!{COLORS[_A]}")
	print(f"\n{COLORS[_F]}1.{COLORS[_A]} Configure Settings");print(f"{COLORS[_F]}2.{COLORS[_A]} Start Automation");print(f"{COLORS[_F]}3.{COLORS[_A]} Stop Automation");print(f"{COLORS[_F]}4.{COLORS[_A]} Test Game Join");print(f"{COLORS[_F]}5.{COLORS[_A]} View Configuration");print(f"{COLORS[_F]}6.{COLORS[_A]} User Management");print(f"{COLORS[_F]}7.{COLORS[_A]} Exit")
	if automation_running:print(f"\n{COLORS[_E]}Status: AUTOMATION ACTIVE{COLORS[_A]}")
	else:print(f"\n{COLORS[_G]}Status: READY{COLORS[_A]}")
def configure_settings():
	A=load_config();print(f"\n{COLORS[_L]}=== CONFIGURATION SETTINGS ==={COLORS[_A]}");C=A.get(_J,'');D=A.get(_K,'');E=A.get(_S,'')
	if D:print(f"\n{COLORS[_F]}Current Private Server:{COLORS[_A]} {D}")
	else:print(f"\n{COLORS[_F]}Current Game ID:{COLORS[_A]} {C if C else _d}")
	print(f"{COLORS[_F]}Current User ID:{COLORS[_A]} {E if E else _l}");print('\n1. Set Game ID');print('2. Set Private Server Link');print('3. Set User ID');print('4. Configure Advanced Settings');print('5. Back to Main Menu');B=safe_input(f"\n{COLORS[_F]}Select option (1-5): {COLORS[_A]}")
	if B=='1':
		F=safe_input('Enter Game ID: ').strip()
		if F:A[_J]=F;A[_K]='';print_formatted(_E,'Game ID set successfully!')
	elif B=='2':
		print('\nEnter Private Server Link');G=safe_input('Private Server Link: ').strip()
		if G:A[_K]=G;A[_J]='';print_formatted(_E,'Private Server link set successfully!')
	elif B=='3':
		print('\nEnter User ID (leave blank for auto-detection)');H=safe_input('User ID: ').strip();A[_S]=H
		if H:print_formatted(_E,'User ID set successfully!')
		else:print_formatted(_E,'User ID set to auto-detect')
	elif B=='4':configure_advanced_settings(A)
	if B in['1','2','3','4']:save_config(A)
	input(_X)
def configure_advanced_settings(config):
	I='disabled';H='enabled';G='Disabled';F='Enabled';A=config;print(f"\n{COLORS[_L]}=== ADVANCED SETTINGS ==={COLORS[_A]}");print(f"1. Check Delay: {A.get(_P,60)} seconds");print(f"2. Game Load Delay: {A.get(_R,90)} seconds");print(f"3. Max Retries: {A.get(_Q,3)}");print(f"4. Performance Mode: {F if A.get(_M,_B)else G}");print(f"5. Crash Recovery: {F if A.get(_N,_D)else G}");print(f"6. Back");B=safe_input(f"\n{COLORS[_F]}Select option (1-6): {COLORS[_A]}")
	if B=='1':
		C=safe_input(f"Enter check delay (current: {A.get(_P,60)}): ")
		if C.isdigit():A[_P]=int(C);print_formatted(_E,'Check delay updated!')
	elif B=='2':
		C=safe_input(f"Enter game load delay (current: {A.get(_R,90)}): ")
		if C.isdigit():A[_R]=int(C);print_formatted(_E,'Game load delay updated!')
	elif B=='3':
		E=safe_input(f"Enter max retries (current: {A.get(_Q,3)}): ")
		if E.isdigit():A[_Q]=int(E);print_formatted(_E,'Max retries updated!')
	elif B=='4':A[_M]=not A.get(_M,_B);D=H if A[_M]else I;print_formatted(_E,f"Performance mode {D}!")
	elif B=='5':A[_N]=not A.get(_N,_D);D=H if A[_N]else I;print_formatted(_E,f"Crash recovery {D}!")
def user_management():
	global user_id_map;print(f"\n{COLORS[_L]}=== USER MANAGEMENT ==={COLORS[_A]}");user_id_map=get_roblox_users()
	if not user_id_map:print_formatted(_G,'No Roblox users found on this device!');print('Please log in to Roblox first to detect users.');input(_X);return
	print('\nDetected Roblox Users:')
	for(E,(A,F))in enumerate(user_id_map.items(),1):print(f"{E}. {F} ({A})")
	print(f"\n{len(user_id_map)+1}. Refresh User List");print(f"{len(user_id_map)+2}. Back to Main Menu");C=safe_input(f"\n{COLORS[_F]}Select user (1-{len(user_id_map)+2}): {COLORS[_A]}")
	if C.isdigit():
		B=int(C)
		if 1<=B<=len(user_id_map):A=list(user_id_map.keys())[B-1];D=load_config();D[_S]=A;save_config(D);print_formatted(_E,f"Selected user: {user_id_map[A]}")
		elif B==len(user_id_map)+1:user_id_map=get_roblox_users();print_formatted(_E,'User list refreshed!')
		elif B==len(user_id_map)+2:return
	input(_X)
def view_current_config():B='Yes';A=load_config();C,D=detect_current_user();print(f"\n{COLORS[_L]}=== CURRENT CONFIGURATION ==={COLORS[_A]}");print(f"{COLORS[_F]}Game ID:{COLORS[_A]} {A.get(_J,_d)}");print(f"{COLORS[_F]}Private Server:{COLORS[_A]} {A.get(_K,_d)}");print(f"{COLORS[_F]}User ID:{COLORS[_A]} {A.get(_S,_l)}");print(f"{COLORS[_F]}Current User:{COLORS[_A]} {D} ({C})");print(f"{COLORS[_F]}Check Delay:{COLORS[_A]} {A.get(_P,60)} seconds");print(f"{COLORS[_F]}Game Load Delay:{COLORS[_A]} {A.get(_R,90)} seconds");print(f"{COLORS[_F]}Max Retries:{COLORS[_A]} {A.get(_Q,3)}");print(f"{COLORS[_F]}Performance Mode:{COLORS[_A]} {B if A.get(_M,_B)else'No'}");print(f"{COLORS[_F]}Crash Recovery:{COLORS[_A]} {B if A.get(_N,_D)else'No'}");input(_X)
def test_game_join():
	A=load_config();B=A.get(_J);C=A.get(_K,'')
	if not B and not C:print_formatted(_H,'No game ID or private server configured.');input(_Y);return
	print_formatted(_C,'Testing game join');print_formatted(_C,'This will close Roblox and attempt to join the game...');D=safe_input('Continue with test? (y/n): ').strip().lower()
	if D not in['y','yes']:return
	E=attempt_game_join(A)
	if E:print_formatted(_E,'Game join test completed successfully!')
	else:print_formatted(_H,'Game join test failed!')
	input(_X)
def main():
	global automation_running,current_username
	try:
		try:os.system(_a if os.name=='posix'else'cls')
		except:pass
		print(f"{COLORS[_L]}ROBLOX REJOINER {COLORS[_A]}");print(f"{COLORS[_C]}Initializing...{COLORS[_A]}");F,E=detect_current_user();current_username=E;print_formatted(_O,f"Detected user: {E} ({F})")
		try:
			G=run_shell_command([_W,_b,_c,ROBLOX_PACKAGE])
			if ROBLOX_PACKAGE not in G:print_formatted(_G,'Roblox not found! Please install it from Google Play.')
		except:print_formatted(_G,'Could not verify Roblox installation')
		A=_U
		while _D:
			try:
				display_menu();B=safe_input(f"\n{COLORS[_F]}Choice (1-7): {COLORS[_A]}",30)
				if B=='1':configure_settings()
				elif B=='2':
					if automation_running:print_formatted(_G,'Automation is already running!');input(_Y)
					else:
						C=load_config()
						if not C.get(_J)and not C.get(_K):print_formatted(_H,'No game ID or private server configured!');input(_Y)
						else:A=threading.Thread(target=automation_loop,args=(C,),daemon=_D);A.start()
				elif B=='3':
					if automation_running:
						print_formatted(_C,'Stopping automation...');automation_running=_B
						if A:A.join(timeout=5)
						print_formatted(_E,'Automation stopped!')
					else:print_formatted(_G,'Automation is not running!')
					input(_Y)
				elif B=='4':test_game_join()
				elif B=='5':view_current_config()
				elif B=='6':user_management()
				elif B=='7':
					if automation_running:
						print_formatted(_C,'Stopping automation before exit...');automation_running=_B
						if A:A.join(timeout=5)
					print_formatted(_C,'Thank you for using Roblox Rejoiner!');break
				else:print_formatted(_G,'Invalid choice! Please enter 1-7.');input(_Y)
			except KeyboardInterrupt:
				print_formatted(_C,'\nExiting...')
				if automation_running:automation_running=_B
				break
			except Exception as D:print_formatted(_H,f"Menu error: {str(D)}");time.sleep(2)
	except Exception as D:
		print_formatted(_H,f"Critical error: {str(D)}")
		try:
			if automation_running:
				automation_running=_B
				if A:A.join(timeout=3)
		except:pass
		sys.exit(1)
if __name__=='__main__':main()
