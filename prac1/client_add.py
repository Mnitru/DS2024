import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
print("Result:", proxy.add(5, 3))  # Calls the server function 'add'
