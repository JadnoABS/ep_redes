import socket
  

msgFromClient = ""
mensagem = ""
ordem = 0
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 20
headerSize = 12

# Cria um socket UDP no lado do cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(10)

while True:
    try:
        msgFromClient = input("Escreva mensagem: ")
        message_size = len(msgFromClient)
        wait_for = message_size + ordem
        # Servidor faz a fragmentação e envia as mensagens
        for i in range(0, (message_size // bufferSize) + 1):
            last_index = bufferSize * (i + 1) if bufferSize * (i + 1) < message_size else message_size 
            ordem = last_index
            fragmento = msgFromClient[bufferSize * i : last_index]
            mensagem = str(ordem).zfill(6) + str(wait_for).zfill(6) + fragmento
            Bytes_msg = bytes(mensagem, 'utf-8')
            UDPClientSocket.sendto(Bytes_msg, serverAddressPort)

        # Servidor espera os acks
        while True:
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            
            msg = format(msgFromServer[0])
            msg = msg.replace("b'","")
            ack = int(msg.replace("'",""))
            print("Ack recebido: ", ack)
            if ack == message_size:
                break

        
    except socket.error:
        print("TimeOut Erro! Mande a mensagem novamente")