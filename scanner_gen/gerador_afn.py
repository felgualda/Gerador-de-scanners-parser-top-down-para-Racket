# fg

from scanner_gen.estado import AFN, Estado

class ConstrutorAFN():

    @staticmethod
    def criar_simbolo(caractere):
        estado_inicio = Estado()
        estado_fim = Estado()
        estado_fim.set_final(True)

        estado_inicio.add_transicao(caractere, estado_fim)
        return AFN(estado_inicio, estado_fim)
    
    @staticmethod
    def criar_concat(afn1, afn2):
        afn1.fim.set_final(False)
        afn1.fim.add_transicao('epsilon', afn2.inicio)
        return AFN(afn1.inicio, afn2.fim)
    
    @staticmethod
    def criar_uniao(afn1, afn2):
        novo_inicio = Estado()
        novo_fim = Estado()
        novo_fim.set_final()

        novo_inicio.add_transicao('epsilon', afn1.inicio)
        novo_inicio.add_transicao('epsilon', afn2.inicio)

        afn1.fim.set_final(False)
        afn2.fim.set_final(False)

        afn1.fim.add_transicao('epsilon', novo_fim)
        afn2.fim.add_transicao('epsilon', novo_fim)

        return AFN(novo_inicio, novo_fim)
    
    @staticmethod
    def criar_kleene(afn):
        novo_inicio = Estado()
        novo_fim = Estado()

        novo_fim.set_final(True)

        novo_inicio.add_transicao('epsilon', afn.inicio)
        novo_inicio.add_transicao('epsilon', novo_fim)

        afn.fim.set_final(False)

        afn.fim.set_final(False)
        afn.fim.add_transicao('epsilon', afn.inicio)
        afn.fim.add_transicao('epsilon', novo_fim)
