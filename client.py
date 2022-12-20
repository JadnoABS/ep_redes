import socket
import time
from threading import Thread

def reconstruct_message(buffer: list[dict], ack: int):
    for message in buffer:
        if (len(message["value"] + ack == message["ack"])):
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

        # Fora de ordem
        if ack > self.last_ack + self.MSS:
            print(message, "Received: {} Last_ack: {}, saving in buffer".format(ack, self.last_ack))
            # Adicionar no buffer
            self.current_buffer_size += len(message)
            if self.current_buffer_size > self.max_buffer_size:
                # Enviar mensagem de erro ao servidor
                pass
            else:
                self.buffer += {
                    "value": message,
                    "ack": ack
                }
        # Ja recebeu pode descartar
        elif self.last_ack >= ack:
            pass
        # Dentro de ordem
        else:
            if (self.current_buffer_size != 0):
                new_ack = ack
                stop = False
                while stop:
                    new_ack = reconstruct_message(self.buffer, self.ack)
                    if ack != new_ack:
                        ack = new_ack
                        for index, message in enumerate(self.buffer):
                            if message["ack"] == ack:
                                self.buffer.pop(index)
                    else:
                        self.last_ack = ack
                        self.UDPServerSocket.sendto(str.encode(str(ack)), address)
                        print(
                            message[:-1],
                            "with ack:{} expected until :{}".format(ack, final)
                        )
                        stop = True
            else:
                self.last_ack = ack
                self.UDPServerSocket.sendto(str.encode(str(ack)), address)
                print(
                    message[:-1],
                    "with ack:{} expected until :{}".format(ack, final)
                )


    def listen_to(self):
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.headerSize + self.MSS)
            t = Thread(target = self.listen_thread, args = (bytesAddressPair))
            t.start()
            t.join()



if __name__ == "__main__":
    client = Client()
    client.new_connection(20001)
