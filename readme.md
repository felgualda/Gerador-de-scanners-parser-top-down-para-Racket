# Gerador de Scanner + Parser (Racket)
**Autores:** Bruno Porto Monteiro, Felipe Vieira Gualda Pereira, Gustavo Henrique Fontes Pereira

## **O que temos?**
- *scanner_gen/estado.py:* \
Estado - estrutura de dados responsável por armazenar um estado de um AFN. \
AFN: estrutura de dados que armazena o estado inicial e final de um AFN.

- *scanner_gen/gerador_afn.py:* \
Definidas as funções que representam operações básicas do teorema de Kleene, para transformar expressões regulares em AFNs.


## **TODO**:
### Gerador de Scanner:
- Desempacotador de atalhos (exemplo [0-9] para 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 )
- Leitor de regex (mini-parser pras expressões) para empilhar as expressões na ordem certa e chamar funções do gerador.
- Algoritmo de subconjuntos (AFN -> AFD)
- Programa final
### Parser:
- Ainda não iniciado.