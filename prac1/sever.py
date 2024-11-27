import socket
import os

def start_server(host='127.0.0.1', port=5432):
    # Đường dẫn nơi server sẽ lưu file nhận được
    save_directory = r"C:\Users\trung\OneDrive\Desktop\B3\distributed system\DS2024\prac1"
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(save_directory, exist_ok=True)

    print("Initializing server...")  # Thêm log khởi tạo

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")
    except Exception as e:
        print(f"Error binding server: {e}")
        return

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    with conn:
        file_name = conn.recv(1024).decode()
        file_size = int(conn.recv(1024).decode())
        print(f"Receiving file: {file_name}, Size: {file_size} bytes")

        # Tạo đường dẫn đầy đủ để lưu file
        file_path = os.path.join(save_directory, file_name)

        with open(file_path, 'wb') as file:
            received = 0
            while received < file_size:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
                received += len(data)
                print(f"Received {received}/{file_size} bytes")
    
    server_socket.close()
    print(f"File transfer complete, saved to: {file_path}")
    print("Server closed.")

if __name__ == "__main__":
    start_server()

