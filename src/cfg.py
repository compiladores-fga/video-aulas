from lark import Lark


grammar = Lark(r"""
module  : "\n"* [stm ("\n"+ stm)* "\n"*]

?stm    : assign
        | expr

assign  : VAR "=" expr

?expr   : STRING   -> string
        | VAR      -> var
        | funcall
        | "..."    -> ellipsis

funcall : expr "(" [args] ")"
args    : expr ("," expr)*

VAR     : ("a".."z"|"ç")+
STRING  : "\"" ("a".."z"|"A".."Z"|" ")* "\""

%ignore " "+
""", start="module")

code = """
ç = "Noam Chomsky"
print(ç)
"""

tree = grammar.parse(code)
print(tree.pretty())

