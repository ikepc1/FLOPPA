from floppaREC import *

def main():
    fl = FlasherOperationRec()
    while True:
        fl.listen_for_cmd()

if __name__ == '__main__':
    main()
