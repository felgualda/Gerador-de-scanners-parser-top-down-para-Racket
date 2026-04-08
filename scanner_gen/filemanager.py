
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