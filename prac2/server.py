import grpc
from concurrent import futures
import file_transfer_pb2_grpc
import file_transfer_pb2

class FileTransferService(file_transfer_pb2_grpc.FileTransferServiceServicer):
    def UploadFile(self, request_iterator, context):
        for chunk in request_iterator:
            with open(chunk.filename, "ab") as f:
                f.write(chunk.content)
        return file_transfer_pb2.UploadStatus(message="File uploaded successfully", success=True)

    def DownloadFile(self, request, context):
        try:
            with open(request.filename, "rb") as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    yield file_transfer_pb2.FileChunk(content=chunk, filename=request.filename)
        except FileNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"File '{request.filename}' not found.")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
file_transfer_pb2_grpc.add_FileTransferServiceServicer_to_server(FileTransferService(), server)
server.add_insecure_port("[::]:50051")
print("Server started on port 50051")
server.start()
server.wait_for_termination()