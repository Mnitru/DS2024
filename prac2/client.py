import grpc
import file_transfer_pb2_grpc
import file_transfer_pb2

def upload_file(stub, filename):
    def generate_chunks():
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                yield file_transfer_pb2.FileChunk(content=chunk, filename=filename)
    response = stub.UploadFile(generate_chunks())
    print(response.message)

def download_file(stub, filename):
    response = stub.DownloadFile(file_transfer_pb2.FileRequest(filename=filename))
    with open(f"downloaded_{filename}", "wb") as f:
        for chunk in response:
            f.write(chunk.content)

if __name__ == "__main__":
    channel = grpc.insecure_channel("localhost:50051")
    stub = file_transfer_pb2_grpc.FileTransferServiceStub(channel)

    # Example usage
    print("Uploading file...")
    upload_file(stub, "example.txt")
    print("Downloading file...")
    download_file(stub, "example.txt")