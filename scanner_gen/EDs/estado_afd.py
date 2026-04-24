# fg

class EstadoAFD:
    _contador_id = 0

    def __init__(self,conjunto_afn):
        self.id = EstadoAFD._contador_id
        EstadoAFD._contador_id += 1

        self.conjunto_afn = frozenset(conjunto_afn)

        self.transicoes = {}
        self.final = False
        self.token_id = None

    def add_transicao(self, simbolo, estado_destino):
        self.transicoes[simbolo] = estado_destino

    def set_final(self, value):
        self.final = value

class AFD:
    def __init__(self,inicio):
        self.inicio = inicio
        self.estados = []

    def add_estado(self, estado_afd):
        self.estados.append(estado_afd)