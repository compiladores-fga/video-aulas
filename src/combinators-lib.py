from typing import Tuple, Callable, Any, List, Union

ST = Tuple[int, str]
AnyParser = Union["Parser", str]


class Parser:
    """
    Objeto responsável por ler um padrão de texto com uma chamada ao método
    Parser.parse().
    """

    def __init__(self, func: Callable[[ST], Tuple[ST, Any]]):
        self.function = func

    def __or__(self, other: AnyParser):
        # self | other
        return anyof([self, as_parser(other)])

    def __rshift__(self, other: AnyParser) -> "Parser":
        """
        Executa dois parsers e retorna o resultado do segundo: self >> other
        """

        second = as_parser(other)

        def parser(st: ST) -> Tuple[ST, Any]:
            st, __ = self.parse(st)
            st, v2 = second.parse(st)
            return st, v2

        return Parser(parser)

    def __rrshift__(self, other):
        # other >> self
        return as_parser(other) >> self

    def __lshift__(self, other: AnyParser) -> "Parser":
        """
        Executa dois parsers e retorna o resultado do primeiro: self << other
        """

        second = as_parser(other)

        def parser(st: ST) -> Tuple[ST, Any]:
            st, v1 = self.parse(st)
            st, __ = second.parse(st)
            return st, v1

        return Parser(parser)

    def __rlshift__(self, other):
        # other << self
        return as_parser(other) << self

    def __matmul__(self, other: Callable):
        # self @ other
        return self.map(other)

    def __rmatmul__(self, other: Callable):
        # other @ self
        return self.map(other)

    def sep_by(self, sep: AnyParser) -> "Parser":
        """
        Lê lista com zero ou mais "elem"s separados por "sep".
        """

        sep_parser = as_parser(sep)

        def parser(st: ST) -> Tuple[ST, list]:
            try:
                st, x = self.parse(st)
            except SyntaxError:
                return st, []

            elems = [x]
            while True:
                try:
                    st, _ = sep_parser.parse(st)
                except SyntaxError:
                    return st, elems

                st, x = self.parse(st)
                elems.append(x)

        return Parser(parser)

    def map(self, fn: Callable) -> "Parser":
        """
        Aplica a função no resultado obtido pelo parser.
        """

        def parser(st: ST) -> Tuple[ST, list]:
            st, x = self.parse(st)
            return st, fn(x)

        return Parser(parser)

    def parse(self, st: ST) -> Tuple[ST, Any]:
        """
        Executa parser a partir do estado fornecido e retorna uma tupla com o
        novo estado e o valor lido.
        """
        return self.function(st)


def as_parser(obj: AnyParser) -> Parser:
    if isinstance(obj, Parser):
        return obj
    elif isinstance(obj, str):
        return literal(obj)
    else:
        raise TypeError


def error(st, msg):
    return SyntaxError(msg)


def literal(lit: str, value=None) -> Parser:
    """
    Lê um valor literal "lit" e retorna "value" se bem sucedido
    """

    def parser(st: ST) -> Tuple[ST, Any]:
        pos, src = st

        if src.startswith(lit, pos):
            st = (pos + len(lit), src)
            return st, value
        else:
            raise error(st, f"expect {lit!r}!")

    return Parser(parser)


def anyof(parsers: List[Parser]) -> Parser:
    """
    Testa cada parser na lista e retorna o resultado do primeiro parser bem
    sucedido.
    """

    def parser(st: ST) -> Tuple[ST, Any]:
        for parser in parsers:
            try:
                return parser.parse(st)
            except SyntaxError:
                continue

        raise error(st, "all parsers failed")

    return Parser(parser)


def join(parsers: List[Parser]) -> Parser:
    """
    Executa todos parsers agregando o resultado em uma lista.
    """

    def parser(st: ST) -> Tuple[ST, list]:
        results = []
        for parser in parsers:
            st, x = parser.parse(st)
            results.append(x)
        return st, results

    return Parser(parser)


def read_number(st: ST) -> Tuple[ST, int]:
    """
    Lê um número.
    """
    pos, src = st
    pos_end = pos
    while pos_end < len(src) and src[pos_end].isdigit():
        pos_end += 1
    if pos == pos_end:
        raise error(st, "not a number")
    n = int(src[pos:pos_end])
    return (pos_end, src), n


def read_string(st: ST) -> Tuple[ST, str]:
    """
    Lê uma string.
    """
    pos, src = st
    if src[pos] != '"':
        raise error(st, "not a string!")
    pos_end = src.find('"', pos + 1)
    string = src[pos + 1 : pos_end]
    return (pos_end + 1, src), string


number = Parser(read_number)
string = Parser(read_string)

json_options = []
value = anyof(json_options)
true = literal("true", True)
false = literal("false", False)
null = literal("null", None)

elements = value.sep_by(",")
array = "[" >> elements << "]"

pair = join([string << ":", value])
pairs = pair.sep_by(",")
object_ = dict @ ("{" >> pairs << "}")

json_options.extend([true, false, null, number, string, array, object_])


def loads(text: str) -> object:
    """
    Carrega um documento JSON e retorna o valor Python correspondente.
    """
    st = (0, text)
    return value.parse(st)[1]


# Exemplos
print(loads("true"))
print(loads("false"))
print(loads("null"))
print(loads("42"))
print(loads('"Hello World"'))
print(loads("[true,false,null,[1,2,3,[]]]"))
print(loads('{"answer":[1,2,[]]}'))
