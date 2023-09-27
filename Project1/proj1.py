## import `socket` module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket

# Fill in start
port = 6789
serverSocket.bind(('127.0.0.1',port))
serverSocket.listen(1)
#Fill in end

while True:
    # Establish the connection
    print('ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        #send one HTTP header line into socket
        #Fill in start
        connectionSocket.send(b'\nHTTP/1.1 200 OK\n\n')
        #connectionSocket.send(outputdata)
        #Fill in end

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        #connectionSocket.close()

    except IOError:
        #send response message for file not found
        #fill in start
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        #fill in end

        #close client socket
        #fill in start
        #connectionSocket.close()
        #fill in end
    connectionSocket.close()

serverSocket.close()

sys.exit()

