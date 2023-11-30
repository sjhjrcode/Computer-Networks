import os
import sys
import struct
import time
import select
import socket
import binascii

ICMP_ECHO_REQUEST = 8

"""
Had issues with the given code tried to fix it but that didn't work so I reworked it
    csum = 0
    countTo = (len(str_in) / 2) * 2
    #print(str_in)
    count = 0
    while count < countTo:
        str_in = str(str_in)
        thisVal = ord(str_in[count+1]) * 256 + ord(str_in[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(str_in):
        csum = csum + ord(str_in[len(str_in) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    global rtt_min, rtt_max, rtt_sum, rtt_cnt
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        #Fill in start
        #Fetch the ICMP header from the IP packet
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
        #Fill in end

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    #Both LISTS and TUPLES consist of a number of objects
    #which can be referenced by their position number within the object
"""
def checksum(str):
    csum = 0
    countTo = (len(str) // 2) * 2

    count = 0
    while count < countTo:
        thisVal = str[count+1] * 256 + str[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(str):
        csum = csum + str[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while True:
        startTime = time.time()
        selectReady = select.select([mySocket], [], [], timeLeft)
        timeReceived = time.time()
        if selectReady[0] == []: 
            return "Request timed out."
        timeLeft = timeLeft - (timeReceived - startTime)
        if timeLeft <= 0:
            return "Request timed out."
        recPacket, addr = mySocket.recvfrom(1024)
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
        if type == 3:  # ICMP type 3 corresponds to destination unreachable
            if code == 0:
                return "Destination Network Unreachable"
            elif code == 1:
                return "Destination Host Unreachable"
        if packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    ICMP_ECHO_REQUEST = 8

    # Initialize checksum to zero
    myChecksum = 0

    # Create a dummy header with a 0 checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    # Get the current time
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header
    myChecksum = checksum(header + data)

    # Get the right checksum and put it in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
    else:
        myChecksum = socket.htons(myChecksum)

    # Pack the header with the correct checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    # Create the packet
    packet = header + data

    # Send the packet to the destination address
    mySocket.sendto(packet, (destAddr, 1))
    
def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")
    #SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.org/papers/sock_raw

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    # Initialize variables
    min_rtt = float('inf')
    max_rtt = float('-inf')
    sum_rtt = 0
    num_sent = 0
    num_received = 0
Untitled document
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    print("Pinging " + host + " using Python:")
    dest = socket.gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")

    # Send ping requests to a server separated by approximately one second
    for i in range(10):
        num_sent += 1
        delay = doOnePing(dest, timeout)
        print("Current Delay: ",delay)
        time.sleep(1)   # one second
        #Debugging
        #print(type(delay))
        if isinstance(delay, float):
            delay = delay * 1000  # Convert delay to ms
            min_rtt = min(min_rtt, delay)
            max_rtt = max(max_rtt, delay)
            sum_rtt += delay
            num_received += 1
            # Calculate packet loss rate and average RTT
            packet_loss_rate = (num_sent - num_received) / num_sent * 100
            avg_rtt = sum_rtt / num_received if num_received != 0 else 0

            print(f"\nMin RTT: {min_rtt} ms, Max RTT: {max_rtt} ms, Avg RTT: {avg_rtt} ms, Packet Loss Rate: {packet_loss_rate}%")


        

    # Calculate packet loss rate and average RTT
    packet_loss_rate = (num_sent - num_received) / num_sent * 100
    avg_rtt = sum_rtt / num_received if num_received != 0 else 0

    print(f"\nFinal Min RTT: {min_rtt} ms,\nFinal Max RTT: {max_rtt} ms, \nFinal Avg RTT: {avg_rtt} ms, \nFinal Packet Loss Rate: {packet_loss_rate}%")

    return delay


"Things were breaking made unit test until I could figure it out"
def test_ping():
    # Test with localhost
    delay = ping("127.0.0.1")
    assert delay == "Request timed out.", "Test failed: No response from localhost"

    # Test with a known website
    delay = ping("google.com")
    assert delay == "Request timed out.", "Test failed: No response from google.com"

    # Test with a non-existent website
    try:
        delay = ping("nonexistentwebsite.com")
    except socket.gaierror:
        pass  # Expected error
    else:
        assert False, "Test failed: Expected a socket.gaierror"

    print("All tests passed")

# Run the tests
#test_ping()

# Test Destination Network Unreachable
ping("203.0.113.0")  # This is a reserved IP address and should be unreachable

# Test Destination Host Unreachable
ping("10.255.255.255")  # This is a reserved IP address and should be unreachable
ping("127.0.0.1")
ping("www.google.com")
ping("www.bbc.co.uk")
ping("www.abc.net.au")
ping("www.dstv.com")
