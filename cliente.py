import socket
import threading  
  

msgFromClient = ""
ordem = 1
mensagem = ""
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 20

# Cria um socket UDP no lado do cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(10)

while True:
    try:
        # Escrevendo mensagem
        msgFromClient = input("Escreva mensagem: ")
        mensagem = str(ordem) + "/" + msgFromClient + "/" + str(len(msgFromClient))
        Bytes_msg = bytes(mensagem, 'utf-8')
        #print("Tamanho em bytes: ",len(Bytes_msg))

        #mensagem maior do que o buffer, index tem 4bytes
        if(len(Bytes_msg) > 16):
            for i in range(0, (len(mensagem) // bufferSize) +1):
                fragmento = mensagem[bufferSize * i, bufferSize * i + 1 if bufferSize * (i + 1) < message_size else message_size]
                # Mando algo pro servidor usando o socket UDP 
                UDPClientSocket.sendto(bytes(fragmento, 'utf-8'), serverAddressPort) 
                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        else:
            # Mando algo pro servidor usando o socket UDP 
            UDPClientSocket.sendto(Bytes_msg, serverAddressPort) 
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            
        # Tratando a resposta
        msg = format(msgFromServer[0])
        msg = msg.replace("b'","")
        msg = msg.replace("'","")
        print("Ack recebido: ", msg)
        # Conferindo se é a certa
        if(msg == str(ordem)):
            ordem = ordem+1
        else:
            print("Mensagem nao entregue, mande novamente")
        
    except socket.error:
        print("TimeOut Erro! Mande a mensagem novamente")