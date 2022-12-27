import socket
from threading import Thread, Timer

def reconstruct_message(buffer: list[dict], ack: int):
    for message in buffer:
        if (len(message["value"]) - 1 + ack == message["ack"]):
            return message["ack"]

    return ack

class Client:
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    max_buffer_size = 256
    current_buffer_size = 0
    buffer = []
    MSS = 20
    headerSize = 12
    ip = "127.0.0.1"
    last_ack = None

    def check_if_timer(self, ack, value):
        for index, message in enumerate(self.buffer):
            if message["ack"] == ack and message["value"] == value:
                self.buffer.pop(index)

    def received_ack_wrong_order(self, ack, message, address):
        print("Salvando no buffer")
        # Adicionar no buffer
        self.current_buffer_size += len(message)
        if self.current_buffer_size > self.max_buffer_size:
            self.UDPServerSocket.sendto(str.encode(str(-1)), address)
            pass
        else:
            self.buffer.append({
                "value": message,
                "ack": ack
            })
            Timer(3, lambda _: self.check_if_timer(ack, message))

    def check_if_concatenation_of_messages_are_possible(self, ack, address):
        print("Checando se concatenar é possivel")
        new_ack = ack
        while True:
            new_ack = reconstruct_message(self.buffer, ack)
            if ack != new_ack:
                ack = new_ack
                for index, message in enumerate(self.buffer):
                    if message["ack"] == ack:
                        self.buffer.pop(index)
            else:
                self.last_ack = ack
                print("Enviando msg com ack {}".format(ack))
                self.UDPServerSocket.sendto(str.encode(str(ack)), address)
                break

    def new_connection(self, port):
        self.UDPServerSocket.bind((self.ip, port))
        print("UDP server up and listening")
        self.last_ack = 0
        self.listen_to()

    def listen_thread(self, message, address):
        message.decode("utf-8")
        clientMsg = format(message)

        confere = clientMsg.replace("b'","")
        ack = int(confere[:6])
        final = int(confere[6:12])
        message = confere[12:]
        print(
            message[:-1],
            "with ack:{} expected until :{}".format(ack, final)
        )
        # Fora de ordem
        if ack > self.last_ack + self.MSS:
            self.received_ack_wrong_order(ack, message, address)
        # Ja recebeu pode descartar
        elif self.last_ack >= ack:
            print("Errou")
            pass
        # Dentro de ordem
        else:
            print("Enviando resposta")
            if (self.current_buffer_size != 0):
                self.check_if_concatenation_of_messages_are_possible(ack, address)
            else:
                self.last_ack = ack
                self.UDPServerSocket.sendto(str.encode(str(ack)), address)
 


    def listen_to(self):
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.headerSize + self.MSS)
            # Thread para ouvir por mensagens
            t = Thread(target = self.listen_thread, args = (bytesAddressPair))
            t.start()
            t.join()





if __name__ == "__main__":
    client = Client()
    client.new_connection(20001)
