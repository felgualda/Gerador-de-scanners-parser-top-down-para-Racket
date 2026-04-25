(module sistema-incompleto)

(define (funcao-vazia x))

(define (calcula-invalido y)
    (if (> y 10)
        (set! y)
        "ok"
        "argumento-extra-no-if"
    )
)

(define (teste-assinatura "string-no-nome")
    100
)

(module final racket
    (provide +)