
import socket
import threading
from file_utils import chunk_file

def handle_client(client_socket, file_chunks):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if request.startswith("GET_CHUNK"):
            chunk_index = int(request.split()[1])
            if 0 <= chunk_index < len(file_chunks):
                client_socket.sendall(file_chunks[chunk_index])
            else:
                client_socket.sendall(b'')
    except Exception as e:
        print(f"Error handling client request: {e}")
    finally:
        client_socket.close()

def start_server(port, file_chunks):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Server listening on port {port}...")
    
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, file_chunks))
        client_handler.start()
