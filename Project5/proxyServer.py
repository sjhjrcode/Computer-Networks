from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address of the Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerPort = 8888
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(5)

while True:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024)
    if message:
        message = message.decode()

        # Extract the filename from the given message
        print(message.split()[1])
        filename = message.split()[1].partition("/")[2]
        fileExist = "false"
        filetouse = "./" + filename
        try:
            # Check whether the file exists in the cache
            f = open(filetouse[1:], "r")
            outputdata = f.readlines()
            fileExist = "true"

            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n\r\n")

            # Send each line of outputdata to the client
            for line in outputdata:
                tcpCliSock.send(line.encode())
            print('Read from cache')

        except IOError:
            print('File Exist:', fileExist)
            if fileExist == "false":
                c = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.", "", 1)
                print('Host Name:', hostn)
                try:
                    c.connect((hostn, 80))
                    fileobj = c.makefile('rwb', 0)

                    # Improved HTTP request format
                    http_get_request = "GET / HTTP/1.0\r\nHost: {}\r\n\r\n".format(hostn)
                    print("HTTP GET Request:", http_get_request)  # Debug print
                    fileobj.write(http_get_request.encode())
                    # Read the response into buffer
                    buff = fileobj.readlines()

                    # Write to cache and send to client
                    with open("./" + filename, "wb") as tmpFile:
                        for item in buff:
                            tmpFile.write(item)
                            tcpCliSock.send(item)

                except Exception as e:
                    print('Illegal request:', e)

        tcpCliSock.close()

tcpSerSock.close()
