(define (analise-complexa p1 p2 p3 p4)
    (if (> (+ p1 p2) (* p3 p4))
        (begin
            (set! p1 (* p1 2))
            (if (> p1 100) 
                "estado-critico" 
                "estado-normal"
            )
        )
        (if (< p2 0)
            "valor-negativo"
            (if (= p3 0) 
                "erro-divisao-zero" 
                "processamento-ok"
            )
        )
    )
)

(define total (analise-complexa 10 20 5 2))

(define verificacao-final (if #t "sistema-ativo" "sistema-erro"))