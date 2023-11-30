import socket
import time

def ping():
    try:
        min_rtt = float('inf')
        max_rtt = 0
        total_rtt = 0
        lost_packets = 0
        last_heartbeat = time.time()

        for i in range(10):
            start = time.time()
            message = f'Ping#{i} {time.ctime(start)}'

            try:
                # Create a UDP socket and send the message
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                port = 12000
                server_addr = '127.0.0.1'
                sock.connect((server_addr, port))
                sock.settimeout(11)
                sock.sendto(message.encode('ascii'), (server_addr, port))

                print("Sent:", message)

                data, server = sock.recvfrom(1024)
                print("Received:", data.decode('ascii'))

                end_time = time.time()
                elapsed = end_time - start

                print("RTT:", elapsed)

                min_rtt = min(min_rtt, elapsed)
                max_rtt = max(max_rtt, elapsed)
                total_rtt += elapsed
            except socket.timeout:
                print(f"#{i} Requested Timeout\n")
                lost_packets += 1
            finally:
                print("Closing socket")
                sock.close()

            if i % 5 == 0:
                current_time = time.time()
                if current_time - last_heartbeat > 10:
                    print("Sending Heartbeat")
                    sock.sendto(b'Heartbeat', (server_addr, port))
                    last_heartbeat = current_time

        avg_rtt = total_rtt / (10 - lost_packets)
        packet_loss_rate = (lost_packets / 10) * 100

        print("Minimum RTT:", min_rtt)
        print("Maximum RTT:", max_rtt)
        print("Average RTT:", avg_rtt)
        print("Packet Loss Rate:", packet_loss_rate, "%")

    except KeyboardInterrupt:
        print("Ping stopped by user.")

# Call the ping() function to start the ping operations
ping()