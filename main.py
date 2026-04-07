from scanner_gen.leitor_regex import LeitorRegex

r1 = LeitorRegex.revelar_operador("(a|bc)d*")
r2 = LeitorRegex.shunting_yard(r1)
r3 = LeitorRegex.thompson_construction(r2)

r3.visualizar()