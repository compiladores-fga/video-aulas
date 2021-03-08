from pprint import pprint
from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    

LEX_SPECIFICATION = {
    "STRING": r'"( |!|[#-[]|[\]-\U0010FFFF]|\\(["\\\/bfnrt]|u[0-9a-zA-Z]{4}))*"',
    "NUMBER": r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-][0-9]+)?',
    "LIT": r'true|false|null',          
    "OP": r'[{}[\],:]',
    "WS": r'\s+',
    "ERROR": r'.',          
}
PATTERN = '|'.join('(?P<%s>%s)' % pair for pair in LEX_SPECIFICATION.items())
REGEX = re.compile(PATTERN)    


def tokenize(src):
    for mo in REGEX.finditer(src):
        kind = mo.lastgroup
        value = mo.group()
        if kind in ('NUMBER', 'STRING'):
            value = eval(value)
        elif kind == 'WS':
            continue
        elif kind == 'ERROR':
            raise SystemError(mo)
        
        yield Token(kind, value)


def lex(src: str) -> list:
    return list(tokenize(src))


# Exemplos
examples = [
    "true",
    "42",
    '"Hello World"',
    "[1, 2, 3]",
    '{ "answer" : 42! }',
]
for doc in examples:
    print('In: ', repr(doc))
    pprint(lex(doc))
    print()
