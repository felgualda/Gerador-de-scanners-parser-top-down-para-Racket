from parser.parser_top_down import Parser
from scanner_gen.filemanager import Filemanager
from scanner_gen.gerador_afd import Subset_construction
from scanner_gen.gerador_afn import LeitorRegex

def analisar(caminho):
    try:
        import scanner
    except:
        print("É necessário gerar um scanner antes de realizar a análise.")
        return
    
    lista_tokens = []
    with open(caminho, 'r', encoding='utf-8') as f:
        codigo = f.read()
        lista_tokens = scanner.ler_codigo(codigo)
        lista_tokens = [t for t in lista_tokens if t[0] != 'COMMENT']
        for t in lista_tokens:
            print(t)
    
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
           print(f"\n{i}. {erro}")

def print_tree(node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "
    
    if isinstance(node, list):
        print(prefix + connector + "[")
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, child in enumerate(node):
            last_child = (i == len(node) - 1)
            print_tree(child, new_prefix, last_child)
            
        print(prefix + ("    " if is_last else "│   ") + "]")
    else:
        print(prefix + connector + str(node))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        analisar(sys.argv[1])
    else:
        print("Uso: python gerar_scanner.py <regex.txt>")