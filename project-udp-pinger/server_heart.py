# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 12000))
print("Started UDP server on port 12000")

# Initialize dictionary to store last Heartbeat time for each client
last_heartbeat = {}

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    
    # Check if the message is a Heartbeat packet
    if message == b'Heartbeat':
        # Update the last Heartbeat time for the client
        last_heartbeat[address] = time.time()
        continue
    
    # Capitalize the message from the client
    message = message.upper()
    
    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue
        
    # Otherwise, the server responds
    serverSocket.sendto(message,  )
    
    # Check if the client has sent a Heartbeat recently
    if address in last_heartbeat:
        elapsed_time = time.time() - last_heartbeat[address]
        print(elapsed_time)
        if elapsed_time > 10:
            print("Client", address, "has stopped responding to Heartbeats")
            del last_heartbeat[address]