class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.current_token = self.tokens[self.pos] if tokens else None

    def report_error(self, message):
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
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            return None

    def parse(self):
        tree = []
        while self.current_token is not None:
            expr = self.expression()
            if expr:
                tree.append(expr)
        
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
    
        if self.current_token and self.current_token[0] == 'RPAREN':
            self.eat('RPAREN')
            return node

        primeiro = self.current_token[0]
        
        if primeiro == 'IF':
            node = self.if_expression()
        elif primeiro == 'IDENTIFIER' and self.current_token[1] == 'define':
            node = self.define_expression()
        else:
            while self.current_token and self.current_token[0] != 'RPAREN':
                node.append(self.expression())
                
        self.eat('RPAREN')
        return node

    def if_expression(self):
        node = [self.eat('IF')] 
        
        for i in range(3):
            if self.current_token and self.current_token[0] != 'RPAREN':
                node.append(self.expression())
            else:
                self.report_error(f"O 'if' exige 3 argumentos, mas encontrou apenas {i}")
                break
                
        if self.current_token and self.current_token[0] != 'RPAREN':
            self.report_error("Argumentos extras encontrados no 'if'")
            while self.current_token and self.current_token[0] != 'RPAREN':
                self.pos += 1
                self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
                
        return node

    def define_expression(self):
        node = [self.eat('IDENTIFIER')]
        
        if self.current_token and self.current_token[0] not in ['IDENTIFIER', 'LPAREN']:
            self.report_error(f"O 'define' esperava um nome ou lista, mas encontrou {self.current_token[0]}")
        
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
            
        if count < 2:
            self.report_error(f"O 'define' requer nome e valor, mas encontrou apenas {count} argumento(s)")
        elif count > 2 and node[1][0] == 'IDENTIFIER':
            self.report_error(f"O 'define' de variável requer apenas 1 valor, mas encontrou {count - 1}")
            
        return node

    def atom(self):
        token = self.current_token
        if not token: return None
        
        tipos_aceitos = ['IDENTIFIER', 'INTEGER', 'FLOAT', 'BOOLEAN', 'STRING', 'IF', 'ELSE']
        if token[0] in tipos_aceitos:
            return self.eat(token[0])
        else:
            self.report_error(f"Token inesperado '{token[1]}' ({token[0]})")
            self.pos += 1 
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            return None
        
    def report_error(self, mensagem):
        linha = self.current_token[2] if self.current_token else "Final do ficheiro"
        self.errors.append(f"Erro Sintático (Linha {linha}): {mensagem}")