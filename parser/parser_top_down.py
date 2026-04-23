class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = [] # Lista para armazenar as strings de erro
        self.current_token = self.tokens[self.pos] if tokens else None

    def report_error(self, message):
        # Captura a linha do token atual, se disponível
        line = self.current_token[2] if self.current_token and len(self.current_token) > 2 else "desconhecida"
        error_msg = f"Erro na linha {line}: {message}"
        self.errors.append(error_msg)

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            token = self.current_token
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            return token
        else:
            expected = token_type
            found = self.current_token[0] if self.current_token else "EOF"
            self.report_error(f"Esperado '{expected}', mas encontrou '{found}'")
            # Sincronização simples: avança um token para tentar continuar
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            return None

    def parse(self):
        tree = []
        while self.current_token is not None:
            expr = self.expression()
            if expr:
                tree.append(expr)
        
        # Se houver erros, retorna a lista de erros; caso contrário, a árvore
        return self.errors if self.errors else tree

    def expression(self):
        if not self.current_token: return None
        
        if self.current_token[0] == 'LPAREN':
            return self.list_expression()
        else:
            return self.atom()

    def list_expression(self):
        node = []
        self.eat('LPAREN')
        # Sincronização: continua a ler até fechar o parêntese ou acabar os tokens
        while self.current_token and self.current_token[0] != 'RPAREN':
            child = self.expression()
            if child:
                node.append(child)
        self.eat('RPAREN')
        return node

    def atom(self):
        token = self.current_token
        if not token: return None
        
        tipos_aceitos = ['IDENTIFIER', 'INTEGER', 'FLOAT', 'BOOLEAN', 'STRING', 'IF', 'ELSE']
        if token[0] in tipos_aceitos:
            return self.eat(token[0])
        else:
            self.report_error(f"Token inesperado '{token[1]}' ({token[0]})")
            self.pos += 1 # Avança para evitar loop infinito
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            return None
        
    def report_error(self, mensagem):
        linha = self.current_token[2] if self.current_token else "Final do ficheiro"
        self.errors.append(f"Erro Sintático (Linha {linha}): {mensagem}")