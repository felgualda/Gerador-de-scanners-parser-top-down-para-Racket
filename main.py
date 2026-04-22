from scanner_gen.filemanager import Filemanager
from scanner_gen.scan import Scan
from scanner_gen.gerador_afn import LeitorRegex
from scanner_gen.gerador_afd import Subset_construction
import scanner_gen.gerador_scanner

regexs = Filemanager.carregar("scanner_gen/teste.txt")
master = LeitorRegex.get_afn_master(regexs)

afd = Subset_construction.afn_to_afd(master)

#afd.visualizar()

lista_tokens = Scan.ler("scanner_gen/code.txt",afd)
scanner_gen.gerador_scanner.gerar_scanner(afd)
print(f"N de estados: {len(afd.estados)}")
print()
print(lista_tokens)
print()
