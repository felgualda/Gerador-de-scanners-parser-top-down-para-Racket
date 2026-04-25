(define (potencia base expoente)
    (if (> expoente 0)
        (* base (potencia base (- expoente 1)))
        1
    )
)

(define (avalia-desempenho nota1 nota2 nota3)
    (if (> (+ nota1 (+ nota2 nota3)) 20)
        (if (> nota1 8)
            "aprovado-com-louvor"
            "aprovado"
        )
        "reprovado"
    )
)

(define resultado-potencia (potencia 2 10))

(define resultado-aluno (avalia-desempenho 7 8 6))