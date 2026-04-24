from scanner_gen.filemanager import Filemanager
from scanner_gen.gerador_afd import Subset_construction
from scanner_gen.gerador_afn import LeitorRegex


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        regexs = Filemanager.carregar(sys.argv[1])
        master = LeitorRegex.get_afn_master(regexs)
        afd = Subset_construction.afn_to_afd(master)

        print(f"N de estados: {len(afd.estados)}")
        Filemanager.gerar_arquivo_scanner(afd)
    else:
        print("Uso: python gerar_scanner.py <regex.txt>")