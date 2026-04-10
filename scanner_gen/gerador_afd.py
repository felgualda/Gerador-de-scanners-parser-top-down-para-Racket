
from .EDs.estado_afd import AFD, EstadoAFD


class Subset_construction:

    @staticmethod
    def epsilon_reach(estados):
        pilha = []
        result = set()

        for s in estados:
            if s not in result:
                pilha.append(s)
                result.add(s)
        
        while pilha:
            atual = pilha.pop()

            if 'epsilon' in atual.transicoes.keys():
                for neighbor in atual.transicoes.get('epsilon'):
                    if neighbor not in result:
                        pilha.append(neighbor)
                        result.add(neighbor)

        return result
    
    @staticmethod
    def move(estados, simbolo):
        destinos = set()
        for s in estados:
            if simbolo in s.transicoes.keys():
                for dest in s.transicoes[simbolo]:
                    destinos.add(dest)
        return destinos
    
    @staticmethod
    def get_alfabeto(afn_inicio):
        alfabeto = set()
        visitados = set()
        fila = [afn_inicio]

        while fila:
            atual = fila.pop(0)
            if atual in visitados: continue
            visitados.add(atual)

            for simbolo, destinos in atual.transicoes.items():
                if simbolo != 'epsilon' and simbolo != '' and simbolo is not None:
                    alfabeto.add(simbolo)
                for dest in destinos:
                    if dest not in visitados:
                        fila.append(dest)

        return list(alfabeto)

    @staticmethod
    def afn_to_afd(afn):
        alfabeto = Subset_construction.get_alfabeto(afn.inicio)

        mapa = {}
        fila = []

        set_inicial = Subset_construction.epsilon_reach([afn.inicio])
        estado_inicial = EstadoAFD(set_inicial)

        mapa[estado_inicial.conjunto_afn] = estado_inicial

        fila.append(estado_inicial)

        afd = AFD(estado_inicial)
        afd.add_estado(estado_inicial)

        while fila:
            atual = fila.pop(0)

            for simbolo in alfabeto:
                target_move = Subset_construction.move(atual.conjunto_afn, simbolo)

                if not target_move:
                    continue

                u = Subset_construction.epsilon_reach(target_move)
                setkey = frozenset(u)

                if setkey not in mapa:

                    novo_estado = EstadoAFD(setkey)
                    mapa[setkey] = novo_estado
                    fila.append(novo_estado)
                    afd.add_estado(novo_estado)

                atual.add_transicao(simbolo, mapa[setkey])

        for s_afd in afd.estados:
            for s_afn in s_afd.conjunto_afn:
                if s_afn.final:
                    s_afd.final = True

                    if s_afn.token_id:
                        s_afd.token_id = s_afn.token_id
                        break
        return afd