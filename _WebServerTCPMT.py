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

class ThreadWebServer(threading.Thread):
    def __init__(self, conn_socket, addr):
        self.conn_socket = conn_socket
        self.addr = addr
        threading.Thread.__init__(self)

    def run(self):
        while True:
            # Estabelece a conexão
            print('Ready to serve {}:{}...'.format(self.addr[0], self.addr[1]))

            try:
                message = self.conn_socket.recv(1024).decode()
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
                self.conn_socket.send(cabecalho)
                # Envia o conteúdo do arquivo solicitado ao cliente
                for i in range(0, len(outputdata)):
                    self.conn_socket.send(outputdata[i].encode())
                self.conn_socket.send('\r\n\r\n'.encode())
                self.conn_socket.close()
            except Exception as e:
                # Envia uma mensagem de resposta “File not Found”
                self.conn_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
                # Fecha o socket cliente
                self.conn_socket.close()

while True:
    con, addr = server_socket.accept()
    sock_thread = ThreadWebServer(con, addr)
    sock_thread.start()
    threads.append(sock_thread)

for thread in threads:
    thread.join()

server_socket.close()
sys.exit()#Termina o programa depois de enviar os dados