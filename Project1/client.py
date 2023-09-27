## import `socket` module
from _thread import *
import threading
import socket
import sys  # In order to terminate the program
import argparse
def create_parser() -> argparse.ArgumentParser:
    """
    Create an argument parser object using the `argparse` module in Python.
    
    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(prog="client")
    parser.add_argument("--address", type=str, default='127.0.0.1', help="server address")
    parser.add_argument("--port", type=int, default=6789, help="port number")
    parser.add_argument("--message", type=str, default="GET /HelloWorld.html")

    return parser
parser = create_parser()
args = parser.parse_args()
# local host IP '127.0.0.1'
host = args.address

# Define the port on which you want to connect
port = args.port

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# connect to server on local computer
s.connect((host,port))

# message you send to server
message = args.message
while True:
    
    # message sent to server
    s.send(message.encode('ascii'))

    # message received from server
    data = s.recv(1024)

    # print the received message
    # here it would be a reverse of sent message
    print('Received from the server :',str(data.decode('ascii')))

    break
# close the connection
s.close()