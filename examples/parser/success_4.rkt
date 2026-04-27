(define (fatorial n)
    (if #t
        1
        (* n (fatorial (- n 1)))
    )
)

(define (processa-dados status valor)
    (if status
        (fatorial valor)
        "dados-invalidos"
    )
)

(define resultado-final (processa-dados #t 5))