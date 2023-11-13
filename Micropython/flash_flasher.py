from floppaSNCT import *
from time import sleep        

fl = FlasherOperationSNCT()
fl.send_cmd('FLASHER_ON')
sleep(1)
fl.send_cmd('FLASHER_OFF')
sleep(1)
