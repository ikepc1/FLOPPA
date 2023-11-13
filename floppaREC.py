from machine import Pin, ADC, reset
from time import sleep
import utime
from display import Display
import json
from LoRa import LoRa, Command, FlasherOperation
from voltage import ReadVoltages
from config import fadcratios, relay_pins, relay_names

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
        #self.display_on_lcd(msg)
        reset()

class RelayON(Command):
    '''This is the implementation of the relay on command. It switches
    the relay on.
    '''
    def __init__(self, relay_pin):
        self.pin = relay_pin
        self.relay = Pin(relay_pin, Pin.OUT)
    
    def __str__(self):
        return 'RelayON command'
    
    def excecute(self, msg):
        '''This is the implementation of the excecute command for RelayOn
        '''
        #self.display_on_lcd(msg)
        self.relay.value(0)
        LoRa().send({'msg':'RELAY_ON', 'relay':relay_names[self.pin]})
        print('Relay ON sent')

class RelayOFF(Command):
    '''This is the implementation of the relay off command, it turns
    off the relay
    '''
    def __init__(self, relay_pin):
        self.pin = relay_pin
        self.relay = Pin(relay_pin, Pin.OUT)

    def __str__(self):
        return 'RelayOFF Command'
    
    def excecute(self, msg):
        '''This is the implementation of the excecute command for RelayOFF.
        '''
        #self.display_on_lcd(msg)
        self.relay.value(1)
        LoRa().send({'msg':'RELAY_OFF', 'relay':relay_names[self.pin]})
        print('Relay OFF sent')

def read_batteries():
    ''' This function imports the pin and fadc to voltage ratios
    corresponding to the 3 voltages read in the flasher crate, and reads
    the voltage from each.
    '''  
    v1 = ReadVoltages(fadcratios['solpin'],fadcratios['solrat']).read_source_voltage()
    v2 = ReadVoltages(fadcratios['batt1pin'],fadcratios['batt1rat']).read_source_voltage()
    # ~ v3 = ReadVoltages(fadcratios['batt2pin'],fadcratios['batt2rat']).read_source_voltage()
    # v1 = ReadVoltages(fadcratios['solpin'],fadcratios['solrat']).read_pin_fadc()
    # v2 = ReadVoltages(fadcratios['batt1pin'],fadcratios['batt1rat']).read_pin_fadc()
    # v3 = ReadVoltages(fadcratios['batt2pin'],fadcratios['batt2rat']).read_pin_fadc()
    return v1,v2
        
class Voltage(Command):
    '''This is the implementation of the voltage query command.
    '''
        
    def __str__(self):
        return 'Voltage command'
    
    def voltage_dict(self, sol, batt1):
        '''This method returns a dictionary with the appropriate key-value
        pairs to send the solar voltage (sol), battery 1 voltage (batt1),
        and battery 2 voltage (batt2)
        '''
        #return {'msg':'VOLTAGE','SOLAR':sol, 'BATT1':batt1, 'BATT2':batt2}
        return {'msg':'VOLTAGE','SOLAR':sol, 'BATT1':batt1}
        
    def excecute(self, msg):
        '''This is the implementation of the excecute method for the voltage command.
        It reads the voltage and sends them in a message to the control tower.
        '''
        #self.display_on_lcd(msg)
        sol, v1 = read_batteries()
        voltages = self.voltage_dict(sol, v1)
        LoRa().send(voltages)
        print('voltage msg sent')
        
	
    
class InvalidMessage(Command):
    '''This is the implementation of the invalid message command.
    '''
    def __str__(self):
        return 'Invalid message'
    
    def excecute(self, msg):
        #self.display_on_lcd(msg)
        print('Invalid message')
    
class FlasherOperationRec(FlasherOperation):
    '''This class is the implementation of FlasherOperation for the esp32
    module at the flasher site.
    ''' 
    cmds = {'FLASHER_ON':RelayON(relay_pins['flasher_pin']),
            'FLASHER_OFF':RelayOFF(relay_pins['flasher_pin']),
            'FLASHER_FIRE':RelayON(relay_pins['hv_pin']),
            'FLASHER_CEASEFIRE':RelayOFF(relay_pins['hv_pin']),
            'BATT1_ON':RelayOFF(relay_pins['batt1_pin']),
            'BATT1_OFF':RelayON(relay_pins['batt1_pin']),
            'BATT2_ON':RelayOFF(relay_pins['batt2_pin']),
            'BATT2_OFF':RelayON(relay_pins['batt2_pin']),
            'VOLTAGE':Voltage(),
            'NOMESSAGE':NoMessage()
            }
    
    flasher_pin = Pin(relay_pins['flasher_pin'], Pin.OUT)
    solar_pin = Pin(relay_pins['hv_pin'], Pin.OUT)
    batt1_pin = Pin(relay_pins['batt1_pin'], Pin.OUT)
    batt2_pin = Pin(relay_pins['batt2_pin'], Pin.OUT)
            
    def __init__(self):
        self.flasher_pin.value(1)
        self.solar_pin.value(1)
        self.batt1_pin.value(1)
        self.batt2_pin.value(1)
        #self.display = Display()
        #self.display.display_text('Flasher active')
        print('Flasher active')
