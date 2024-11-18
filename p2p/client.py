import socket
import threading

server_ip = '127.0.0.1'  # Endereço do servidor central
server_port = 1234  # Porta do servidor

# Função para escutar por mensagens recebidas do servidor
def listen_for_messages():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))  # Conecta-se ao servidor central

    while True:
        message = client_socket.recv(1024)  # Recebe mensagem do servidor
        print(f"> {message.decode()}")

# Função para enviar mensagens para o servidor
def send_message():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))  # Conecta-se ao servidor central

    while True:
        message = input("Digite a mensagem para enviar: ")
        client_socket.send(message.encode())  # Envia mensagem para o servidor

# Inicia as threads para enviar e receber mensagens simultaneamente
listen_thread = threading.Thread(target=listen_for_messages)
listen_thread.daemon = True
listen_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.daemon = True
send_thread.start()

# Manter o cliente rodando
while True:
    pass
