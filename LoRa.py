from config import *
from machine import Pin, SoftSPI, ADC
from time import sleep
import utime
from sx127x import SX127x
from display import Display
import json

class LoRa:
    '''This class contols the SX127x module on the heltec lora 32 v2'''
    def __init__(self):
        self.device_spi = SoftSPI(baudrate = 10000000, 
                                    polarity = 0, phase = 0, bits = 8, firstbit = SoftSPI.MSB,
                                    sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
                                    mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
                                    miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))
        self.sx1276 = SX127x(self.device_spi, pins=device_config, parameters=lora_parameters)
        
    def listen(self):
        '''This method listens for a message.
        Returns: the message as a dict, or an empty dict if no message was received.
        '''
        if self.sx1276.received_packet():
            return self.parse_payload()
        else:
            return {'msg': 'NOMESSAGE'}
        
    def parse_payload(self):
        '''This method loads the json payload data. If an incomplete message is received,
        an empty dictionary is returned.
        '''
        try:
            payload_dict = json.loads(self.sx1276.read_payload())
        except:
            payload_dict = {'msg': 'Invalid Message'}
        payload_dict['rssi'] = self.sx1276.packet_rssi()
        return payload_dict
        
        
    def send(self, payload_dict):
        '''This method sends a message.
        Parameters:
        payload_dict: the dict to be sent
        '''
        self.sx1276.println(json.dumps(payload_dict))

class Command:
    '''This is the base class for commands that the esp32 can
    excecute locally. Subclasses must override the excecute method,
    and the implementation must be added to the control class's
    command dictionary.
    '''
    def excecute(self, msg):
        '''This method should be overridden by the specific command implementation'''
        pass
    
    def display_on_lcd(self, msg):
        '''This method displays the message on the LCD
        Parameters:
        disp: Display() object
        msg: message dict
        '''
        Display().display_lines(self.msg2list(msg))
        
    def msg2list(self, msg: dict):
        '''This method converts a message dictionary to a list of strings to print'''
        lines = [str(msg['msg']), 'confirmed']
        for key in msg:
            lines.append(key + ' ' + str(msg[key]))
        return lines

class NoMessage(Command):
    def excecute(self, msg):
        print(msg)
        
class InvalidMessage(Command):
    def excecute(self, msg):
        pass

def waiting_for_timeout(start_time, timeout_time = 10):
    '''This function checks if an amount of time greater than a set
    timeout time (timeout_time: int (secs)) is yet to pass. If less than
    the timeout time has passed since the start time, True is returned.
    If more time than the timeout time has passed, False is returned.
    '''
    return (utime.time() - start_time) < timeout_time

class FlasherOperation:
    '''This is the interface class for point to point communication 
    between flasher controllers in the field. Subclasses need to define
    commands with their handles and command class name as key value 
    pairs e.g. cmds = {'SAMPLECMD': SampleCommand()}
    '''
    cmds = {'NOMESSAGE':NoMessage(),
            'INVALIDMESSAGE':InvalidMessage()
            }
            
    def create_cmd_msg(self, cmd):
        '''This method returns a command message dictionary to be used as
        a transmission payload'''
        return {'msg': cmd}
    
    def send_cmd(self, cmd):
        '''This method sends a command over LORA, then listens for a 
        response command.
        '''
        command = self.create_cmd_msg(cmd)
        print(command)
        LoRa().send(command)
        self.listen_for_cmd()
        
    def waiting_for_msg(self, msg):
        '''This method checks if a command message has been received.
        It returns True if no message, or an incomplete message, was
        received. It returns False if a message has been received.
        '''
        try:
            return msg['msg'] == 'NOMESSAGE'
        except:
            return True

    def listen_for_cmd(self):
        '''This method listens for an incoming LORA signal. If one is
        received, it decodes the command and excecutes it.
        '''
        start_time = utime.time()
        Display().display_text('Listening...')
        msg = {'msg':'NOMESSAGE'}
        lora = LoRa()
        while self.waiting_for_msg(msg) and waiting_for_timeout(start_time):
            msg = lora.listen()
        self.decode_cmd(msg)

    def get_command_obj(self, msg):
        '''This method retrieves the appropriate command class requested
        by a particular message
        '''
        try:
            return self.cmds[msg['msg']]
        except:
            return InvalidMessage()
            
    def decode_cmd(self, msg):
        '''This method decodes the command and calls the excecute method of
        the appropriate command class.
        '''
        command = self.get_command_obj(msg)
        print(command)
        command.excecute(msg)
        print('cmd excecuted')
            
    def listen_for_time(self, time):
        '''This method listens for an amount of seconds (time) before resetting the device
        '''
        start_time = utime.time()
        while waiting_for_timeout(start_time,time):
            self.listen_for_cmd()
        reset()
