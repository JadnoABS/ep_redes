# Criação e implementação de um protocolo de comunicação para uma rede UDP

## Objetivo: 
Implementar transmissão de dados confiáveis com controle de fluxo e congestionamento sobre o UDP. A ideia é criar protocolos de comunicação 
via código que garantem a confiabildiade da comunicação, além do recebimento em ordem, considerando diversos fatores como problemas no meio de 
transmissão.

## Relatório:
* descrição do protocolo implementado
* possíveis cenários para análise empíricas:
  1. simular perda de pacote
  2. simular atrasos de propagação
  3. simular um roteador com fila e diferentes tamanhos
  4. simular diferentes taxas de transmissão
  5. simular compartilhamento de banda
  6. simular buffer de recepção e lentidão para leitura

## Possíveis mensuração:
1. tamanho da janela de congestionamento
2. fila no roteador
3. taxa média de transmissão útil

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
- [ ] Bugs
  - [ ] Enviar mensagem com tamanho maior que 20 buga o servidor
    - [ ] O servidor envia as mensagens corretamente
    - [ ] O cliente recebe corretamente
    - [ ] No entanto, a leitura pelo servidor não ocorre de maneira correta bugando todas as próximas leituras
