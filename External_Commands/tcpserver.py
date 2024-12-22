import socketserver
from pathlib import Path
from datetime import datetime
import ast
from abc import ABC, abstractmethod

from config import FLOPPA_DIR, FLASH_TIME
from external_commands import flash_flasher, test_voltages

def get_current_utc() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat(' ')

class CommandParser(ABC):
    '''This is the definition of an interface for parsing 
    commands over the TCP connection.
    '''
    args = []

    @abstractmethod
    def excecute(self, cmd: list[bytes]) -> None:
        '''This is the method which parses the command bytestring 
        and excecutes the appropriate function.
        '''

    @abstractmethod
    def format_response(self, resp: dict) -> bytes:
        '''This is the method which takes the flasher's response 
        and formats it appropriately.
        '''

class VoltageCommandParser(CommandParser):
    '''This is the implementation of a command parser for the voltage
    TCP command.
    '''

    def excecute(self, cmd: list[bytes]) -> None:
        '''This excecutes the voltage command.
        '''
        test_voltages()

    def format_response(self, resp: dict) -> bytes:
        '''This formats the flasher's voltage response.
        '''
        formatted_response = ""
        now = get_current_utc()
        for k, v in resp.items():
            if k == "SOLA(1)R":
                k = "SOLAR"
            if k == "time":
                continue
            elif k == "msg":
                formatted_response += "VOLTAGE " + now
            else:
                formatted_response += " " + k.lower() + " " + str(v)
        return bytes(formatted_response + "\n",'utf-8')

class FlashCommandParser(CommandParser):
    '''This is the implementation of a command parser for the FLASH
    command.
    '''

    def excecute(self, cmd: list[bytes]) -> None:
        '''This excecutes the flash command.
        '''
        if len(cmd) > 1:
            args = [int(arg) for arg in cmd[1:]]
        elif len(cmd) == 1:
            args = [FLASH_TIME]
        if args[0] > 60:
            args[0] = 60
        self.args = args
        flash_flasher(*args)

    def format_response(self, resp: dict) -> bytes:
        '''This is the method which takes the flasher's response 
        and formats it appropriately.
        '''
        formatted_response = ""
        now = get_current_utc()
        for k, v in resp.items():
            if k == "time":
                continue
            elif k == "msg":
                formatted_response += f"FLASH {self.args[0]} " + now
            else:
                formatted_response += " " + k.lower() + " " + str(v)
        return bytes(formatted_response + "\n",'utf-8')


class InclineFlasherTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    cmds = {b'FLASH':FlashCommandParser(),
            b'VOLTAGE':VoltageCommandParser()}


    @property
    def cmd_ids(self) -> str:
        return ' '.join([str(key,'utf-8') for key in self.cmds])

    @staticmethod
    def get_response() -> str:
        '''This function reads the most recent response from the flasher.
        '''
        recent_response = Path(FLOPPA_DIR) / 'response_logs.txt'
        with recent_response.open() as openfile:
            response = openfile.readlines()[-1]
        return response+'\n'

    def format_response(self, command: str, response: str) -> str:
        ''' This function reformats the response string to be human-readable.
            Adds UTC ISO 8601 time stamp.
        '''
        formatted_response = ""
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        response_dict = ast.literal_eval(response)
        for k, v in response_dict.items():
            if k == "SOLA(1)R":
                k = "SOLAR"
            if k == "time":
                continue
            elif k == "msg":
                formatted_response += str(command) + " " + now
            else:
                formatted_response += " " + k.lower() + " " + str(v)
        return formatted_response + "\n"

    def handle(self) -> None:
        ''' This function handles the request and response between TCP server and client.
        '''
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        cmd_list = self.data.split(b' ')
        print("Received from {}:".format(self.client_address[0]))
        print(self.data)
        try:
            parser = self.cmds[cmd_list[0]]
            parser.excecute(cmd_list)
            flasher_resp = ast.literal_eval(self.get_response())
            if flasher_resp["msg"] == "NOMESSAGE" or flasher_resp["msg"] == "Invalid Message":
                resp = bytes("NO RESPONSE FROM FLASHER\n", 'utf-8')
            else:
                resp = parser.format_response(flasher_resp)
            #resp = self.format_response(' '.join([c.decode('utf-8') for c in cmd_list]), self.get_response())
        except KeyError:
            resp = f"{str(self.data,'utf-8')}: unrecognized command\nPossible commands: {self.cmd_ids}\n"
            resp = bytes(resp,'utf-8')
        self.request.sendall(resp)
        # send back the flasher response
        #self.request.sendall(bytes(self.get_response(),'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), InclineFlasherTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

