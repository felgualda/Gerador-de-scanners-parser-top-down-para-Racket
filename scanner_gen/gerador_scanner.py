
def gerar_scanner(afd):
    matriz, mapa_c, num_colunas = gerar_matriz(afd)
    num_estados = len(afd.estados)

    with open("scanner.c", "w") as f:
        f.write("#include <stdio.h>\n\n")

        f.write("int mapa[128] = {" + ",".join(map(str, mapa_c)) + "};\n\n")

        f.write(f"int transicao[{num_estados}][{num_colunas}] = {{\n")
        for linha in matriz:
            f.write("    {" + ",".join(map(str, linha)) + "},\n")
        f.write("};\n\n")

        tokens = [e.token_id if e.final else -1 for e in afd.estados]
        f.write(f"int aceitacao[{num_estados}] = {{{','.join(map(str, tokens))}}};\n\n")

        f.write("""
int yylex(char* entrada, int* posicao) {
    int estado_atual = 0;
    int ultimo_estado_final = -1;
    int ultima_pos_final = *posicao;
    int p = *posicao;

    while (entrada[p] != '\\0') {
        int c = (int)entrada[p];
        
        if (c < 0 || c >= 128) break;

        int coluna = mapa[c];
        if (coluna == -1) break;

        int proximo = transicao[estado_atual][coluna];
        if (proximo == -1) break;

        estado_atual = proximo;
        p++;

        if (aceitacao[estado_atual] != -1) {
            ultimo_estado_final = estado_atual;
            ultima_pos_final = p;
        }
    }

    if (ultimo_estado_final != -1) {
        *posicao = ultima_pos_final;
        return aceitacao[ultimo_estado_final];
    }

    return -1; 
}
""")


def gerar_matriz(afd):
    estado_id = {estado: i for i, estado in enumerate(afd.estados)}

    alfabeto = set()
    for estado in afd.estados:
        for simbolo in estado.transicoes.keys():
            alfabeto.add(simbolo)
    
    alfabeto = sorted(list(alfabeto))
    num_colunas = len(alfabeto)

    char_para_coluna = {char: i for i, char in enumerate(alfabeto)}

    mapa_c = [-1] * 128
    for char, col in char_para_coluna.items():
        mapa_c[ord(char)] = col

    matriz = []
    for estado in afd.estados:
        linha = [-1] * num_colunas
        
        for simbolo, destino in estado.transicoes.items():
            coluna = char_para_coluna[simbolo]
            linha[coluna] = estado_id[destino]
            
        matriz.append(linha)
        
    return matriz, mapa_c, num_colunas