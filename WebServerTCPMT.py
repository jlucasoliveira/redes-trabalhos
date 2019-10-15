#import socket module
from socket import *
import sys
import random
import threading

lock = threading.Lock()
threads = []
abertos = []
fechados = []

server_socket = socket(AF_INET, SOCK_STREAM)

#Prepara o socket servidor
server_socket.bind(('', 9999))
server_socket.listen(5)

class ThreadWebServer(threading.Thread):
    def __init__(self, id, conn_socket, addr, lock):
        self.id = id
        self.conn_socket = conn_socket
        self.addr = addr
        self.lock = lock
        threading.Thread.__init__(self)

    def port_rand(self, low, up):
        _counter = 0
        while True:
            try:
                _port = random.randint(low, up)
                self.conn_socket.bind(('', _port))
            except:
                _counter += 1

            if _counter > 100:
                break


    def run(self):
        while True:
            # Estabelece a conexão
            try:
                self.port_rand(40000, 65000)
            except:
                sys.exit()
            print('Ready to serve {}:{}...'.format(self.addr[0], self.addr[1]))

            try:
                message = self.conn_socket.recv(1024).decode()
                if not message:
                    self.conn_socket.close()
                    global threads
                    del threads[self.id]
                    break
                # separando por espaço a requisição recebida
                arquivo_requisitado = message.split(' ')[1]

                # 1º caractere desse split eh /, removendo com a sublista [1:]
                arquivo = open(arquivo_requisitado[1:])
                outputdata = arquivo.read()

                # Envia um linha de cabeçalho HTTP para o socket
                cabecalho = b'HTTP/1.1 200 OK\r\n'
                self.conn_socket.send(cabecalho)

                # Envia o conteúdo do arquivo solicitado ao cliente
                self.conn_socket.sendall("{}{}\r\n\r\n".format(cabecalho, outputdata).encode())
            except Exception as e:
                print(e)
                # Envia uma mensagem de resposta “File not Found”
                self.conn_socket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
                # Fecha o socket cliente
                self.conn_socket.close()

id = 0

while True:
    con, addr = server_socket.accept()
    sock_thread = ThreadWebServer(id, con, addr, lock)
    sock_thread.start()
    threads.append(sock_thread)

for thread in threads:
    thread.join()




server_socket.close()
sys.exit()#Termina o programa depois de enviar os dados