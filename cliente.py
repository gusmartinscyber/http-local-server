import socket

HOST = "127.0.0.1"
PORTA = 8080

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))

print(f"Servidor: {HOST}")
print(f"Porta: {PORTA}")

requisicao = (
    "GET / HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "Connection: close\r\n"
    "\r\n"
)

dados_enviados = requisicao.encode("utf-8")
cliente.sendall(dados_enviados)

print(f"Bytes enviados: {len(dados_enviados)}")

resposta_completa = b""

while True:
    parte = cliente.recv(4096)
    if not parte:
        break
    resposta_completa += parte

cliente.close()

print(f"Bytes recebidos: {len(resposta_completa)}")
print("\n--- RESPOSTA RECEBIDA ---")
print(resposta_completa.decode("utf-8", errors="replace"))
