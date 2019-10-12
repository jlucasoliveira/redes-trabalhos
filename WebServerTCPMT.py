#import socket module
from socket import *
import sys
from _thread import *
import threading

lock = threading.Lock()

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepara o socket servidor
serverSocket.bind(('', 9999))
serverSocket.listen(5)

def thread_server(connectionSocket, addr):
    while True:
        #Estabelece a conexão
        connectionSocket.bind(('', 0))
        print('Ready to serve {}:{}...'.format(addr[0], addr[1]))
        try:
            message = connectionSocket.recv(1024).decode()
            #separando por espaço a requisição recebida
            arquivo_requisitado = message.split(' ')[1]
            #1º caractere desse split eh /, removendo com a sublista [1:]
            arquivo = open(arquivo_requisitado[1:])
            outputdata = arquivo.read()
            #Envia um linha de cabeçalho HTTP para o socket
            cabecalho = 'HTTP/1.1 200 OK\r\n\r\n'
            connectionSocket.send(cabecalho.encode())
            #Envia o conteúdo do arquivo solicitado ao cliente
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
        except Exception as e:
            print(e)
            #Envia uma mensagem de resposta “File not Found”
            connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\nFile not Found'.encode())
            #Fecha o socket cliente
    connectionSocket.close()
    lock.release()

while True:
    con, addr = serverSocket.accept()
    lock.acquire()
    start_new_thread(thread_server, (con, addr))
serverSocket.close()
sys.exit()#Termina o programa depois de enviar os dados
