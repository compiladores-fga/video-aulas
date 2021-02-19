import lark
from lark.visitors import Transformer  # pip3 install lark-parser

# EBNF
grammar = r"""
start    : value

?value   : object
         | array 
         | STRING 
         | NUMBER 
         | "true"   -> true
         | "false"  -> false
         | "null"   -> null

array    : "[" (value ("," value)*)? "]"

object   : "{" (member ("," member)*)? "}"
member   : STRING ":" value

WS       : ("\u0020" | "\u0009" | "\u000A" | "\u000D")+
%ignore WS

NUMBER   : "-"? INTEGER FRACTION? EXPONENT?
INTEGER  : "0"
         | ONENINE DIGIT*
DIGITS   : DIGIT+
DIGIT    : "0" | ONENINE
ONENINE  : "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
FRACTION : "." DIGITS
EXPONENT : ("E" | "e") ("+" | "-")? DIGITS

STRING    : "\"" CHARACTER* "\""
CHARACTER : /[\u0020\u0021]/
          | /[\u0023-\u005b]/
          | /[\u005d-\U0010FFFF]/
          | "\\" ESCAPE
ESCAPE    : "\""
          | "\\"
          | "/"
          | "b"
          | "f"
          | "n"
          | "r"
          | "t"
          | "u" HEX HEX HEX HEX
HEX       : DIGIT
          | /[A-Fa-f]/
"""


class JSONTransformer(lark.Transformer):
    def null(self, children):
        return None

    def false(self, children):
        return False

    def true(self, children):
        return True

    def NUMBER(self, st):
        if '.' not in st and 'e' not in st and 'E' not in st:
            return int(st)
        return float(st)

    def STRING(self, st):
        return eval(st)

    def array(self, children):
        return children

    def object(self, children):
        return dict(children)

    def member(self, children):
        return tuple(children)

    def start(self, children):
        return children[0]

parser = lark.Lark(grammar)


def loads(text: str) -> object:
    """
    Carrega um documento JSON e retorna o valor Python correspondente.
    """
    tree = parser.parse(text)
    transformer = JSONTransformer()
    tree = transformer.transform(tree)
    if hasattr(tree, "pretty"):
        return tree.pretty()
    return tree


# Exemplos
print(loads("true"))
print(loads("false"))
print(loads("null"))
print(loads("42"))
print(loads(r'"Hello\u0020\nWorld"'))
print(loads("[ true , false,null,[1, 2, 3e10, [ ]] ]"))
print(loads('{"x" : 10 , "y" : 3.14}'))
