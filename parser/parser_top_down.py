class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.current_token = self.tokens[self.pos] if tokens else None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def report_error(self, mensagem):
        linha = self.current_token[2] if self.current_token and len(self.current_token) > 2 else "Final do arquivo"
        self.errors.append(f"Erro Sintático (Linha {linha}): {mensagem}")

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            self.report_error(f"Esperado {token_type}, mas encontrou {self.current_token[0] if self.current_token else 'EOF'}")
            if self.current_token:
                token = self.current_token
                self.advance()
                return token
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
        self.eat('LPAREN')
        
        if not self.current_token:
            self.report_error("Expressão incompleta após '('")
            return []
            
        token_type = self.current_token[0]
        lexema = self.current_token[1]
        
        if token_type == 'KW_IF':
            node = self.if_expression()
        elif token_type == 'ID' and lexema == 'define':
            node = self.define_expression()
        elif token_type == 'ID' and lexema == 'set!':
            node = self.set_expression()
        elif token_type == 'ID' and lexema == 'lambda':
            node = self.lambda_expression()
        elif token_type == 'ID' and lexema == 'let':
            node = self.let_expression('let')
        elif token_type == 'ID' and lexema == 'let-values':
            node = self.let_expression('let-values')
        elif token_type == 'KW_QUOTE' or (token_type == 'ID' and lexema == 'quote'):
            node = self.quote_expression()
        elif token_type == 'KW_MODULE' or (token_type == 'ID' and lexema == 'module'):
            node = self.module_expression()
        elif token_type == 'ID' and lexema == 'cond':
            node = self.cond_expression()
        elif token_type == 'ID' and lexema in ['and', 'or']:
            node = self.and_or_expression(lexema)
        elif token_type == 'ID' and lexema == 'define-values':
            node = self.define_values_expression()
        elif token_type == 'ID' and lexema in ['begin', 'begin0']:
            node = self.begin_expression(lexema)
        elif token_type == 'ID' and lexema in ['when', 'unless']:
            node = self.when_unless_expression(lexema)
        else:
            node = []
            while self.current_token and self.current_token[0] != 'RPAREN':
                node.append(self.expression())
        
        self.eat('RPAREN')
        return node

    def if_expression(self):
        node = [self.eat('KW_IF')] 
        
        for i in range(3):
            if self.current_token and self.current_token[0] != 'RPAREN':
                node.append(self.expression())
            else:
                self.report_error(f"O 'if' exige 3 argumentos, mas encontrou apenas {i}")
                break
                
        if self.current_token and self.current_token[0] != 'RPAREN':
            self.report_error("Argumentos extras encontrados no 'if'")
            while self.current_token and self.current_token[0] != 'RPAREN':
                self.advance() 
                
        return node

    def define_expression(self):
        node = [self.eat('ID')]
        
        if self.current_token and self.current_token[0] == 'LPAREN':
            sig = [self.eat('LPAREN')]
            while self.current_token and self.current_token[0] != 'RPAREN':
                if self.current_token[0] != 'ID':
                    self.report_error(f"Assinatura inválida: esperado ID, mas encontrou {self.current_token[0]}")
                sig.append(self.expression())
            sig.append(self.eat('RPAREN'))
            node.append(sig)
        else:
            node.append(self.eat('ID'))
            
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
            
        if count < 1:
            self.report_error(f"O 'define' requer pelo menos um valor ou corpo, mas não encontrou nenhum")
        elif count > 1 and isinstance(node[1], tuple) and node[1][0] == 'ID':
            self.report_error(f"O 'define' de variável requer apenas 1 valor, mas encontrou {count}")
            
        return node

    def set_expression(self):
        node = [self.eat('KW_SET')]
        node.append(self.eat('ID'))
        
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
            
        if count == 0:
            self.report_error("O 'set!' exige um valor de atribuição")
        elif count > 1:
            self.report_error(f"O 'set!' aceita apenas 1 valor, mas encontrou {count}")
            
        return node
    
    def module_expression(self):
        node = [self.eat('KW_MODULE')]
        node.append(self.eat('ID'))
        node.append(self.eat('ID'))
        
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
        return node
    
    def lambda_expression(self):
        node = [self.eat('KW_PLAIN_LAMBDA')]
        if self.current_token and self.current_token[0] == 'LPAREN':
            node.append(self.expression()) 
        else:
            self.report_error("O 'lambda' exige uma lista de argumentos")
        
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
        return node
    
    def quote_expression(self):
        node = [self.eat('KW_QUOTE')]
        
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
            
        if count != 1:
            self.report_error(f"O 'quote' exige exatamente 1 argumento, mas encontrou {count}")
            
        return node
    
    def let_expression(self, nome_let):
        node = [self.eat('ID' if nome_let == 'let' else 'ID')] 
        
        if self.current_token and self.current_token[0] in ['LPAREN', 'LBRACKET']:
            opener = self.current_token[0]
            closer = 'RPAREN' if opener == 'LPAREN' else 'RBRACKET'
            
            bindings = [self.eat(opener)]
            while self.current_token and self.current_token[0] != closer:
                if self.current_token[0] in ['LPAREN', 'LBRACKET']:
                    b_opener = self.current_token[0]
                    b_closer = 'RPAREN' if b_opener == 'LPAREN' else 'RBRACKET'
                    
                    binding = [self.eat(b_opener)]
                    while self.current_token and self.current_token[0] != b_closer:
                        binding.append(self.expression())
                    binding.append(self.eat(b_closer))
                    bindings.append(binding)
                else:
                    self.report_error(f"Binding malformado no '{nome_let}'")
                    self.advance()
            
            bindings.append(self.eat(closer))
            node.append(bindings)
        else:
            self.report_error(f"O '{nome_let}' exige uma lista de bindings")

        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
        
        if count == 0:
            self.report_error(f"O '{nome_let}' exige pelo menos uma expressão no corpo")
            
        return node
    
    def cond_expression(self):
        node = [self.eat('ID')]
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            if self.current_token[0] in ['LPAREN', 'LBRACKET']:
                opener = self.current_token[0]
                closer = 'RPAREN' if opener == 'LPAREN' else 'RBRACKET'
                
                clause = [self.eat(opener)]
                while self.current_token and self.current_token[0] != closer:
                    clause.append(self.expression())
                clause.append(self.eat(closer))
                node.append(clause)
                count += 1
            else:
                self.report_error("Cláusula de 'cond' malformada")
                self.advance()
        
        if count == 0:
            self.report_error("O 'cond' exige pelo menos uma cláusula")
        return node
    
    def and_or_expression(self, nome):
        node = [self.eat('ID')]
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
        return node

    def begin_expression(self, nome):
        node = [self.eat('ID')]
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
        if count == 0 and nome == 'begin0':
            self.report_error("'begin0' exige pelo menos uma expressão")
        return node

    def define_values_expression(self):
        node = [self.eat('ID')] 
        
        if self.current_token and self.current_token[0] == 'LPAREN':
            ids = [self.eat('LPAREN')]
            while self.current_token and self.current_token[0] != 'RPAREN':
                ids.append(self.eat('ID'))
            ids.append(self.eat('RPAREN'))
            node.append(ids)
        else:
            self.report_error("'define-values' exige uma lista de identificadores entre parênteses")
            if self.current_token and self.current_token[0] == 'ID':
                node.append(self.eat('ID'))

        node.append(self.expression())
        return node 

    def when_unless_expression(self, nome):
        node = [self.eat('ID')]
        node.append(self.expression())
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
        return node

    def atom(self):
        token = self.current_token
        if not token: return None
        
        tipos_aceitos = [
            'ID', 'INT', 'FLOAT', 'TRUE', 'FALSE', 'STRING', 'KW_IF',
            'KW_MODULE_STAR', 'KW_MODULE', 'KW_BEGIN_FOR_SYNTAX', 'KW_BEGIN0',
            'KW_BEGIN', 'KW_DEFINE_VALUES', 'KW_DEFINE_SYNTAXES', 'KW_CASE_LAMBDA',
            'KW_LETREC_VALUES', 'KW_LET_VALUES', 'KW_SET', 'KW_QUOTE_SYNTAX',
            'KW_QUOTE', 'KW_WITH_CONT_MARK', 'KW_EXPRESSION', 'KW_PLAIN_MOD_BEGIN',
            'KW_PROVIDE', 'KW_DECLARE', 'KW_REQUIRE', 'KW_PLAIN_LAMBDA',
            'KW_PLAIN_APP', 'KW_TOP', 'KW_VAR_REF', 'KW_LOCAL', 'DOT',
            'LBRACKET', 'RBRACKET'
        ]
        
        if token[0] == 'DOT':
            self.report_error("Uso inválido do ponto '.' fora de uma lista ou em posição incorreta")
            return self.eat('DOT')
        if token[0] in tipos_aceitos:
            return self.eat(token[0])
        else:
            self.report_error(f"Token inesperado '{token[1]}' ({token[0]})")
            self.advance()
            return None