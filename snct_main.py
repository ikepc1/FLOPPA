from floppaSNCT import *
from time import sleep

def main():
    fl = FlasherOperationSNCT()
    while True:
        fl.send_cmd('ON')
        sleep(5)
        fl.send_cmd('OFF')
        sleep(5)
        fl.send_cmd('VOLTAGE')
        sleep(5)
    
if __name__ == '__main__':
    main()
