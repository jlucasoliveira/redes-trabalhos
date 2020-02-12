#import socket module
from socket import *
import sys
import threading

threads = []

server_socket = socket(AF_INET, SOCK_STREAM)

#Prepara o socket servidor
server_socket.bind(('', 9999))
server_socket.listen(5)

# reusar sockets usados anteriormente ainda nao fechados
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

def server_thread(conn_socket, addr):
    while True:
        try:
            print('Serving => {}:{}...'.format(addr[0], addr[1]))
            message = conn_socket.recv(1024).decode()
            print(message)
            if not message:
                break
            # separando por espaço a requisição recebida
            arquivo_requisitado = message.split(' ')[1]

            if arquivo_requisitado == '/':
                arquivo_requisitado = arquivo_requisitado + 'index.html'

            # 1º caractere desse split eh /, removendo com a sublista [1:]
            arquivo = open(arquivo_requisitado[1:])
            outputdata = arquivo.read()
            arquivo.close()

            # Envia um linha de cabeçalho HTTP para o socket
            cabecalho = b'HTTP/1.1 200 OK\r\n'
            conn_socket.send(cabecalho)
            # Envia o conteúdo do arquivo solicitado ao cliente
            for i in range(0, len(outputdata)):
                conn_socket.send(outputdata[i].encode())
            conn_socket.send('\r\n\r\n'.encode())
            break
        except Exception as e:
            print(e)
            # Envia uma mensagem de resposta “File not Found”
            conn_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
            # Fecha o socket cliente
            conn_socket.close()
    conn_socket.close()

while True:
    con, addr = server_socket.accept()
    sock_thread = threading.Thread(target= server_thread, args = (con, addr))
    sock_thread.start()
    threads.append(sock_thread)

for thread in threads:
    thread.join()

server_socket.close()
sys.exit()#Termina o programa depois de enviar os dados