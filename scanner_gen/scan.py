
class Scan:
    def ler(caminho,afd):
        resultado = []
        num_linha = 0

        with open(caminho, 'r', encoding='utf-8') as arquivo:

            estado_atual = afd.inicio

            pilha_simbolos = []

            for linha in arquivo:
                num_linha += 1
                coluna = 0
                linha = linha.strip()
                
                if not linha:
                    continue
                    
                i = 0
                while i < len(linha):
                    caracter = linha[i]

                    #print(caracter)

                    if estado_atual == afd.inicio and caracter in " \t\n\r":
                        i += 1
                        continue                    

                    if caracter in estado_atual.transicoes.keys():
                        pilha_simbolos.append(caracter)
                        prox = estado_atual.transicoes.get(caracter)
                        estado_atual = prox
                        i += 1
                    else:
                        if estado_atual.final:
                            resultado.append((estado_atual.token_id, "".join(pilha_simbolos), num_linha, coluna))
                            pilha_simbolos.clear()
                            estado_atual = afd.inicio
                        else:
                            print("CADEIA NÃO ACEITA")
                            break
                    coluna += 1

                if pilha_simbolos and estado_atual.final:       
                    resultado.append((estado_atual.token_id, "".join(pilha_simbolos), num_linha, coluna)) 
                    pilha_simbolos.clear() 
                    estado_atual = afd.inicio               

                    
        return resultado
                
                    