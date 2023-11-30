

import socket
import time
import random

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Assign IP address and port number to the socket
udp_socket.bind(('127.0.0.1', 12000))
print("Started UDP server on port 12000")

# Initialize a dictionary to store the last heartbeat time for each client
client_last_heartbeat = {}

while True:
    try:
        # Receive the client packet along with the address it is coming from
        client_message, client_address = udp_socket.recvfrom(1024)

        # Check if the message is a Heartbeat packet
        if client_message == b'Heartbeat':
            # Update the last heartbeat time for the client
            client_last_heartbeat[client_address] = time.time()
            continue

        # Capitalize the message from the client
        client_message = client_message.upper()

        # Generate a random number
        rand_num = random.randint(0, 10)

        # If rand_num is less than 4, we consider the packet lost and do not respond
        if rand_num < 4:
            continue

        # Otherwise, the server responds to the client
        udp_socket.sendto(client_message, client_address)

        # Check if the client has sent a heartbeat recently
        if client_address in client_last_heartbeat:
            elapsed_time = time.time() - client_last_heartbeat[client_address]
            print(elapsed_time)
            if elapsed_time > 10:
                print("Client", client_address, "has stopped responding to Heartbeats")
                del client_last_heartbeat[client_address]

    except KeyboardInterrupt:
        # Handle Ctrl+C to exit the loop gracefully
        print("Server stopped by user.")
        break
    except Exception as error:
        # Handle other exceptions gracefully
        print("An error occurred:", str(error))