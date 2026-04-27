(module sistema-bancario racket
  ;; --- Definição de Constantes e Variáveis ---
  (define taxa-administrativa 0.02) ; Taxa de 2%
  (define limite-especial -500.0)
  (define saldo-cliente 1250.50)
  
  ;; --- Lógica de Cálculo de Juros ---
  (define (calcular-rendimento capital meses)
    (if (> meses 0)
        (let ([taxa-mensal 0.005])
          (* capital (+ 1.0 (* taxa-mensal meses))))
        capital))

  ;; --- Processador de Transações ---
  (define (executar-transacao tipo valor)
    (begin
      ; Registando a tentativa de operação
      (set! tipo tipo) 
      (cond
        [(equal? tipo "deposito")
         (set! saldo-cliente (+ saldo-cliente valor))]
        
        [(equal? tipo "saque")
         (if (>= (- saldo-cliente valor) limite-especial)
             (set! saldo-cliente (- saldo-cliente valor))
             "Erro: Limite insuficiente")]
             
        [else "Erro: Operação inválida"])))

  ;; --- Validação de Status da Conta ---
  (define (verificar-status saldo)
    (case saldo
      [(0.0) "Conta Zerada"]
      [(1000.0) "Cliente Ouro"]
      [else 
       (if (< saldo 0)
           "Conta no Vermelho"
           "Conta Regular")]))

  ;; --- Testes de Execução ---
  
  ; 1. Realizando um depósito inicial
  (executar-transacao "deposito" 500.0)
  
  ; 2. Aplicando rendimento via lambda
  (define novo-saldo 
    ((lambda (s) (+ s (* s taxa-administrativa))) saldo-cliente))
    
  ; 3. Verificação final com let aninhado
  (let ([status-final (verificar-status novo-saldo)])
    (begin
      (set! saldo-cliente novo-saldo)
      status-final))
)