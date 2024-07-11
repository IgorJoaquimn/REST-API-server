import socket
import json
from utils.socket_t import Socket

class Client:
    def __init__(self):
        #The client should strive to **reuse** the TCP connection
        #to send as many REST requests as possible.
        self.socket = Socket("localhost",5000)

    def send_request(self,method, path):
        host = 'localhost'
        headers = {
            "Host": host,
            "User-Agent": "PythonClient",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
        }
        
        print("Sending Request:")
        print(method,host,path)

        # TO-DO
        request = "".encode()
        self.socket.send(request)
        response = self.socket.receive(4096)
        return response