# Gerador de Scanner + Parser (Racket)
**Autores:** Bruno Porto Monteiro, Felipe Vieira Gualda Pereira, Gustavo Henrique Fontes Pereira

## **Como executar?**
Gerador de scanner: ```py gerar_scanner.py <caminho_lista_regex>``` \
Analisador sintático (parser): ```py analisar_sintaxe.py <caminho_codigo_racket>```
Makefile (roda Gerador de scanner e Analisador sintático para todos os testes em "examples/parser"): ```make test```

## **O que temos?**
### ▪ scanner_gen/EDs/estado_afd.py:
Definição das classes *EstadoAFD* e *AFD*, que são as estruturas de dados utilizadas para representar autômatos finitos determinísticos.

### ▪ scanner_gen/gerador_afn.py:
Definição das classes *EstadoAFN* e *AFN*, que são as estruturas de dados utilizadas para representar autômatos finitos não-determinísticos.

### ▪ scanner_gen/filemanager.py:
Definição da classe *Filemanager*, com a função única *carregar()* responsável por ler as regras no arquivo de entrada e retornar a tupla *(Token, Regex)*.

### ▪ scanner_gen/funcoes_afn.py:
Definição da classe *ConstrutorAFN*, com as funções que retornam AFNs característicos das operações básicas em expressões regulares.

### ▪ scanner_gen/gerador_afd.py:
Definição da classe *Subset_construction*, que contém as funções necessárias para executar o algoritmo de Construção de Subconjuntos, que converte um AFN para um AFD.

### ▪ scanner_gen/gerador_afn.py:
Definição da classe *LeitorRegex*, que trata as expressões regulares recebidas para estarem na forma pós-fixa e serem devidamente estruturadas para a construção do AFN a partir da Construção de Thompson.

### ▪ scanner_gen/scan.py:
Definição da classe *Scan*, que contém a função única *ler()*, que recebe um arquivo de texto e um AFD e verifica se a cadeia é aceita. Além disso, para cada token identificado, a função põe a tupla (Token, cadeia) na lista retornada.

### ▪ parser/parser_top_down.py:
Definição da classe *Parser*, um analisador sintático preditivo Top-Down (Descida Recursiva). Contém a lógica para processar gramáticas complexas do Racket, como `define`, `if`, `let`, `cond`, `lambda` e recursividade de expressões.

### ▪ analisar_sintaxe.py:
Script principal de interface do Parser. Realiza a ponte entre o Scanner e o Parser, aplicando filtros de limpeza (remoção de comentários e espaços) e exibindo a Árvore Sintática Abstrata (AST) formatada para o usuário.