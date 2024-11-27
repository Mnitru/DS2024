import socket
import os

def send_file(file_path, host='127.0.0.1', port=5432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    client_socket.send(file_name.encode())
    client_socket.send(str(file_size).encode())
    print(f"Sending file: {file_name}, Size: {file_size} bytes")

    with open(file_path, 'rb') as file:
        while chunk := file.read(4096):
            client_socket.send(chunk)
            print(f"Sent {len(chunk)} bytes")
    
    client_socket.close()
    print("File transfer complete, client closed.")

if __name__ == "__main__":
    file_path = r"C:\Users\trung\OneDrive\Desktop\B3\time series\file.txt"
    send_file(file_path, port = 5432)

