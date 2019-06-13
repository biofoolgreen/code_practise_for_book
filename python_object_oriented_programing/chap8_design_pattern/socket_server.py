'''
@Description: python面向对象编程-chap8-设计模式
@Version: 
@Author: liguoying
@Date: 2019-06-04 14:50:23
'''

##################################
####         装饰器模式        ####
##################################
import socket
import gzip
from io import BytesIO


def respond(client):
    response = input("Enter a value: ")
    client.send(bytes(response, "utf-8"))
    client.close()

class LogSocket:
    def __init__(self, socket):
        self.socket = socket
    
    def send(self, data):
        print("Send {0} to {1} ".format(data, self.socket.getpeername()[0]))
        self.socket.send(data)
    
    def close(self):
        self.socket.close()


class GzipSocket:
    def __init__(self, socket):
        self.socket = socket
    
    def send(self, data):
        buf = BytesIO()
        zipfile = gzip.GzipFile(fileobj=buf, mode='w')
        zipfile.write(data)
        zipfile.close()
        self.socket.send(buf.getvalue())
    
    def close(self):
        self.socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 2401))
server.listen(1)
try:
    while True:
        client, addr = server.accept()
        # if client.getpeername()[0] in compress_hosts:
        #     client = GzipSocket(client)
        # if log_send:
        #     client = LogSocket(client)
        respond(client)
finally:
    server.close()
