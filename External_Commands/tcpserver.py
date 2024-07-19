import socketserver
from pathlib import Path
from datetime import datetime
import ast

from config import FLOPPA_DIR, FLASH_TIME
from external_commands import flash_flasher, test_voltages

class InclineFlasherTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    cmds = {b'FLASH':flash_flasher,
            b'VOLTAGE':test_voltages}


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
        if len(cmd_list) > 1:
            args = [int(arg) for arg in cmd_list[1:]]
        elif cmd_list[0] == b'FLASH':
            args = [FLASH_TIME]
            cmd_list.append(bytes(str(FLASH_TIME), 'utf-8'))
        else:
            args = []
        try:
            self.cmds[cmd_list[0]](*args)
            resp = self.format_response(' '.join([c.decode('utf-8') for c in cmd_list]), self.get_response())
            self.request.sendall(bytes(resp,'utf-8'))
        except KeyError:
            resp = f"{str(self.data,'utf-8')}: unrecognized command\nPossible commands: {self.cmd_ids}\n"
            self.request.sendall(bytes(resp,'utf-8'))
        # send back the flasher response
        #self.request.sendall(bytes(self.get_response(),'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), InclineFlasherTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

