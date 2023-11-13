from floppaREC import *

def main():
    '''Create the flopparec class and isten for a command forever.
    '''
    fl = FlasherOperationRec()
    while True:
        fl.listen_for_cmd()

if __name__ == '__main__':
    main()
