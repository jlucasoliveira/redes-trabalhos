from socket import *
import sys

try:
    servidor_host = sys.argv[1]
    servidor_porta = int(sys.argv[2])
    arquivo_requisitado = sys.argv[3]
except Exception:
    print("[+] ENTRADA MAL FORMATADA!!!")
    sys.exit(1)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((servidor_host, servidor_porta))
(addr, porta) = client_socket.getsockname()

cabecalho_http_requisicao = 'GET /{} HTTP/1.1\r\nHost: {}:{}\r\nUser-Agent: Client_Python/0.1\r\n\r\n'.format(
    arquivo_requisitado,
    addr,
    porta
)

client_socket.send(cabecalho_http_requisicao.encode())

resul = client_socket.recv(1024)
print(resul.decode())

client_socket.close()
