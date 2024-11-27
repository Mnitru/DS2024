from xmlrpc.server import SimpleXMLRPCServer

def add(a, b):
    return a + b

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(add, "add")
print("Server running...")
server.serve_forever()
