from scanner_gen.EDs.estado_afn import AFN, EstadoAFN
from scanner_gen.funcoes_afn import ConstrutorAFN
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
    def prep(exp):
        i = 0
        while i < len(exp):
            if exp[i] == '[':
                if i > 0 and exp[i-1] == '\\':
                    i += 1
                    continue
                
                inicio_colchete = i
                
                j = i + 1
                while j < len(exp) and exp[j] != ']':
                    if exp[j] == '\\':
                        j += 2
                    else:
                        j += 1
                
                if j < len(exp):
                    fim_colchete = j
                    conteudo = exp[inicio_colchete+1 : fim_colchete]
                    
                    itens = []
                    k = 0
                    while k < len(conteudo):
                        if conteudo[k] == '\\':
                            itens.append('\\' + conteudo[k+1])
                            k += 2
                        elif k + 2 < len(conteudo) and conteudo[k+1] == '-':
                            inicio = ord(conteudo[k])
                            fim = ord(conteudo[k+2])
                            for char_code in range(inicio, fim + 1):
                                itens.append(chr(char_code))
                            k += 3
                        else:
                            itens.append(conteudo[k])
                            k += 1
                    
                    substituicao = "(" + "|".join(itens) + ")"
                    
                    exp = exp[:inicio_colchete] + substituicao + exp[fim_colchete+1:]
                    
                    i = inicio_colchete + len(substituicao) - 1
            i += 1
            
        i = 0
        while i < len(exp):
            if exp[i] in ['+', '?']:
                if i > 0 and exp[i-1] == '\\':
                    i += 1
                    continue
                
                operador = exp[i]
                fim_op = i
                inicio_op = i - 1
                
                if exp[inicio_op] == ')':
                    pares = 1
                    inicio_op -= 1
                    while inicio_op >= 0 and pares > 0:
                        if exp[inicio_op] == ')': pares += 1
                        elif exp[inicio_op] == '(': pares -= 1
                        inicio_op -= 1
                    inicio_op += 1 
                elif inicio_op - 1 >= 0 and exp[inicio_op - 1] == '\\':
                    inicio_op -= 1
                    
                operando = exp[inicio_op:fim_op]
                
                if operador == '+':
                    substituicao = f"{operando}({operando})*"
                elif operador == '?':
                    substituicao = f"({operando}|ε)"
                    
                exp = exp[:inicio_op] + substituicao + exp[i+1:]
                i = inicio_op + len(substituicao) - 1 
            i += 1
            
        return exp

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
        pilha = []

        for e in rpn:
            if not LeitorRegex.is_operador(e):
                simbolo_real = e[1] if str(e).startswith('\\') else e
                
                pilha.append(ConstrutorAFN.criar_simbolo(simbolo_real))     
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

    @staticmethod
    def get_afn(regex):
        expandido = LeitorRegex.prep(regex)
        exp_op = LeitorRegex.revelar_operador(expandido)
        rpn = LeitorRegex.shunting_yard(exp_op)
        return LeitorRegex.thompson_construction(rpn)
    
    @staticmethod
    def get_afn_master(regex_list):

        estado_inicial = EstadoAFN()

        for token, regex in regex_list:
            afn = LeitorRegex.get_afn(regex)
            afn.fim.token_id = token
            estado_inicial.add_transicao('epsilon',afn.inicio)

        return AFN(estado_inicial,None)