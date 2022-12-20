import socket
import time


class Client:
    PROCCESS_TIME = 0.1
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    bufferSize = 20
    headerSize = 12
    ip = "127.0.0.1"

    def new_connection(self, port):
        self.UDPServerSocket.bind((self.ip, port))
        print("UDP server up and listening")
        self.listen_to()
    
    def listen_to(self):
        last_ack = 0
        # Esperando por datagramas
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.headerSize + self.bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            message.decode("utf-8")
            clientMsg = format(message)

            confere = clientMsg.replace("b'","")
            ack = int(confere[:6])
            final = int(confere[6:12])
            message = confere[12:]

            if ack > last_ack + self.bufferSize:
                print(message, "Received: {} Last_ack: {}, saving in buffer".format(ack, last_ack))
                pass
            else:
                last_ack = ack
                self.UDPServerSocket.sendto(str.encode(str(ack)), address)
                print(
                    message[:-1],
                    "with ack:{} expected until :{}".format(ack, final)
                )
                pass

client = Client()
client.new_connection(20001)