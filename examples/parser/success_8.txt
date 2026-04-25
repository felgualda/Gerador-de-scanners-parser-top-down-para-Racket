(module biblioteca-experimental racket
    (provide teste-logico processar-status)

    (define-values (autor versao status) (values "Bruno" 2.0 #t))

    (define (processar-status nota)
        (cond
            [(>= nota 9) "excelente"]
            [(>= nota 7) "aprovado"]
            [(< nota 5) (begin (display "alerta") "reprovado")]
            [else "recuperacao"]
        )
    )

    (define (teste-logico x y)
        (and (> x 0) (or (<= y 10) status) #t)
    )

    (define (executar-sequencia)
        (begin
            (display "Passo 1")
            (display "Passo 2")
            (+ 10 20)
        )
    )

    (define (notificar condicao)
        (begin
            (when condicao (display "Ativando..."))
            (unless condicao (display "Desligado."))
        )
    )
)

(define-values (a b) (values 10 20))
(teste-logico a b)