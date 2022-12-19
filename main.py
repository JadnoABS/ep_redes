import socket

def server(host = 'localhost', port=8082):
    data_payload = 2048
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    print ("Starting up echo server  on %s port %s" % server_address)
    sock.bind(server_address)
    i = 0
    while True: 
        print ("Waiting to receive message from client")
        data, address = sock.recvfrom(data_payload) 
        if data:
            data = data.decode('utf-8')
            print(data);
server()
