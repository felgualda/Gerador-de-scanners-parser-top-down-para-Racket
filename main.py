from scanner_gen.gerador_afn import LeitorRegex
from scanner_gen.gerador_afd import Subset_construction

r1 = LeitorRegex.revelar_operador("d*")
r2 = LeitorRegex.shunting_yard(r1)
r3 = LeitorRegex.thompson_construction(r2)

afd = Subset_construction.afn_to_afd(r3)

afd.visualizar()