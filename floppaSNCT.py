from machine import Pin, ADC
from time import sleep
import utime
from display import Display
from LoRa import LoRa, Command, FlasherOperation

class RelayON(Command):    
    def excecute(self, msg):
        self.display_on_lcd(msg)
        print(msg)

class RelayOFF(Command):    
    def excecute(self, msg):
        self.display_on_lcd(msg)
        print(msg)
        
class Voltage(Command):
    def excecute(self, msg):
        self.display_on_lcd(msg)
        print(msg)
        
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
    cmds = {'ON':RelayON(),
            'OFF':RelayOFF(),
            'VOLTAGE':Voltage(),
            'NOMESSAGE':NoMessage()
            }
    def __init__(self):
        self.display = Display()
        self.display.display_text('Flasher active')
        print('Flasher control module active')
