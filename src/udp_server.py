from socket import *

serverPort = 12000

# create UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# bind socket to local port number
serverSocket.bind(("", serverPort))
print("The server is ready to receive")

# loop forever
while True:
    # read from UDP socket into message, getting client's address
    message, clientAddress = serverSocket.recvfrom(2048)
    print("Received:", message.decode())

    # echo message back to this client
    serverSocket.sendto(message, clientAddress)
