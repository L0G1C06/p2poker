import socket
import threading

max_connections = 8   # Número máximo de conexões simultâneas permitidas
clients = []  # Lista para armazenar os peers conectados

# Função para lidar com a comunicação com cada cliente (peer)
def handle_client(client_socket, client_address):
    print(f"Novo peer conectado: {client_address}")
    while True:
        try:
            message = client_socket.recv(10245)  # Recebe mensagem do peer
            if message:
                print(f"Mensagem recebida de {client_address}: {message.decode()}")
                broadcast_message(message, client_socket)  # Envia para todos os outros peers
            else:
                break
        except:
            break

    # Remover cliente da lista e fechar conexão
    clients.remove(client_socket)
    client_socket.close()
    print(f"Peer {client_address} desconectado.")

# Função para enviar mensagem para todos os outros peers conectados
def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)  # Envia para todos os peers exceto o remetente
            except:
                pass

# Função para escutar por novos peers
def listen_for_peers():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Escuta na porta 12345
    server_socket.listen(10)  # Permite até 5 conexões pendentes na fila
    print("Servidor centralizado escutando na porta 1234...")

    while True:
        # Verifica se o número de conexões ativas está abaixo do limite
        if len(clients) < max_connections:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)  # Adiciona o peer à lista de clientes
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
        else:
            print(f"Limite de {max_connections} conexões atingido. Rejeitando nova conexão.")
            # Caso o limite de conexões seja atingido, o servidor fecha a conexão com o novo cliente
            new_client_socket, _ = server_socket.accept()
            new_client_socket.close()

# Inicia a escuta por novos peers em uma thread
listen_thread = threading.Thread(target=listen_for_peers)
listen_thread.daemon = True
listen_thread.start()

# Manter o servidor rodando
while True:
    pass