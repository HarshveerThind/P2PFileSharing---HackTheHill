
import time
import threading
from file_utils import chunk_file, rebuild_file
from server import start_server
from client import get_chunk_from_peer

def request_missing_chunks(available_chunks, peer_chunk_map, total_chunks):
    downloaded_chunks = [None] * total_chunks
    for chunk_index in range(total_chunks):
        if chunk_index not in available_chunks:
            for peer, peer_chunks in peer_chunk_map.items():
                if chunk_index in peer_chunks:
                    peer_ip, peer_port = peer.split(":")
                    chunk = get_chunk_from_peer(peer_ip, int(peer_port), chunk_index)
                    if chunk:
                        downloaded_chunks[chunk_index] = chunk
                        print(f"Downloaded chunk {chunk_index} from {peer}")
                        break
                    else:
                        print(f"Failed to download chunk {chunk_index} from {peer}")
        else:
            downloaded_chunks[chunk_index] = available_chunks[chunk_index]
    return downloaded_chunks

def main():
    file_chunks = chunk_file('file_to_share.txt')
    
    # Debugging: Print how many chunks were created
    print(f"Total chunks created: {len(file_chunks)}")

    # Only use the available chunks (as much as we have)
    available_chunks = {i: file_chunks[i] for i in range(9, 12) if i < len(file_chunks)}  # Ensure we don't exceed the chunk list

    # Print the chunks that Node 4 has
    print(f"Node 4 has chunks: {list(available_chunks.keys())}")

    # Adjust peer_chunk_map accordingly, if fewer chunks are present
    peer_chunk_map = {
        '127.0.0.1:8000': [i for i in range(0, 3) if i < len(file_chunks)],
        '127.0.0.1:8001': [i for i in range(3, 6) if i < len(file_chunks)],
        '127.0.0.1:8002': [i for i in range(6, 9) if i < len(file_chunks)],
    }

    total_chunks = len(file_chunks)
    downloaded_chunks = request_missing_chunks(available_chunks, peer_chunk_map, total_chunks)
    
    if None not in downloaded_chunks:
        # Show how the file is reconstructed by printing out the chunks
        print(f"Node 4 is reconstructing the file with chunks: {list(range(len(downloaded_chunks)))}")
        rebuild_file(downloaded_chunks, 'reconstructed_file_node4.txt')
        print("File successfully reconstructed by Node 4.")
    else:
        print("Failed to download all chunks.")

if __name__ == '__main__':
    threading.Thread(target=start_server, args=(8003, chunk_file('file_to_share.txt'))).start()
    time.sleep(2)
    main()
