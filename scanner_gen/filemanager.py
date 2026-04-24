
class Filemanager:
    def carregar(caminho):
        regras = []
    
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                
                if not linha:
                    continue
                    
                partes = linha.split(maxsplit=1)
                
                nome_token = partes[0]
                regex_str = partes[1]
                regras.append((nome_token, regex_str))
                    
        return regras
    
    def gerar_arquivo_scanner(afd, nome_arquivo="scanner.py"):
        tabela_str = "{\n"
        finais_str = "{\n"

        for estado in afd.estados:
            transicoes = []
            for simbolo, estado_destino in estado.transicoes.items():
                transicoes.append(f"{repr(simbolo)}: {estado_destino.id}")
            
            transicoes_str = ", ".join(transicoes)
            tabela_str += f"    {estado.id}: {{{transicoes_str}}},\n"

            if estado.final:
                finais_str += f"    {estado.id}: {repr(estado.token_id)},\n"

        tabela_str += "}"
        finais_str += "}"

        codigo_template = f"""\
# Código gerado automaticamente.

TABELA_TRANSICOES = {tabela_str}
ESTADOS_FINAIS = {finais_str}
ESTADO_INICIAL = {afd.inicio.id}

def ler_codigo(codigo_fonte):
    tokens = []
    linha_atual = 1
    posicao = 0
    tamanho = len(codigo_fonte)

    while posicao < tamanho:
        char_atual = codigo_fonte[posicao]

        if char_atual in ' \\t\\n\\r':
            if char_atual == '\\n':
                linha_atual += 1
            posicao += 1
            continue

        estado_atual = ESTADO_INICIAL
        lexema_atual = ""
        ultimo_estado_final = None
        pos_ultimo_final = -1

        temp_pos = posicao
        while temp_pos < tamanho:
            c = codigo_fonte[temp_pos]
            
            if estado_atual in TABELA_TRANSICOES and c in TABELA_TRANSICOES[estado_atual]:
                estado_atual = TABELA_TRANSICOES[estado_atual][c]
                lexema_atual += c
                
                if estado_atual in ESTADOS_FINAIS:
                    ultimo_estado_final = estado_atual
                    pos_ultimo_final = temp_pos
                
                temp_pos += 1
            else:
                break

        if ultimo_estado_final is not None:
            token_id = ESTADOS_FINAIS[ultimo_estado_final]
            lexema_real = codigo_fonte[posicao : pos_ultimo_final + 1]
            tokens.append((token_id, lexema_real, linha_atual))
            
            posicao = pos_ultimo_final + 1
        else:
            print(f"Erro Léxico na linha {{linha_atual}}: Caractere inesperado '{{codigo_fonte[posicao]}}'")
            posicao += 1  # Pula o caractere inválido para não entrar em loop infinito

    return tokens

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            codigo = f.read()
            lista_tokens = ler_codigo(codigo)
            for t in lista_tokens:
                print(t)
    else:
        print("Uso: python meu_scanner.py <arquivo_racket.rkt>")
"""

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(codigo_template)
        
        print(f"O arquivo '{nome_arquivo}' foi gerado.")