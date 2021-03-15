import math
from random import random
from lark import Lark
from lark.visitors import Interpreter, v_args
import operator

grammar = Lark(
    r"""
?start  : block

?block  : expr (";" expr)* ";"?

?expr   : cond
        | assign

?assign : NAME "=" expr
        
?cond   : "if" or_ "then" or_ "else" cond
        | or_

?or_    : or_ "or" and_
        | and_

?and_   : and_ "and" not_
        | not_

?not_   : "not" cmp      -> not_
        | cmp

?cmp    : sum ">" sum    -> gt
        | sum "<" sum    -> lt 
        | sum ">=" sum   -> ge
        | sum "<=" sum   -> le
        | sum "==" sum   -> eq
        | sum "!=" sum   -> ne
        | sum

?sum    : sum "+" mul    -> add 
        | sum "-" mul    -> sub
        | mul

?mul    : mul "*" pow    -> mul     
        | mul "/" pow    -> div     
        | pow

?pow    : unary "^" pow  -> pow     
        | unary

?unary  : "-" atom       -> neg 
        | "+" atom       -> pos
        | atom

?atom   : INT                -> int
        | NAME               -> var
        | NAME "(" args ")"  -> funcall
        | "(" expr ")"

args    : [expr ("," expr)*]

INT     : ("0".."9")+
NAME    : ("a".."z"|"_")+

%ignore " "
""", parser='lalr')

def make_binop(fn):
    def binop(self, x, y):
        return fn(self.visit(x), self.visit(y))
    return binop 


@v_args(inline=True)
class CalcEval(Interpreter):
    GLOBAL_VARIABLES = {
        "pi": math.pi,
        "e": math.e,
        "rand": random,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "ln": math.log,
    }
    add = make_binop(operator.add) 
    sub = make_binop(operator.sub) 
    mul = make_binop(operator.mul) 
    div = make_binop(operator.truediv) 
    pow = make_binop(operator.pow) 
    neg = make_binop(operator.neg) 
    pos = make_binop(operator.pos)
    gt = make_binop(operator.gt) 
    lt = make_binop(operator.lt) 
    ge = make_binop(operator.ge) 
    le = make_binop(operator.le) 
    eq = make_binop(operator.eq) 
    ne = make_binop(operator.ne)
    and_ = make_binop(operator.and_) 
    or_ = make_binop(operator.or_)
    int = int 

    def __init__(self, env):
        self.env = env
        self.env.update(self.GLOBAL_VARIABLES)
        super().__init__()

    def not_(self, x):
        return not self.visit(x)
    
    def pi(self):
        return math.pi 

    def cond(self, cond, then, other):
        if self.visit(cond):
            return self.visit(then)
        else:
            return self.visit(other)

    def var(self, name):
        return self.env[name]

    def funcall(self, name, args):
        fn = self.var(name)
        return fn(*self.visit(args))

    @v_args(inline=False)
    def args(self, tree):
        return self.visit_children(tree)

    def assign(self, name, value):
        self.env[str(name)] = res = self.visit(value)
        return res

    @v_args(inline=False)
    def block(self, tree):
        return self.visit_children(tree)[-1]


exemplos = [
    'x = y = 21; x + y',
    'x = 1; loop 5 x = 2 * x; x',
    'cos(pi) + ln(e)',
    'if pi > 3 then 4 else 3 / 0',
    '3 - 2 - 1', 
    '(2 + 10) * 4', 
    '4 ^ 3 ^ 2',
]

def eval(src: str, env: dict = None) -> object:
    if env is None:
        env = {}

    ast = grammar.parse(src)
    ctx = CalcEval(env)
    return ctx.visit(ast)


print("EXEMPLOS!")
for src in exemplos:
    print('In: ', src)
    print('Out:', eval(src), end='\n\n')