
# fg

class LeitorRegex:

    ### Esta função recebe uma expressão regular e explicita as concatenações, para que essa operação seja facilmente
    ### reconhecível na próxima etapa do programa, que é gerar a notação polonesa reversa.
    ### Exemplo: (ab|c)d -> (a.b|c).d
    @staticmethod
    def revelar_operador(regex):
        elementos = []
        i = 0

        while i < len(regex):
            if regex[i] == '\\':
                elementos.append("\\" + regex[i + 1])
                i += 2
            else:
                elementos.append(regex[i])
                i += 1

        #print(elementos)
        result = ''
            
        for j in range (len(elementos)-1):
            atual = elementos[j]
            prox = elementos[j+1]

            result += atual

            if atual != '(' and atual != '|':
                if prox != ')' and prox != '|' and prox != '*':
                    result+= '.'
            
        if elementos:
            result += elementos[-1]

        return result

    @staticmethod
    def precedencia(op):
        if op == '*': return 3
        if op == '.': return 2
        if op == '|': return 1
        if op == '(': return 0
    
    def is_operador(sim):
        if sim == '(' or sim == ')' or sim == '*' or sim == '.' or sim == '|':
            return True
        return False
    
    ### Esta função recebe uma expressão regular com todos os operadores explícitos e aplica o algoritmo de
    ### Shunting Yard de Dijkstra, para deixar a expressão na notação polonesa reversa, facilitando lidar com a
    ### precedência da regex.
    ### Exemplo: (a|b.c).d -> a b c . | d .
    @staticmethod
    def shunting_yard(regex):
        operadores = []     # Pilha de operadores
        saida = []          # Pilha de saída

        i = 0
        while i < len(regex):
            if not LeitorRegex.is_operador(regex[i]):   # é letra ou bloco com \
                if regex[i] == '\\':
                    saida.append('\\' + regex[i+1])
                    i += 2
                else:
                    saida.append(regex[i])
                    i += 1
            else:                                       # é operador
                if regex[i] == '(':
                    operadores.append(regex[i])
                elif regex[i] == ')':
                    o = operadores.pop()
                    while o != '(':
                        saida.append(o)
                        o = operadores.pop()
                else:
                    while operadores and LeitorRegex.precedencia(operadores[-1]) >= LeitorRegex.precedencia(regex[i]):
                        saida.append(operadores.pop())
                    operadores.append(regex[i])
                i += 1

        while operadores:
            saida.append(operadores.pop())

        return saida

    @staticmethod
    def thompson_construction(rpn):
        from scanner_gen.funcoes_afn import ConstrutorAFN
        pilha = []

        for e in rpn:
            if not LeitorRegex.is_operador(e):
                pilha.append(ConstrutorAFN.criar_simbolo(e))        
            elif e == '.':
                afn_2 = pilha.pop()
                afn_1 = pilha.pop()
                novo_afn = ConstrutorAFN.criar_concat(afn_1,afn_2)
                pilha.append(novo_afn)
            elif e == '|':
                afn_2 = pilha.pop()
                afn_1 = pilha.pop()
                novo_afn = ConstrutorAFN.criar_uniao(afn_1,afn_2)
                pilha.append(novo_afn)
            elif e == '*':
                novo_afn = ConstrutorAFN.criar_kleene(pilha.pop())
                pilha.append(novo_afn)

        return pilha[-1]
