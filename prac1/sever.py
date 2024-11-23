import socket

def start_server(host='127.0.0.1', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    with conn:
        file_name = conn.recv(1024).decode()
        file_size = int(conn.recv(1024).decode())
        print(f"Receiving file: {file_name}, Size: {file_size} bytes")

        with open(file_name, 'wb') as file:
            received = 0
            while received < file_size:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
                received += len(data)
                print(f"Received {received}/{file_size} bytes")
    
    server_socket.close()
    print("File transfer complete, server closed.")

if __name__ == "__main__":
    start_server()
