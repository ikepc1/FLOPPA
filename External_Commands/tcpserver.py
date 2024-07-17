import socketserver
from pathlib import Path
from datetime import datetime
import ast
import re

from config import FLOPPA_DIR
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

    def get_response(self) -> str:
        '''This function reads the most recent response from the flasher.
        '''
        recent_response = Path(FLOPPA_DIR) / 'response_logs.txt'
        with recent_response.open() as openfile:
            response = openfile.readlines()[-1]
        return response+'\n'

    def format_response(self, response: str) -> str:
        ''' This function reformats the response string to be human-readable.
            Adds UTC ISO 8601 time stamp.
        '''
        formatted_response = ""
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        response_dict = ast.literal_eval(re.search('({.+})', response).group(0))
        for k, v in response_dict.items():
            if k == "SOL(1)R":
                k = "SOLAR"
            if k == "msg":
                formatted_response += str(v).split("_")[0]
            else:
                formatted_response += " " + now + " " k.lower() + " " + str(v) + " "
        return formatted_response

    def handle(self) -> None:
        ''' This function 
        '''
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("Received from {}:".format(self.client_address[0]))
        print(self.data)
        try:
            self.cmds[self.data]()
            self.request.sendall(bytes(self.formatted_response(self.get_response()),'utf-8'))
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

