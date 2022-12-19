import socket

class Client:
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    bufferSize = 20
    headerSize = 12
    ip = "127.0.0.1"

    def new_connection(self, port):
        self.UDPServerSocket.bind((self.ip, port))
        print("UDP server up and listening")
        self.listen_to()
    
    def listen_to(self):
        espera = 0
        # Esperando por datagramas
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.headerSize + self.bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            message.decode("utf-8")
            clientMsg = format(message)

            #verificações
            confere = clientMsg.replace("b'","")
            ack = int(confere[:6])
            final = int(confere[6:12])
            message = confere[12:]

            print(
                message,
                "with {} expected until {}\n".format(ack, final)
            )

            if ack >= espera + self.bufferSize:
                pass
            else:
                espera = ack
                self.UDPServerSocket.sendto(str.encode(str(ack)), address)
                pass

client = Client()
client.new_connection(20001)