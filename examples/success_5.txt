(define (relu x)
    (if (> x 0)
        x
        0
    )
)

(define (neuronio peso entrada bias ativo)
    (if ativo
        (relu (+ (* peso entrada) bias))
        "neuronio-desligado"
    )
)

(define (camada-oculta p1 e1 b1 p2 e2 b2)
    (if #t
        (list
            (neuronio p1 e1 b1 #t)
            (neuronio p2 e2 b2 #f)
        )
        "falha-na-camada"
    )
)

(define output-final (camada-oculta 2 5 1 4 3 0))