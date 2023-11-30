import socket
import time







# Fill-1
# create an UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
port = 12000
# Specify server address and port number
server_addr = '127.0.0.1'
sock.connect((server_addr,port))
# set timeout for the socket
sock.settimeout(5)






try:
    for i in range(10):
        start = time.time()
        message = 'Ping #' + str(i) + " " + time.ctime(start)
        try:
            # Fill-2: do a send and receive 

            # send to the socket using `sendto`
            sock.sendto(message.encode('ascii'),(server_addr,port))
            # print the sent message
            print("Sent: " + message)
            # receive from the socket using `recvfrom`
            data = sock.recvfrom(1024)
            # print the received message
            print("Receive"+str(data))
            # store current time to `endt`
            
            endt = time.time()
            
            # compute the elapsed time
            telapsed = endt-start
            
            # print RTT
            print(telapsed)
            # fill-2 ends

        except socket.timeout:
            print("#" + str(i) + " Requested Time out\n")

finally:
    print("closing socket")
    sock.close()
    
    