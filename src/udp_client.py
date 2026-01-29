from socket import *

# from slide
serverName = "localhost"
serverPort = 12000

# create UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# get user keyboard input (Python 3 version of raw_input)
message = input("Input sentence: ")

# attach server name, port to message; send into socket
clientSocket.sendto(message.encode(), (serverName, serverPort))

# read reply characters from socket into string
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# print out received string and close socket
print("From Server:", modifiedMessage.decode())
clientSocket.close()
