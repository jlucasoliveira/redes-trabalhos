# UDPPingerServer.py
# precisaremos do modulo random para gerar perdas de pacotes aleatorias
import random
from socket import *
# Cria um socket UDO
# Note o uso de SOCK_DGRAM para pacotes UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Atribui um endereco IP e um numero de porta ao socket
serverSocket.bind(('', 12000))
while True:
    # Gera um numero aleatorio de 0 a 10
    rand = random.randint(0, 10)
    # Recebe do cliente o pacote junto com seu endereco de destino
    message, address = serverSocket.recvfrom(1024)
    # Escreve a mensagem em letras maiusculas
    message = message.upper()
    # Se rand < 4, consideramos que o pacote foi perdido
    if rand < 4:
        continue
    # Caso contrario, o servidor responde
    serverSocket.sendto(message, address)
