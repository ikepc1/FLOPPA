import os
import time

from config import TCPPORT, MONITORING_INTERVAL

while True:
    os.system(f'echo VOLTAGE | nc localhost {TCPPORT}')
    time.sleep(MONITORING_INTERVAL * 3600)
