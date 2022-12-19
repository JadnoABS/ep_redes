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
3. taxa m´edia de transmiss˜ao ´util
