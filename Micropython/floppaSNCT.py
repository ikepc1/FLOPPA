from machine import Pin, ADC
from time import sleep
import utime
from display import Display
from LoRa import LoRa, Command, FlasherOperation

def write_flasher_log(msg):
    '''This function writes the response from the flasher module to the
    file flash_log.txt
    '''
    try:
        flasher_msg = msg['msg']
        rssi = msg['rssi']
    except:
        flasher_msg = rssi = 'InvalidResponse'
    with open('recent_flash_log.txt', 'w') as log_file:
        log_file.write('Command: {} rssi: {} \n'.format(flasher_msg,rssi))

class RelayON(Command):    
    def excecute(self, msg):
        self.display_on_lcd(msg)
        write_flasher_log(msg)
        print(msg)

class RelayOFF(Command):    
    def excecute(self, msg):
        self.display_on_lcd(msg)
        write_flasher_log(msg)
        print(msg)
        
class Voltage(Command):
    def excecute(self, msg):
        self.write_voltages(msg)
        self.display_on_lcd(msg)
        print(msg)
        
    def write_voltages(self, msg):
        '''This method writes the received voltages to a file.
        '''
        try:
            solar = msg['SOLAR']
            batt1 = msg['BATT1']
            rssi = msg['rssi']
            #batt2 = msg['BATT2']
        except:
            #solar = batt1 = batt2 = 'InvalidVoltage'
            solar = batt1 = rssi = 'InvalidResponse'
        with open('recent_voltage.txt', 'w') as voltage_file:
            #voltage_file.write('Solar: {} Battery1: {} Battery2: {} \n'.format(solar,batt1,batt2))
            voltage_file.write('Solar: {} Battery1: {} rssi: {} \n'.format(solar,batt1,rssi))
        
        
class NoMessage(Command):
    def excecute(self, msg):
        self.display_on_lcd(msg)
        print(msg)
        
class InvalidMessage(Command):
    def excecute(self, msg):
        self.display_on_lcd(msg)
        print(msg)
    
class FlasherOperationSNCT(FlasherOperation):
    '''This is the implementation of FlasherOperation() for the SNCT
    tower LoRa module.
    '''
    cmds = {'RELAY_ON':RelayON(),
            'RELAY_OFF':RelayOFF(),
            'VOLTAGE':Voltage(),
            'NOMESSAGE':NoMessage()
            }
    def __init__(self):
        self.display = Display()
        self.display.display_text('Flasher active')
        print('Flasher control module active')
