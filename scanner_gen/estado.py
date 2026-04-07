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

    def visualizar(self):
        visitados = set()
        fila = [self.inicio]
        estados_encontrados = []

        while fila:
            atual = fila.pop(0)
            if atual in visitados:
                continue
            
            visitados.add(atual)
            estados_encontrados.append(atual)

            for destinos in atual.transicoes.values():
                for destino in destinos:
                    if destino not in visitados:
                        fila.append(destino)

        estados_encontrados.sort(key=lambda e: e.id)

        print("\n=== Autômato Finito Não Determinístico (AFN) ===")
        print(f"Estado Inicial: q{self.inicio.id}")
        print(f"Estado Final:   q{self.fim.id}")
        print("-" * 48)
        print("Lista de Transições:")
        
        for estado in estados_encontrados:
            marca_inicial = "->" if estado == self.inicio else "  "
            marca_final = " *" if estado == self.fim or estado.final else "  "
            nome_estado = f"q{estado.id}"
            
            prefixo = f"{marca_inicial}{marca_final} {nome_estado}"

            if not estado.transicoes:
                print(f"{prefixo} : Nenhuma transição")
            else:
                for simbolo, destinos in estado.transicoes.items():
                    # Formata o símbolo vazio (epsilon) para ficar legível
                    simb_print = "ε" if simbolo == "" or simbolo is None else simbolo
                    
                    for destino in destinos:
                        print(f"{prefixo} --({simb_print})--> q{destino.id}")
        print("================================================\n")