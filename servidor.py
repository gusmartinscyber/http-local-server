import socket
from datetime import datetime

HOST = "127.0.0.1"
PORTA = 8080

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORTA))
servidor.listen(1)

print(f"Servidor aguardando conexão em {HOST}:{PORTA}...")

conexao, endereco_cliente = servidor.accept()

print(f"\nCliente conectado: {endereco_cliente[0]}:{endereco_cliente[1]}")

requisicao = b""
while b"\r\n\r\n" not in requisicao:
    parte = conexao.recv(4096)
    if not parte:
        break
    requisicao += parte
texto_requisicao = requisicao.decode("utf-8", errors="replace")

print("\n--- REQUISIÇÃO RECEBIDA ---")
print(texto_requisicao)

corpo = "<h1>Resposta do servidor com sockets</h1>"
resposta = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    f"Content-Length: {len(corpo.encode('utf-8'))}\r\n"
    "Connection: close\r\n"
    "\r\n"
    f"{corpo}"
)

conexao.sendall(resposta.encode("utf-8"))

print("--- RESPOSTA ENVIADA ---")
print(resposta)

conexao.close()
servidor.close()

print(f"\nConexão encerrada em {datetime.now().isoformat(timespec='seconds')}.")
