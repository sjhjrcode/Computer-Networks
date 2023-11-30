import socket
import time




def ping():
    try:
        min_rtt = float('inf')
        max_rtt = 0
        total_rtt = 0
        lost_packets = 0
        for i in range(10):
            start = time.time()
            message = 'Ping #' + str(i) + " " + time.ctime(start)
            try:
                # send to the socket using `sendto`
                sock.sendto(message.encode('ascii'),(server_addr,port))
                # print the sent message
                print("Sent: " + message)
                # receive from the socket using `recvfrom`
                data, server = sock.recvfrom(1024)
                # print the received message
                print("Receive"+str(data.decode()))
                # store current time to `endt`
                endt = time.time()
                # compute the elapsed time
                telapsed = endt-start
                # print RTT
                print(telapsed)
                # update min_rtt, max_rtt, and total_rtt
                min_rtt = min(min_rtt, telapsed)
                max_rtt = max(max_rtt, telapsed)
                total_rtt += telapsed
            except socket.timeout:
                print("#" + str(i) + " Requested Time out\n")
                lost_packets += 1
        # calculate average RTT and packet loss rate
        avg_rtt = total_rtt / (10 - lost_packets)
        packet_loss_rate = (lost_packets / 10) * 100
        # print statistics
        print("Minimum RTT:", min_rtt)
        print("Maximum RTT:", max_rtt)
        print("Average RTT:", avg_rtt)
        print("Packet Loss Rate:", packet_loss_rate, "%")
    finally:
        print("closing socket")
        sock.close()





# Fill-1
# create an UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
port = 12000
# Specify server address and port number
server_addr = '127.0.0.1'
sock.connect((server_addr,port))
# set timeout for the socket
sock.settimeout(5)
ping()



# Fill-1 ends

# try:
#     for i in range(10):
#         start = time.time()
#         message = 'Ping #' + str(i) + " " + time.ctime(start)
#         try:
#             # Fill-2: do a send and receive 

#             # send to the socket using `sendto`
#             sock.sendto(message.encode('ascii'),(server_addr,port))
#             # print the sent message
#             print("Sent: " + message)
#             # receive from the socket using `recvfrom`
#             data = sock.recvfrom(1024)
#             # print the received message
#             print("Receive"+str(data))
#             # store current time to `endt`
            
#             endt = time.time()
            
#             # compute the elapsed time
#             telapsed = endt-start
            
#             # print RTT
#             print(telapsed)
#             # fill-2 ends

#         except socket.timeout:
#             print("#" + str(i) + " Requested Time out\n")

# finally:
#     print("closing socket")
#     sock.close()
    
    