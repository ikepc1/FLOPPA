from floppaSNCT import *
from time import sleep        

def main():
    fl = FlasherOperationSNCT()
    while True:    
        fl.send_cmd('FLASHER_ON')
        sleep(1)
        fl.send_cmd('FLASHER_FIRE')
        sleep(5)
        fl.send_cmd('FLASHER_CEASEFIRE')
        sleep(1)
        fl.send_cmd('FLASHER_OFF')
        sleep(1)
        fl.send_cmd('VOLTAGE')
        sleep(3600)

    
if __name__ == '__main__':
    main()
