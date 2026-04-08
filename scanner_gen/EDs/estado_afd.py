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

    def visualizar(self):
        print("\n=== Autômato Finito Determinístico (AFD) ===")
        print(f"Estado Inicial: q{self.inicio.id}")
        print("-" * 60)
        print("Lista de Estados e Transições:\n")

        estados_ordenados = sorted(self.estados, key=lambda e: e.id)

        for estado in estados_ordenados:
            marca_inicial = "->" if estado == self.inicio else "  "
            marca_final = " *" if estado.final else "  "
            nome_estado = f"q{estado.id}"

            ids_afn = sorted([e.id for e in estado.conjunto_afn])
            conjunto_str = "{" + ", ".join(f"q{i}" for i in ids_afn) + "}"
            
            token_str = f" [Token: {estado.token_id}]" if estado.token_id else ""

            prefixo = f"{marca_inicial}{marca_final} {nome_estado}"
            
            print(f"{prefixo} (Origem AFN: {conjunto_str}){token_str}")

            if not estado.transicoes:
                espacamento = " " * len(prefixo)
                print(f"{espacamento} : Nenhuma transição")
            else:
                for simbolo in sorted(estado.transicoes.keys()):
                    destino = estado.transicoes[simbolo]
                    espacamento = " " * len(prefixo)
                    print(f"{espacamento} --({simbolo})--> q{destino.id}")
            
            print()
        print("============================================================\n")