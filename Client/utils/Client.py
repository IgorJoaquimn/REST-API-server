import socket
import json
from utils.socket_t import Socket

class Client:
    def __init__(self,ip,port):
        #The client should strive to **reuse** the TCP connection
        #to send as many REST requests as possible.
        self.socket = Socket(ip,port)

    def build_message(self,headers,method,path):

        request_line = f"{method} {path} HTTP/1.1\r\n"
        header_lines = "".join(f"{key}: {value}\r\n" for key, value in headers.items())

        request = request_line + header_lines + "\r\n"
        request = request.encode()

        return request
    

    def receive_request(self):
        data = None
        header = ""

        while True:
            data = self.socket.receive(1).decode('utf-8')  # Receive data from the socket
            if not data:
                break
            header += data
            if "\r\n\r\n" in header:  # Check for the end of the HTTP header
                break

        length = self.parse_response(header)
        body = self.socket.receive(length).decode('utf-8')

        return body
    
    def parse_response(self,header):
        content_length = None
        header_lines = header.split("\r\n")
        for line in header_lines:
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())
                break
        
        return content_length
    
    

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
        self.socket.close()


        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return None
