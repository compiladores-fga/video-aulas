import lark
from lark.visitors import Transformer  # pip3 install lark-parser

# EBNF
grammar = r"""
start  : value

?value : "true"   -> true
       | "false"  -> false
       | "null"   -> null
       | array 
       | object
       | NUMBER 
       | STRING 

array  : "[" (value ("," value)*)? "]"

object : "{" (pair ("," pair)*)? "}"
pair   : STRING ":" value

%import common.ESCAPED_STRING -> STRING
%import common.SIGNED_NUMBER  -> NUMBER
"""


class JSONTransformer(lark.Transformer):
    def null(self, children):
        return None

    def false(self, children):
        return False

    def true(self, children):
        return True

    def NUMBER(self, st):
        return int(st)

    def STRING(self, st):
        return st[1:-1]

    def array(self, children):
        return children

    def object(self, children):
        return dict(children)

    def pair(self, children):
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
print(loads('"Hello World"'))
print(loads("[true,false,null,[1,2,3,[]]]"))
print(loads('{"answer":[1,2,[]]}'))
