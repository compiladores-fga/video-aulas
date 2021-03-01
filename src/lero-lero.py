# pip install lark-parser hypothesis
from lark import Lark
from hypothesis.extra.lark import from_lark

# https://www.em.com.br/app/noticia/cultura/2021/03/01/interna_cultura,1241408/horoscopo-do-dia-01-03-confira-a-previsao-de-hoje-para-seu-signo.shtml
grammar = Lark(r"""
start : title NL NL intro "." (NL generalidade ".")~2..4
title : SIGNO

intro : PLANETA [planeta_aposto] " se encontra" [SP "com" PLANETA] " em " SIGNO
planeta_aposto : ", seu regente,"
               | ", seu ascendente,"

generalidade : "Sua capacidade de se prover, em especial materialmente e financeiramente, se faz alta"
             | "Estará muito mais generoso e ativo na resolução de questões práticas" 
             | "Seja generoso no uso de seus talentos também"
             | "A Lua e os planetas em Aquário lhe conectam às relações humanas, pedindo troca e envolvimento"

SP    : " "
NL    : "\n"
SIGNO   : "Áries" | "Touro" | "Gêmeos" | "Câncer" | "Leão" | "Virgem" | "Libra" | "Escorpião" | "Serpentário" | "Sagitário" | "Capricórnio" | "Aquário" | "Peixes"
PLANETA : "Mercúrio" | "Vênus" | "Lua" | Marte" | "Júpiter" | "Saturno" | "Urano" | "Netuno" | "Plutão" | "Éris" | "Ceres" | "Haumea" | "Makemake" | "Sedna" 
""")

strategy = from_lark(grammar)
msg = strategy.example()
print('\n\n\n\n\n')
print(msg)