import socket
import time

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 32

msgFromServer       = "Ola Manuel Gomii"
bytesToSend         = str.encode(msgFromServer)

# Criando o socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
# Vincular ao endereço e IP
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

espera = 0

# Esperando por datagramas
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    message.decode("utf-8")
    clientMsg = format(message)

    #verificações
    confere = clientMsg.replace("b'","")
    ack = int(confere[:6])
    tamanhoTotal = int(confere[6:12])
    message = confere[12:]

    if ack == tamanhoTotal:
        espera = ack
        UDPServerSocket.sendto(str.encode(str(espera)), address)
    else:
        if ack >= espera + bufferSize:
            # Adicionar ao buffer
            pass
        else:
            # Buffer está vazio? Se não checar se da pra juntar os pacotes
            espera = ack
            UDPServerSocket.sendto(str.encode(str(espera)), address)
            pass
