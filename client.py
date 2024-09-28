
import socket

def get_chunk_from_peer(peer_ip, peer_port, chunk_index):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)  # Set timeout for socket connection
        client.connect((peer_ip, peer_port))
        client.sendall(f"GET_CHUNK {chunk_index}".encode('utf-8'))
        
        chunk = client.recv(512)  # Receive chunk of size 512 bytes
        client.close()
        return chunk if chunk else None
    except socket.timeout:
        print(f"Connection to {peer_ip}:{peer_port} timed out.")
    except Exception as e:
        print(f"Error fetching chunk from {peer_ip}:{peer_port}: {e}")
    return None
