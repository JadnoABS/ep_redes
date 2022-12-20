import socket
import time


class Client:
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    MSS = 20
    headerSize = 12
    ip = "127.0.0.1"

    def new_connection(self, port):
        self.UDPServerSocket.bind((self.ip, port))
        print("UDP server up and listening")
        self.listen_to()
    
    def listen_to(self):
        last_ack = 0
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.headerSize + self.MSS)
            # A partir daqui fazer tudo em thread para client estar sempre ouvindo mensagens
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            message.decode("utf-8")
            clientMsg = format(message)

            confere = clientMsg.replace("b'","")
            ack = int(confere[:6])
            final = int(confere[6:12])
            message = confere[12:]

            # Fora de ordem
            if ack > last_ack + self.MSS:
                print(message, "Received: {} Last_ack: {}, saving in buffer".format(ack, last_ack))
                # Adicionar no buffer
                pass
            # Ja recebeu pode descartar
            elif last_ack >= ack:
                pass
            # Dentro de ordem
            else:
                # Checar se buffer está vazio ou não 
                last_ack = ack
                self.UDPServerSocket.sendto(str.encode(str(ack)), address)
                print(
                    message[:-1],
                    "with ack:{} expected until :{}".format(ack, final)
                )
                pass

if __name__ == "__main__":
    client = Client()
    client.new_connection(20001)