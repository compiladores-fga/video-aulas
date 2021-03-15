import cmath
from lark import Lark, InlineTransformer

grammar = Lark(
    r"""
start  : expr

?expr  : sum

?sum   : sum "+" mul    -> add     
       | sum "-" mul    -> sub
       | mul

?mul   : mul "*" pow    -> mul     
       | mul "/" pow    -> div     
       | pow

?pow   : unary "^" pow  -> pow     
       | unary

?unary : "-" atom       -> neg 
       | "+" atom       -> pos
       | atom

?atom  : INT
       | COMPLEX
       | NAME              -> name
       | NAME "(" expr ")" -> func
       | "(" expr ")"

INT     : ("0".."9")+
COMPLEX : INT "i"
NAME    : ("a".."z" | "_" | "A".."Z")+

%ignore " "
"""
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow, neg, pos
    names = {
        "pi": cmath.pi, 
        "e": cmath.e, 
        "answer": 42,
        "log": cmath.log,
        "sqrt": cmath.sqrt,
    }

    def __init__(self):
        super().__init__()
        self.env = self.names.copy()

    def INT(self, tk):
        return int(tk)

    def COMPLEX(self, tk):
        return self.INT(tk[:-1]) * 1j

    def name(self, tk):
        try:
            return self.names[tk]
        except KeyError:
            raise ValueError(f'variável inexistente: {tk}')
 
    def func(self, name, arg):
        fn = self.name(name)
        if callable(fn):
            return fn(arg)
        raise ValueError(f'{fn} não é uma função!')

    def assign(self, name, value):
        self.env[name] = value


transformer = CalcTransformer()
# exemplos = '40 2 +', '3 2 - 1 -', '2 10 4 * +', '4 3 2 ^ ^'
exemplos = "x = 1; x + 1", # "2 * pi", "e^1", "3 + 2i", '3 - 2 - (-1)', '(2 + 10) * 4', '4 ^ 3 ^ 2'

for src in exemplos:
    tree = grammar.parse(src)
    print(src)
    print(tree.pretty())
    print(transformer.transform(tree).pretty())