from socket import *
import sys

try:
    HOST = sys.argv[1]
    PORTA = int(sys.argv[2])
    ARQUIVO = sys.argv[3]
except Exception:
    print("[+] ENTRADA MAL FORMATADA!!!")
    sys.exit(1)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORTA))
(cliente_host, cliente_porta) = client_socket.getsockname()

for i in range(10):
    cabecalho_http_requisicao = 'GET /{} HTTP/1.1\r\nHost: {}:{}\r\nUser-Agent: Client_Python/0.2\r\n\r\n'.format(
        ARQUIVO,
        cliente_host,
        cliente_porta
    )

    client_socket.send(cabecalho_http_requisicao.encode())

    cabecalho = client_socket.recv(1024).decode()
    arquivo_recebido = ""

    print(cabecalho)
    while True:
        try:
            tmp = client_socket.recv(1024).decode()
            if not tmp:
                break
            arquivo_recebido = arquivo_recebido + tmp
        except Exception as e:
            print(e)
    print(arquivo_recebido)
client_socket.close()
