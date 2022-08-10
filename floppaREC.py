from machine import Pin, ADC, reset
from time import sleep
import utime
from display import Display
import json
from LoRa import LoRa, Command, FlasherOperation

PINS = {'relay':13,
        'pot':37
    }

class NoMessage(Command):
    '''This class is the excecutes a hardware reset. (Only invoked if no
    message has been received before timeout)
    '''
    def __str__(self):
        return 'No Message'
    
    def excecute(self, msg):
        '''This is the implementation of the excecute command for when no
        message is received.
        '''
        self.display_on_lcd(msg)
        reset()

class RelayON(Command):
    '''This is the implementation of the relay on command. It switches
    the relay on.
    '''
    relay = Pin(PINS['relay'], Pin.OUT)
    
    def __str__(self):
        return 'RelayON command'
    
    def excecute(self, msg):
        '''This is the implementation of the excecute command for RelayOn
        '''
        self.display_on_lcd(msg)
        self.relay.value(0)
        LoRa().send({'msg':'ON'})
        print('Relay ON sent')

class RelayOFF(Command):
    '''This is the implementation of the relay off command, it turns
    off the relay
    '''
    relay = Pin(PINS['relay'], Pin.OUT)

    def __str__(self):
        return 'RelayOFF Command'
    
    def excecute(self, msg):
        '''This is the implementation of the excecute command for RelayOFF.
        '''
        self.display_on_lcd(msg)
        self.relay.value(1)
        LoRa().send({'msg':'OFF'})
        print('Relay OFF sent')
        
class Voltage(Command):
    '''This is the implementation of the voltage query command.
    '''
    pot = ADC(Pin(PINS['pot']))
    
    def __str__(self):
        return 'Voltage command'
    
    def excecute(self, msg):
        '''This is the implementation of the excecute method for the voltage command.
        It reads the voltage and sends them in a message to the control tower.
        '''
        self.display_on_lcd(msg)
        voltages = self.voltage_dict(self.read_battery(),self.read_battery(),self.read_battery())
        LoRa().send(voltages)
        print('voltage msg sent')
        
    def voltage_dict(self, sol, batt1, batt2):
        '''This method returns a dictionary with the appropriate key-value
        pairs to send the solar voltage (sol), battery 1 voltage (batt1),
        and battery 2 voltage (batt2)
        '''
        return {'msg':'VOLTAGE','SOLAR':sol, 'BATT1':batt1, 'BATT2':batt2}
    
    def read_battery(self):
        '''This method converts the pin reading to a voltage'''
        return self.pot.read()*(3.3/4095.0)/(1-(5/6))
    
class InvalidMessage(Command):
    '''This is the implementation of the invalid message command.
    '''
    def __str__(self):
        return 'Invalid message'
    
    def excecute(self, msg):
        self.display_on_lcd(msg)
        print('Invalid message')
    
class FlasherOperationRec(FlasherOperation):
    '''This is the implementation of FlasherOperation() for the incline
    flasher receiver LoRa module.
    '''
    relay = Pin(PINS['relay'], Pin.OUT)
    cmds = {'ON':RelayON(),
            'OFF':RelayOFF(),
            'VOLTAGE':Voltage(),
            'NOMESSAGE':NoMessage()
            }
    def __init__(self):
        self.relay.value(1)
        self.display = Display()
        self.display.display_text('Flasher active')
        print('Flasher active')
