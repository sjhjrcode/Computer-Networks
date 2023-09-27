## import `socket` module
from _thread import *
import threading
from socket import *
import sys  # In order to terminate the program
print_lock = threading.Lock()
serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
host = "127.0.0.1"
# Fill in start
port = 6789
serverSocket.bind((host,port))
serverSocket.listen(5)
# Fill in end
def threaded(connectionSocket):
    while True:
        # Establish the connection
        print('ready to serve...')
        #connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(1024)
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()

            # send an HTTP OK header line into socket
            # Fill in start
            connectionSocket.send(b'\nHTTP/1.1 200 OK\n\n')
            ## TODO: call the proper function with argument (b'\nHTTP/1.1 200 OK\n\n')
            ## Note that b'' converts the string into UTF-8-encoded bytes

            #Fill in end

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

            #connectionSocket.close()
            break

        except IOError:
            # send response message for file not found
            # fill in start
            connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            connectionSocket.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
            #fill in end

            #close client socket
            #fill in start
            #connectionSocket.close()
            #fill in end
            break
    print_lock.release()
    connectionSocket.close()

while True:
 
    # establish connection with client
    c, addr = serverSocket.accept()
 
    # lock acquired by client
    print_lock.acquire()
    print('Connected to :', addr[0], ':', addr[1])
 
    # Start a new thread and return its identifier
    start_new_thread(threaded, (c,))



serverSocket.close()

sys.exit()

