from socket import *
import time


HOST = 'localhost'
PORTA = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
for i in range(1, 11):
    try:
        mensagem = 'Ping {} {}.'.format(i, time.ctime())
        start = time.time()
        clientSocket.sendto(mensagem.encode(), (HOST, PORTA))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        end = time.time()
        print("\n" + modifiedMessage.decode())
        print("RTT: {0:.7f}".format(end-start))
    except timeout:
        print("Solicitacao {} expirada.".format(i))

clientSocket.close()
