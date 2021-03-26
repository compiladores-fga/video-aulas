Exprεssões regulares
====================

Operações fundamentais:
    ε        Representa uma string vazia
    a,b,c... Símbolos do alfabeto
    A*       Identifica zero ou mais repetições de um padrão A
    A|B      Aceita o padrão A ou o padrão B 
    AB       Aceita string no padrão A seguida de string no padrão B
    (...)    Agrupa um padrão e permite definir a precedência de operações

Operações derivadas:
    +        A+ = AA*
    ?        A? = (A|ε) 
    {n}      A{2} = AA
    {,n}     A{,2} = (A|ε)(A|ε)
    {n,}     A{2,} = AAA*
    {n,m}    A{2,4} = AA(A|ε)(A|ε)
    []       [abcd] = (a|b|c|d)
             [^abcd] = (e|f|g|h|...)
             [a-c] = (a|b|c)
    
Operações não-regulares:
    (?P=name)    Encontra conteúdo de um grupo anterior (por nome)
    \1, \2, ...  Encontra conteúdo de um grupo anterior
    (?=...)      Lookahead positivo - aceita string que obedece o padrão, mas 
                 sem avançar na leitura
    (?!...)      Lookahead negativo - aceita string que viola o padrão, mas 
                 sem avançar na leitura
    (?<=...)     Lookbehind positivo - aceita string que obedeceu o padrão à 
                 esquerda, mas sem voltar a leitura
    (?<!...)     Lookbehind positivo - aceita string que violou o padrão à 
                 esquerda, mas sem voltar a leitura
    (?(id/name)yes|no) Execução condicional de padrões em expressões regulares



Relações entre operações e linguagens

L1 = {a, ab, abb, abbb, ...}  # RE: ab*
L2 = {aa, ab, ba, bb}         # RE: aa|ab|ba|bb, (a|b)(a|b)
L3 = {a, b}                   # RE: a|b
L4 = {a}                      # RE: a
L5 = {b}                      # RE: b

A ==> LA (linguagem gerada pela expr. regular A)
B ==> LB (linguagem gerada pela expr. regular B)

A|B ==> LA U LB (linguagem formada pela união das strings de A com B)
  A = a|b  (LA = {a, b})
  B = ab   (LB = {ab})  
  A|B = a|b|ab ==> {a, b, ab}

AB ==> produto cartesiano de concatenação de LA com LB
LA = {a, b, c}
LB = {d, e}

LA ⊗ LB = {(a ⊗ d), (a ⊗ e), (b ⊗ d), (b ⊗ e), (c ⊗ d), (c ⊗ e)}
 a ⊗ d  = concatenação(a, b)

A|B      Aceita o padrão A ou o padrão B 
AB       Aceita string no padrão A seguida de string no padrão B
A*       Identifica zero ou mais repetições de um padrão A