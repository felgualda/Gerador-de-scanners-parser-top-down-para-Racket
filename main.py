from scanner_gen.filemanager import Filemanager
from scanner_gen.scan import Scan
from scanner_gen.gerador_afn import LeitorRegex
from scanner_gen.gerador_afd import Subset_construction
import scanner_gen.gerador_scanner
from parser.parser_top_down import Parser

def print_tree(node, prefix="", is_last=True):
    # Define os caracteres de conexão
    connector = "└── " if is_last else "├── "
    
    if isinstance(node, list):
        # Printa o início da lista
        print(prefix + connector + "[")
        
        # Novo prefixo para os filhos
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, child in enumerate(node):
            last_child = (i == len(node) - 1)
            print_tree(child, new_prefix, last_child)
            
        print(prefix + ("    " if is_last else "│   ") + "]")
    else:
        # Printa o token (átomo)
        print(prefix + connector + str(node))

regexs = Filemanager.carregar("scanner_gen/teste.txt")
master = LeitorRegex.get_afn_master(regexs)
afd = Subset_construction.afn_to_afd(master)

scanner_gen.gerador_scanner.gerar_scanner(afd)
lista_tokens = Scan.ler("examples/success_5.txt", afd)

print(f"N de estados: {len(afd.estados)}")
print("\nTokens identificados:")
print(lista_tokens)
print()

print("=== INICIANDO ANÁLISE SINTÁTICA ===")
parser = Parser(lista_tokens)
resultado = parser.parse()

if not parser.errors:
    print("Programa aceito com sucesso!")
    print("Estrutura da Árvore Sintática:")
    for i, expr in enumerate(resultado):
        print(f"\nExpressão #{i + 1}:")
        print_tree(expr)
else:
    print("\n--- FALHA NA ACEITAÇÃO (Lista de Erros) ---")
    for i, erro in enumerate(parser.errors, 1):
        print(f"{i}. {erro}")