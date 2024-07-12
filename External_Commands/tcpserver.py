import socketserver
from pathlib import Path

from config import FLOPPA_DIR
from external_commands import flash_flasher, test_voltages

class InclineFlasherTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    cmds = {'FLASH':flash_flasher,
            'VOLTAGE':test_voltages}
    
    def get_response(self) -> str:
        '''This function reads the most recent response from the flasher.
        '''
        recent_response = Path(FLOPPA_DIR) / 'response_logs.txt'
        with recent_response.open() as openfile:
            response = openfile.readlines()[-1]
        return response

    def handle(self) -> None:
        ''' This function 
        '''
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("Received from {}:".format(self.client_address[0]))
        print(self.data)
        self.cmds[self.data]()
        # send back the flasher response
        self.request.sendall(self.get_response())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), InclineFlasherTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
