from lark import Lark, InlineTransformer

grammar = Lark(
    r"""
start  : sum

?sum   : sum "+" mul  -> add     
       | sum "-" mul  -> sub
       | mul

?mul   : mul "*" pow  -> mul     
       | mul "/" pow  -> div     
       | pow

?pow   : unary "^" pow  -> pow     
       | unary

?unary : "-" atom -> neg
       | "+" atom -> pos

?atom  : NUMERO
       | "(" sum ")"

NUMERO : ("0".."9")+

%ignore " "
"""
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow, neg

    def NUMERO(self, tk):
        return int(tk)


transformer = CalcTransformer()
# exemplos = '40 2 +', '3 2 - 1 -', '2 10 4 * +', '4 3 2 ^ ^'
exemplos = "40 + 2",  # , '3 - 2 - (-1)', '(2 + 10) * 4', '4 ^ 3 ^ 2'

for src in exemplos:
    tree = grammar.parse(src)
    print(src)
    print(tree.pretty())
    print(transformer.transform(tree).pretty())