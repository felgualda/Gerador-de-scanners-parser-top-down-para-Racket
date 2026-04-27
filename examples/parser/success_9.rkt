(define (contador-passo x)
    (begin
        (set! x (+ x 1))
        (if (> x 10)
            "limite-atingido"
            "dentro-do-esperado"
        )
    )
)

(define (calculo-aninhado a b)
    (+ (* a a) (/ b (+ a 1)))
)

(define valor-inicial 5)
(contador-passo valor-inicial)
(calculo-aninhado 10 20)