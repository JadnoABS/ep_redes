import socket
import time


class Server:
    bufferSize = 20
    headerSize = 12
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    currentSize = 0
    server_port = None
    ack = 0

    def new_connection(self, server_port):
        self.server_port = server_port
        self.UDPClientSocket.settimeout(3)
        self.start_messaging()

    def fragment_envia(self, message):
        message_size = len(message)
        self.currentSize += message_size
        for i in range(0, (message_size // self.bufferSize) + 1):
            last_index = self.bufferSize * (i + 1) if self.bufferSize * (i + 1) < message_size else message_size 
            ordem = last_index
            fragmento = message[self.bufferSize * i : last_index]
            mensagem = str(self.currentSize - message_size + ordem).zfill(6) + str(self.currentSize).zfill(6) + fragmento
            Bytes_msg = bytes(mensagem, 'utf-8')
            self.UDPClientSocket.sendto(Bytes_msg, self.serverAddressPort())


    def espera_ack(self):
        print("ESPERANDO ACK...", self.ack)
        while self.ack != self.currentSize:
            msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize + self.headerSize)
            
            msg = format(msgFromServer[0])
            msg = msg.replace("b'","")
            self.ack = int(msg.replace("'",""))
            print("Ack recebido: ", self.ack)

    def start_messaging(self):
        while True:
            try:
                msgFromClient = input("Escreva mensagem: ")
                self.fragment_envia(msgFromClient)               
                self.espera_ack()
                
            except socket.error:
                print("TimeOut Erro! Mande a mensagem novamente")

    def serverAddressPort(self):
        return ("127.0.0.1", self.server_port)


server = Server()
server.new_connection(20001)