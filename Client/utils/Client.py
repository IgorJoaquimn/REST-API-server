import socket
import json
from utils.socket_t import Socket

class Client:
    def __init__(self):
        #The client should strive to **reuse** the TCP connection
        #to send as many REST requests as possible.
        self.socket = Socket("localhost",5000)

    def build_message(self,headers,method,path):

        request = f"{method} {path} HTTP/1.1\r\n"
        
        headers_lines = ""
        for header, value in headers.items():
            headers_lines += f"{header}: {value}\r\n"

        request += headers_lines + "\r\n"
        request = request.encode()

        return request

    def receive_request(self):

        response = self.socket.receive(1000000)   
        message = self.parse_response(response) 

        return message 
    
    def parse_response(self,response):

        http_message = response.decode()
        _, body = http_message.split('\r\n\r\n', 1)
        
        return body

    def send_request(self, method, path):
        host = 'localhost'
        headers = {
            "Host": host,
            "User-Agent": "PythonClient",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
        }

        request = self.build_message(headers,method,path)
        
        self.socket.send(request)
        response = self.receive_request()
        print(response)


        return json.loads(response)
