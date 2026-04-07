# Gerador de Scanner + Parser (Racket)
**Autores:** Bruno Porto Monteiro, Felipe Vieira Gualda Pereira, Gustavo Henrique Fontes Pereira

## **O que temos?**
- *scanner_gen/estado.py:* \
Estado - estrutura de dados responsável por armazenar um estado de um AFN. \
AFN: estrutura de dados que armazena o estado inicial e final de um AFN.

- *scanner_gen/gerador_afn.py:* \
Definidas as funções que representam operações básicas do teorema de Kleene, para transformar expressões regulares em AFNs.

- *scanner_gen/leitor_regex.py:* \
Definidas as funções para ler uma expressão regular e transformá-la em um AFN a partir dos algoritmos de Shunting Yard, para representar a regex na Notação Polonesa Reversa, e Construtor de Thompson, para gerar o autômato finito não-determinístico através da RPN.


## **TODO**:
### Gerador de Scanner:
- Desempacotador de atalhos (exemplo [0-9] para 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 )
- Algoritmo de subconjuntos (AFN -> AFD)
- Programa final
### Parser:
- Ainda não iniciado.