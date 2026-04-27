(module teste-float racket
    ;; Definindo uma constante com ponto
    (define pi 3.14)

    ;; Operação aritmética com decimais
    (define (calcular-area raio)
        (* pi (* raio raio))
    )

    ;; Testando um float negativo
    (define ajuste -0.5)

    ;; Chamada simples
    (calcular-area 10.0)
)