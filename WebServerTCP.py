#import socket module
from socket import *
import sys # para terminar o programa
server_socket = socket(AF_INET, SOCK_STREAM)
#Prepara o socket servidor
server_socket.bind(('', 9999))
server_socket.listen(5)

while True:
    #Estabelece a conexão
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()
    try:
        message = connection_socket.recv(1024).decode()
        print(message)
        #separando por espaço a requisição recebida
        arquivo_requisitado = message.split(' ')[1]
        if arquivo_requisitado == '/':
            arquivo_requisitado = arquivo_requisitado + 'index.html'
        #1º caractere desse split eh /, removendo com a sublista [1:]
        arquivo = open(arquivo_requisitado[1:])
        outputdata = arquivo.read()
        #Envia um linha de cabeçalho HTTP para o socket
        cabecalho = 'HTTP/1.1 200 OK\r\n\r\n'
        #Envia o conteúdo do arquivo solicitado ao cliente
        #for i in range(0, len(outputdata)):
        #    connection_socket.send(outputdata[i].encode())
        #connection_socket.send('\r\n\r\n'.encode())
        connection_socket.sendall("{}{}\r\n\r\n".format(cabecalho, outputdata).encode())
        connection_socket.close()
    except IOError:
        #Envia uma mensagem de resposta “File not Found”
        connection_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n'
                                    b'<html>\r\n<head>\r\n<title>Servidor Web Python</title>\r\n</head>\r\n'
                                    b'<body>\r\n<h1>File not Found</h1>\r\n</body>\r\n</html>\r\n')
        #Fecha o socket cliente
        connection_socket.close()
server_socket.close()
sys.exit()#Termina o programa depois de enviar os dados
