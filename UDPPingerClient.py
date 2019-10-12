from socket import *
from datetime import datetime
import select

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

for i in range(1,10):
	try:
		mensagem = 'Ping {} {}'.format(i, datetime.now())
		clientSocket.sendto(mensagem.encode(),(serverName, serverPort))
		clientSocket.settimeout(1)
		modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

		print(modifiedMessage)
	except socket.timeout:
		print("DEU RUIM")


clientSocket.close()

