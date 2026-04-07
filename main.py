from scanner_gen.leitor_regex import LeitorRegex

r = LeitorRegex.revelar_operador("(a|bc\+)d")
print(r)
res = LeitorRegex.shunting_yard(r)
print(res)
