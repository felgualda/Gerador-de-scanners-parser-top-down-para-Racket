from scanner_gen.leitor_regex import LeitorRegex

r1 = LeitorRegex.revelar_operador("(a|bc)d")
#print(r1)
r2 = LeitorRegex.shunting_yard(r1)
#print(r2)
r3 = LeitorRegex.thompson_construction(r2)
#print(r3)

r3.visualizar()