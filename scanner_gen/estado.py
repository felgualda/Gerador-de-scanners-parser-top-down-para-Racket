# fg

class Estado:
    _contador_id = 0

    def __init__(self):
        self.id = Estado._contador_id
        Estado._contador_id += 1

        self.transicoes = {}
        self.final = False

    def add_transicao(self, simbolo, estado_destino):
        if simbolo not in self.transicoes:
            self.transicoes[simbolo] = []
        self.transicoes[simbolo].append(estado_destino)

    def set_final(self, value):
        self.final = value

class AFN:
    def __init__(self,inicio,fim):
        self.inicio = inicio
        self.fim = fim
