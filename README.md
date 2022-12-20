# Criação e implementação de um protocolo de comunicação para uma rede UDP

## Objetivo
Implementar transmissão de dados confiáveis com controle de fluxo e congestionamento sobre o UDP. A ideia é criar protocolos de comunicação 
via código que garantem a confiabildiade da comunicação, além do recebimento em ordem, considerando diversos fatores como problemas no meio de 
transmissão.

## Relatório
* descrição do protocolo implementado
* possíveis cenários para análise empíricas:
  1. simular perda de pacote
  2. simular atrasos de propagação
  3. simular um roteador com fila e diferentes tamanhos
  4. simular diferentes taxas de transmissão
  5. simular compartilhamento de banda
  6. simular buffer de recepção e lentidão para leitura

## Possíveis mensuração
1. tamanho da janela de congestionamento
2. fila no roteador
3. taxa média de transmissão útil

## Explicaçao do código
Para execurtar o programa foi necessário estabelecer uma relação entre cliente e servidor, das quais são descritas a seguir. Nessa comunicação, o intuito é fazer com que o cliente receba os dados do servidor, sem resposta, apenas mandando um ack ou algum outro tipo de confirmação.

### Cliente
Primeiro importamos a biblioteca socket que nos ajudará com a conexão, instânciamos algumas variáveis de controle como IP local e Porta(valor arbitrário). Destacamos tamém o tamanho do buffer em `bufferSize`, isto é, o tamanho máximo de bytes aceitos, que podem chegar. Por fim, temos o `headerSize` que representa o tamnho do cabeçalho das mensagens transmitidas. 
```Py
import socket

msgFromClient = ""
mensagem = ""
ordem = 0
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 20
headerSize = 12
```

A bibliteca `socket` nos permite usar o método `socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)`  para criar uma conexão do tipo UDP, caso quisessemos uma conexão mais segura do tipo TCP teriams que usar `socket(family=socket.AF_INET, type=socket.SOCK_STREAM)` 
```Py
# Cria um socket UDP no lado do cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(10)
```

### Servidor
No lado do servidor temos uma biblioteca a mais, o `time` nos ajudará para fazermos teste quando quisermos mensurar um atraso de propragação, aumentando assim o tempo de resposta. Instânciamos aqui também o IP e a porta local, que **deve ser igual à porta do ** `cliente.py`. Por fim, temos o `bufferSize` que ditará o tamanho das mensagens que podemos receber do cliente, nesse caso não será tão importante porque nossa aplicação explora mais o fluxo de mensagens do cliente para o servidor.
```Py
import socket
import time

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 32
```

Aqui vinculamos o servidor ao endeço IP, e esperamos algum cliente conectar no barramento. Assim que ele conecta em `UDPServerSocket.bind((localIP, localPort))` é printado uma mensagem que diz que estamos esperando uma mensagem.
```Py
# Criando o socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
# Vincular ao endereço e IP
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
```

## TODO

- [ ] Cliente
  - [ ] Se receber ack não esperado salvar buffer
  - [ ] Se buffer não estiver vazio, checar se é possível fazer o demultiplexação
    - [ ] Adicionar buffer de mensagens e seus acks
  - [ ] Iniciar conexão com servidor
  - [ ] Adicionar velocidade de processamento
- [ ] Server
  - [ ] Adicionar velocidade de banda
  - [ ] Se receber ack não esperado, reenviar mensage
  - [ ] Fazer envio e leitura de ack através de threads 1 para envio e 1 para leitura
  - [ ] Esperar conexão do client
    - [ ] Fazer leitura da port do client e iniciar conexão
- [x] Bugs
  - [x] Enviar mensagem com tamanho maior que 20 buga o servidor
    - [x] O servidor envia as mensagens corretamente
    - [x] O cliente recebe corretamente
    - [x] No entanto, a leitura pelo servidor não ocorre de maneira correta bugando todas as próximas leituras