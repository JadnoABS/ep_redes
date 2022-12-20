import socket


class Server:
    MSS = 20
    headerSize = 12
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    currentSize = 0
    client_port = None
    ack = 0

    def new_connection(self, client_port):
        self.client_port = client_port
        self.UDPClientSocket.settimeout(3)
        print("Servidor ouvindo na porta ", client_port)
        self.start_messaging()

    def fragment_envia(self, message, start):
        message_size = len(message)
        self.currentSize += message_size
        for i in range(start, (message_size // self.MSS) + 1):
            last_index = self.MSS * (i + 1) if self.MSS * (i + 1) < message_size else message_size 
            ordem = last_index
            fragmento = message[self.MSS * i : last_index]
            mensagem = str(self.currentSize - message_size + ordem).zfill(6) + str(self.currentSize).zfill(6) + fragmento
            Bytes_msg = bytes(mensagem, 'utf-8')
            self.UDPClientSocket.sendto(Bytes_msg, self.serverAddressPort())


    def espera_ack(self):
        while self.ack != self.currentSize:
            msgFromServer = self.UDPClientSocket.recvfrom(self.MSS + self.headerSize)
            
            msg = format(msgFromServer[0])
            msg = msg.replace("b'","")
            self.ack = int(msg.replace("'",""))
            print("Ack recebido: ", self.ack)

    def start_messaging(self):
        while True:
            try:
                msgFromClient = input("Escreva mensagem: ")
                self.fragment_envia(msgFromClient, 0)               
                self.espera_ack()
                
            except socket.error:
                print("TimeOut Erro! Mande a mensagem novamente")

    def serverAddressPort(self):
        return ("127.0.0.1", self.client_port)


if __name__ == "__main__":
    server = Server()
    server.new_connection(20001)