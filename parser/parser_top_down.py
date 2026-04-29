class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.current_token = self.tokens[self.pos] if tokens else None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def report_error(self, mensagem, sugestao=None):
        token = self.current_token
        
        if token:
            linha = token[2]
            coluna = token[3]
            lexema = f"'{token[1]}'"
        else:
            linha = "final do arquivo"
            coluna = "final"
            lexema = "fim do arquivo (EOF)"

        msg_completa = f"Erro (Linha {linha}, Coluna {coluna}): {mensagem}"
        
        if sugestao:
            msg_completa += f"\nSugestão: {sugestao}"
        
        self.errors.append(msg_completa)
        
    def eat(self, token_type, sugestao=None):
        if self.current_token and self.current_token[0] == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            encontrado = self.current_token[1] if self.current_token else "EOF"
            
            msg = f"Esperava encontrar o tipo {token_type}, mas encontrou '{encontrado}'"
            
            self.report_error(msg, sugestao)
            
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
        
        if token_type == 'KW_IF' or (token_type == 'ID' and lexema == 'if'):
            node = self.if_expression()
        elif token_type == 'KW_DEFINE' or (token_type == 'ID' and lexema == 'define'): 
            node = self.define_expression()
        elif token_type == 'KW_SET' or (token_type == 'ID' and lexema == 'set!'): 
            node = self.set_expression()
        elif token_type == 'KW_LAMBDA' or (token_type == 'ID' and lexema == 'lambda'): 
            node = self.lambda_expression()
        elif token_type == 'KW_LET' or (token_type == 'ID' and lexema == 'let'):
            node = self.let_expression('let')
        elif token_type == 'KW_QUOTE' or (token_type == 'ID' and lexema == 'quote'):
            node = self.quote_expression()
        elif token_type == 'KW_MODULE' or (token_type == 'ID' and lexema == 'module'):
            node = self.module_expression()
        elif token_type == 'KW_COND' or (token_type == 'ID' and lexema == 'cond'):
            node = self.cond_expression()
        elif token_type in ['KW_AND', 'KW_OR'] or (token_type == 'ID' and lexema in ['and', 'or']):
            node = self.and_or_expression()
        elif token_type == 'KW_DEFINE_VALUES' or (token_type == 'ID' and lexema == 'define-values'):
            node = self.define_values_expression()
        elif token_type in ['KW_BEGIN', 'KW_BEGIN0'] or (token_type == 'ID' and lexema in ['begin', 'begin0']):
            node = self.begin_expression(lexema)
        elif token_type in ['KW_WHEN', 'KW_UNLESS'] or (token_type == 'ID' and lexema in ['when', 'unless']):
            node = self.when_unless_expression()
        elif token_type == 'KW_CASE' or (token_type == 'ID' and lexema == 'case'):
            node = self.case_expression()
        elif token_type == 'KW_DEFINE_SYNTAXES' or (token_type == 'ID' and lexema in ['define-syntax', 'define-syntaxes']):
            node = self.define_syntax_expression()
        else:
            node = []
            while self.current_token and self.current_token[0] != 'RPAREN':
                node.append(self.expression())
        
        self.eat('RPAREN')
        return node

    def if_expression(self):
        tipo_real = 'KW_IF' if self.current_token[0] == 'KW_IF' else 'ID'
        node = [self.eat(tipo_real)]
        
        for i in range(3):
            if self.current_token and self.current_token[0] != 'RPAREN':
                node.append(self.expression())
            else:
                dicas = ["o predicado (condição)", "o caso verdadeiro", "o caso falso"]
                sugestao = "Estrutura do if: (if <condição> <v-verdade> <v-falso>)"
                self.report_error(f"O 'if' exige 3 argumentos, mas faltou {dicas[i]}", sugestao)
                break
                
        if self.current_token and self.current_token[0] != 'RPAREN':
            sugestao = (
                "Estrutura do if: (if <cond> <v1> <v2>)\n"
                "Estrutura do cond: (cond [<teste1> <res1>] [<teste2> <res2>] [else <res-padrao>])"
            )
            self.report_error("Muitos argumentos para o 'if'.", 
                              f"O 'if' só aceita 3 partes. Para múltiplas condições, use 'cond':\n{sugestao}")
            
            while self.current_token and self.current_token[0] != 'RPAREN':
                self.advance() 
                
        return node

    def define_expression(self):
        tipo_esperado = 'KW_DEFINE' if self.current_token[0] == 'KW_DEFINE' else 'ID'
        node = [self.eat(tipo_esperado)]

        if self.current_token and self.current_token[0] == 'LPAREN':
            sig = [self.eat('LPAREN')]
            while self.current_token and self.current_token[0] != 'RPAREN':
                if self.current_token[0] != 'ID':
                    sugestao = "Os parâmetros de uma função devem ser identificadores.\nEstrutura: (define (<nome> <param1> <param2> ...) <corpo>)"
                    self.report_error(f"Parâmetro inválido: '{self.current_token[1]}'", sugestao)
                sig.append(self.expression())
            
            sugestao_par = "Feche a lista de parâmetros com ')'.\nEstrutura: (define (<nome> <params>) <corpo>)"
            sig.append(self.eat('RPAREN', sugestao_par))
            node.append(sig)
        else:
            sugestao_var = "Defina um nome para sua variável.\nEstrutura: (define <nome> <valor>)\nExemplo: (define x 10)"
            node.append(self.eat('ID', sugestao_var))
            
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
            
        if count < 1:
            sugestao_corpo = "Toda definição exige um valor ou lógica de execução.\nVariável: (define x 10)\nFunção: (define (f x) (+ x 1))"
            self.report_error("Faltou o corpo do 'define'", sugestao_corpo)
            
        return node

    def set_expression(self):
        node = [self.eat('KW_SET' if self.current_token[0] == 'KW_SET' else 'ID')]
        
        sugestao_id = "O 'set!' exige o nome de uma variável já existente para ser alterada.\nEstrutura: (set! <variável> <novo-valor>)\nExemplo: (set! saldo 100)"
        node.append(self.eat('ID', sugestao_id))
        
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
            
        if count == 0:
            sugestao_vazio = "O 'set!' precisa de um valor para realizar a atribuição.\nEstrutura: (set! <variável> <valor>)"
            self.report_error("O 'set!' exige um valor de atribuição", sugestao_vazio)
        elif count > 1:
            sugestao_muitos = "O 'set!' só pode atualizar uma variável por vez com um único valor.\nEstrutura: (set! <variável> <valor>)"
            self.report_error(f"O 'set!' recebeu {count} valores", sugestao_muitos)
            
        return node
    
    def module_expression(self):
        node = [self.eat('KW_MODULE' if self.current_token[0] == 'KW_MODULE' else 'ID')]
        
        sugestao_nome = "O comando 'module' exige um nome para o módulo.\nEstrutura: (module <nome> <linguagem> <body>)"
        node.append(self.eat('ID', sugestao_nome))
        
        sugestao_lang = "O comando 'module' exige a especificação de uma linguagem.\nEstrutura: (module <nome> <linguagem> <body>)\nExemplo: (module meu-app racket)"
        node.append(self.eat('ID', sugestao_lang))
        
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            
        return node
    
    def lambda_expression(self):
        node = [self.eat('KW_LAMBDA' if self.current_token[0] == 'KW_LAMBDA' else 'ID')]
        
        if self.current_token and self.current_token[0] == 'LPAREN':
            node.append(self.expression()) 
        else:
            sugestao_args = "O 'lambda' exige uma lista de argumentos entre parênteses, mesmo que vazia.\nEstrutura: (lambda (<argumentos>) <corpo>)\nExemplo: (lambda (x y) (+ x y))"
            self.report_error("Lista de argumentos ausente no 'lambda'", sugestao_args)
        
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
            
        if count == 0:
            sugestao_corpo = "Uma função anônima precisa de pelo menos uma expressão para executar.\nEstrutura: (lambda (<argumentos>) <corpo>)\nExemplo: (lambda () 42)"
            self.report_error("O 'lambda' exige pelo menos uma expressão no corpo", sugestao_corpo)
            
        return node
    
    def quote_expression(self):
        node = [self.eat('KW_QUOTE' if self.current_token[0] == 'KW_QUOTE' else 'ID')]
        
        arg = self.expression()
        if arg:
            node.append(arg)
        else:
            sugestao_vazio = "O 'quote' transforma código em dado literal e precisa de um objeto para ser congelado.\nEstrutura: (quote <dado>)\nExemplo: (quote (1 2 3))"
            self.report_error("O 'quote' exige um argumento", sugestao_vazio)
        
        if self.current_token and self.current_token[0] != 'RPAREN':
            sugestao_muitos = "O 'quote' aceita apenas um único argumento (um átomo ou uma lista completa).\nEstrutura: (quote <dado>)\nPara citar vários itens, use: (quote (a b c))"
            self.report_error("Muitos argumentos para o 'quote'", sugestao_muitos)
            while self.current_token and self.current_token[0] != 'RPAREN':
                self.advance()
                
        return node
    
    def let_expression(self, nome_let):
        tipo_esperado = 'KW_LET' if self.current_token[0] == 'KW_LET' else 'ID'
        node = [self.eat(tipo_esperado)]

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
                    sugestao = (
                    "Cada associação (binding) deve estar entre colchetes ou parênteses.\n"
                    "Estrutura: (let ([var1 valor1] [var2 valor2]) <corpo>)"
                    )
                    self.report_error(f"Binding malformado no '{nome_let}'", sugestao)
                    self.advance()
            
            bindings.append(self.eat(closer))
            node.append(bindings)
        else:
            self.report_error(f"O '{nome_let}' exige uma lista de associações", 
                              "Tente envolver suas variáveis em parênteses: (let ([x 1] [y 2]) ...)")

        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
        
        if count == 0:
            sugestao = (
                "O corpo do let é onde o código é executado usando as variáveis locais.\n"
                "Exemplo: (let ([x 10]) (+ x 5))"
            )
            self.report_error(f"O '{nome_let}' exige pelo menos uma expressão no corpo", sugestao)
            
        return node
    
    def cond_expression(self):
        tipo = 'KW_COND' if self.current_token[0] == 'KW_COND' else 'ID'
        node = [self.eat(tipo)]
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
                sugestao = "Cada cláusula deve ser: [<condição> <resultado>]. Ex: (cond [(= x 1) \"um\"] [else \"erro\"])"
                self.report_error("Cláusula de 'cond' malformada (faltou '[' ou '(')", sugestao)
                self.advance()
        
        if count == 0:
            self.report_error("O 'cond' não tem nenhuma cláusula", 
                              "Adicione pelo menos um teste: (cond [(> x 0) #t] [else #f])")
        return node
    
    def and_or_expression(self):
        tipo = self.current_token[0] if self.current_token[0] in ['KW_AND', 'KW_OR'] else 'ID'
        nome = self.current_token[1]
        
        sugestao_logica = f"Operadores lógicos permitem avaliar múltiplas condições.\nEstrutura: ({nome} <expressão1> <expressão2> ...)\nExemplo: ({nome} (> x 0) (< x 10))"
        node = [self.eat(tipo, sugestao_logica)]
        
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            
        return node
    
    def begin_expression(self, nome):
        tipo = self.current_token[0] if self.current_token[0] in ['KW_BEGIN', 'KW_BEGIN0'] else 'ID'
        
        sugestao_begin = f"O comando '{nome}' serve para agrupar uma sequência de comandos.\nEstrutura: ({nome} <expr1> <expr2> ...)"
        node = [self.eat(tipo, sugestao_begin)]
        
        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            count += 1
            
        if count == 0 and nome == 'begin0':
            sugestao_begin0 = "O 'begin0' executa todas as expressões, mas retorna obrigatoriamente o valor da PRIMEIRA.\nEstrutura: (begin0 <expressão-de-retorno> <expressões-adicionais> ...)"
            self.report_error("'begin0' exige pelo menos uma expressão", sugestao_begin0)
            
        return node

    def define_values_expression(self):
        tipo = 'KW_DEFINE_VALUES' if self.current_token[0] == 'KW_DEFINE_VALUES' else 'ID'
        node = [self.eat(tipo)] 
        
        if self.current_token and self.current_token[0] == 'LPAREN':
            ids = [self.eat('LPAREN')]
            while self.current_token and self.current_token[0] != 'RPAREN':
                ids.append(self.eat('ID'))
            ids.append(self.eat('RPAREN'))
            node.append(ids)
        else:
            sugestao = "Estrutura correta: (define-values (id1 id2 ...) <expressão-geradora>)\nExemplo: (define-values (x y) (values 1 2))"
            self.report_error("'define-values' exige uma lista de identificadores entre parênteses", sugestao)
            if self.current_token and self.current_token[0] == 'ID':
                node.append(self.eat('ID'))

        node.append(self.expression())
        return node

    def when_unless_expression(self):
        tipo = self.current_token[0] if self.current_token[0] in ['KW_WHEN', 'KW_UNLESS'] else 'ID'
        nome = self.current_token[1]
        
        sugestao_base = f"O comando '{nome}' executa um bloco de código se a condição for atendida.\nEstrutura: ({nome} <condição> <corpo>)\nExemplo: ({nome} (zero? x) (display \"é zero\"))"
        node = [self.eat(tipo, sugestao_base)]
        
        condicao = self.expression()
        if condicao:
            node.append(condicao)
        else:
            self.report_error(f"Faltou a condição do '{nome}'", sugestao_base)
            
        while self.current_token and self.current_token[0] != 'RPAREN':
            node.append(self.expression())
            
        return node
    
    def case_expression(self):
        tipo = 'KW_CASE' if self.current_token[0] == 'KW_CASE' else 'ID'
        sugestao_case = "O 'case' compara um valor contra várias listas de constantes.\nEstrutura: (case <alvo> [(lista-valores) corpo] ... [else corpo])"
        node = [self.eat(tipo, sugestao_case)] 
        
        alvo = self.expression()
        if alvo:
            node.append(alvo)
        else:
            self.report_error("O 'case' exige um valor alvo para comparação", sugestao_case)

        count = 0
        while self.current_token and self.current_token[0] != 'RPAREN':
            if self.current_token[0] in ['LPAREN', 'LBRACKET']:
                opener = self.current_token[0]
                closer = 'RPAREN' if opener == 'LPAREN' else 'RBRACKET'
                clause = [self.eat(opener)]
                
                clause.append(self.expression()) 
                while self.current_token and self.current_token[0] != closer:
                    clause.append(self.expression())
                
                clause.append(self.eat(closer))
                node.append(clause)
                count += 1
            else:
                sugestao_clausula = "Cada opção do 'case' deve estar entre parênteses ou colchetes.\nExemplo: [(1 2 3) \"pequeno\"] [else \"grande\"]"
                self.report_error("Cláusula de 'case' malformada", sugestao_clausula)
                self.advance()
        
        if count == 0:
            self.report_error("O 'case' exige pelo menos uma cláusula de teste ou um 'else'", sugestao_case)
            
        return node

    def define_syntax_expression(self):
        tipo = 'KW_DEFINE_SYNTAXES' if self.current_token[0] == 'KW_DEFINE_SYNTAXES' else 'ID'
        sugestao_syntax = "O comando 'define-syntax' vincula um transformador a uma nova palavra-chave de sintaxe.\nEstrutura: (define-syntax <nome> <expressão-transformadora>)\nExemplo: (define-syntax meu-if (lambda (stx) ...))"
        node = [self.eat(tipo, sugestao_syntax)]
        
        sugestao_id = "A macro precisa de um nome identificador.\nEstrutura: (define-syntax <identificador> <corpo>)"
        node.append(self.eat('ID', sugestao_id))
        
        corpo = self.expression()
        if corpo:
            node.append(corpo)
        else:
            sugestao_corpo = "Uma macro exige um corpo que defina a regra de transformação (geralmente usando syntax-rules ou um transformador explícito)."
            self.report_error("Faltou a expressão transformadora no 'define-syntax'", sugestao_corpo)
            
        return node

    def atom(self):
        token = self.current_token
        if not token: return None
        
        tipos_aceitos = [
            'ID', 'INT', 'FLOAT', 'TRUE', 'FALSE', 'STRING', 'KW_IF',
            'KW_MODULE_STAR', 'KW_MODULE', 'KW_DEFINE', 'KW_LAMBDA',
            'KW_LET', 'KW_COND', 'KW_ELSE', 'KW_AND', 'KW_OR',
            'KW_WHEN', 'KW_UNLESS', 'KW_CASE', 'KW_BEGIN_FOR_SYNTAX',
            'KW_BEGIN0', 'KW_BEGIN', 'KW_DEFINE_VALUES', 'KW_DEFINE_SYNTAXES',
            'KW_CASE_LAMBDA', 'KW_LETREC_VALUES', 'KW_LET_VALUES', 'KW_SET',
            'KW_QUOTE_SYNTAX', 'KW_QUOTE', 'KW_WITH_CONT_MARK', 'KW_EXPRESSION',
            'KW_PLAIN_MOD_BEGIN', 'KW_PROVIDE', 'KW_DECLARE', 'KW_REQUIRE',
            'KW_PLAIN_LAMBDA', 'KW_PLAIN_APP', 'KW_TOP', 'KW_VAR_REF',
            'KW_LOCAL', 'DOT', 'LBRACKET', 'RBRACKET'
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