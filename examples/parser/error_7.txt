(module modulo-com-erros racket
    
    (define-values autor "Bruno")

    (define (teste-cond x)
        (cond 
            "clausula-invalida"
            [(> x 10) "ok"]
        )
    )

    (let-values ([soma 10]) 
        soma
    )

    (define q (quote 1 2 3))

    (when #t)

    (define . 100)
)
