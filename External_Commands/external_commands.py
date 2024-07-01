import os
from time import sleep
from datetime import datetime
from pathlib import Path

from config import FLOPPA_DIR, PORT, FLASH_TIME

def run_pyscript_rshell(script: str) -> None:
	'''This function invokes a python script on the esp32 via rshell.
	Parameters: 
	script: name of the script (string)
	port: name of the port the esp32 is connected to (string)
	'''
	cmd = f'rshell -p {PORT} repl pyboard import {script}~'
	os.system(cmd)
	
def copy_file_from_esp(filename: str) -> None:
	'''This function runs an rshell command on the esp32.
	Parameters: 
	cmd: name of the command e.g. cp, ls (string)
	port: name of the port the esp32 is connected to (string)
	'''
	target_path = Path(FLOPPA_DIR) / filename
	os.system(f'rshell -p {PORT} cp /pyboard/{filename} {str(target_path)}')

def write_to_logfile(filename_from_esp: str, log_filename: str) -> None:
	'''This is a generic function which appends the info copied from the 
	esp to the specified logfile.
	'''
	copy_file_from_esp(filename_from_esp)
	current_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	parent = Path(FLOPPA_DIR)
	esp_file_path = parent / filename_from_esp
	log_file_path = parent / log_filename
	with esp_file_path.open('r') as esp_file:
		data = esp_file.readlines()[0]
		with log_file_path.open('a') as log_file:
			log_file.write('time: ' + current_time + ' ' + data)

def test_voltages() -> None:
	'''This function queries the voltages at the remote site, transfers
	the voltages to the rpi, and appends them to the voltages file on 
	its storage.
	'''
	run_pyscript_rshell('query_voltage')
	sleep(15)
	write_to_logfile('recent_response_log.txt', 'response_logs.txt')
	write_to_logfile('recent_voltage.txt', 'voltages.txt')
	

# def test_voltages() -> None:
	# '''This function queries the voltages at the remote site, transfers
	# the voltages to the rpi, and appends them to the voltages file on 
	# its storage.
	# '''
	# recent_path = f'{FLOPPA_DIR}recent_voltage.txt'
	# voltage_file_path = f'{FLOPPA_DIR}voltages.txt'
	# current_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	# run_pyscript_rshell('query_voltage')
	# sleep(15)
	# copy_voltage()
	# sleep(5)
	# with open(recent_path,'r') as recent_voltage_file:
		# vs = recent_voltage_file.readlines()[0]
		# with open(voltage_file_path,'a') as voltage_file:
			# voltage_file.write('time: ' + current_time + ' ' + vs)

# def flash_flasher(ontime_secs: int = FLASH_TIME) -> None:
	# '''This function sends the command to turn the flasher on, then off 
	# after the configured ontime.
	# '''
	
	# run_pyscript_rshell('flasher_on')
	# sleep(5)
	# write_to_logfile('recent_response_log.txt', 'response_logs.txt')
	# run_pyscript_rshell('flasher_fire')
	# sleep(ontime_secs)
	# write_to_logfile('recent_response_log.txt', 'response_logs.txt')
	# run_pyscript_rshell('flasher_ceasefire')
	# sleep(ontime_secs)
	# write_to_logfile('recent_response_log.txt', 'response_logs.txt')
	# run_pyscript_rshell('flasher_off')
	# sleep(5)
	# write_to_logfile('recent_response_log.txt', 'response_logs.txt')
	
def flash_flasher(ontime_secs: int = FLASH_TIME) -> None:
	'''This function sends the command to turn the flasher on, then off 
	after the configured ontime.
	'''
	cmd = f"rshell -p {PORT} repl pyboard 'import flash_flasher ~ flash_flasher.fl.send_cmd(flash_flasher.cmd,time={ontime_secs})'~"
	os.system(cmd)
	sleep(10)
	write_to_logfile('recent_response_log.txt', 'response_logs.txt')
