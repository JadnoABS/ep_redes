import socket
import time

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 20

msgFromServer       = "Ola Manuel Gomii"
bytesToSend         = str.encode(msgFromServer)
espera = 1
 

# Criando o socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
# Vincular ao endereço e IP
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")


# Esperando por datagramas
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    message.decode("utf-8")
    clientMsg = format(message)

    #verificações
    confere = clientMsg.replace("b'","")
    confere = confere.replace("'","")
    confere = confere.split('/')
    

    if confere[0] == str(espera):
        if confere[2] == str(len(confere[1])):
            print("Mensagem cliente: ", confere)
             #simula timeout
            # Respondendo cliente se o tamanho da mensagem e a ordem é certa
            UDPServerSocket.sendto(str.encode(str(espera)), address)
            espera = espera+1
        else:
            UDPServerSocket.sendto(str.encode(str(espera)), address)
    else:
        UDPServerSocket.sendto(str.encode(str(espera)), address)
