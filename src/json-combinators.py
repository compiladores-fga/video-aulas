from typing import Tuple, Callable, Any, List

ST = Tuple[int, str]
Parser = Callable[[ST], Tuple[ST, Any]]


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

    return parser


def anyof(parsers: List[Parser]) -> Parser:
    """
    Testa cada parser na lista e retorna o resultado do primeiro parser bem
    sucedido.
    """

    def parser(st: ST) -> Tuple[ST, Any]:
        for parser in parsers:
            try:
                return parser(st)
            except SyntaxError:
                continue

        raise error(st, "all parsers failed")

    return parser


def seq(p1: Parser, p2: Parser) -> Parser:
    """
    Executa dois parsers e retorna o resultado do segundo.
    """

    def parser(st: ST) -> Tuple[ST, Any]:
        st, __ = p1(st)
        st, v2 = p2(st)
        return st, v2

    return parser


def rseq(p1: Parser, p2: Parser) -> Parser:
    """
    Executa dois parsers e retorna o resultado do primeiro.
    """

    def parser(st: ST) -> Tuple[ST, Any]:
        st, v1 = p1(st)
        st, __ = p2(st)
        return st, v1

    return parser


def sep_by(sep: Parser, elem: Parser) -> Parser:
    """
    Lê lista com zero ou mais "elem"s separados por "sep".
    """

    def parser(st: ST) -> Tuple[ST, list]:
        try:
            st, x = elem(st)
        except SyntaxError:
            return st, []

        elems = [x]
        while True:
            try:
                st, _ = sep(st)
            except SyntaxError:
                return st, elems

            st, x = elem(st)
            elems.append(x)

    return parser


def join(parsers: List[Parser]) -> Parser:
    """
    Executa todos parsers agregando o resultado em uma lista.
    """

    def parser(st: ST) -> Tuple[ST, list]:
        results = []
        for parser in parsers:
            st, x = parser(st)
            results.append(x)
        return st, results

    return parser


def map(fn, parser: Parser) -> Parser:
    """
    Aplica a função no resultado obtido pelo parser.
    """
    
    def parser_(st: ST) -> Tuple[ST, list]:
        st, x = parser(st)
        return st, fn(x)

    return parser_


def number(st: ST) -> Tuple[ST, int]:
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


def string(st: ST) -> Tuple[ST, str]:
    """
    Lê uma string.
    """
    pos, src = st
    if src[pos] != '"':
        raise error(st, "not a string!")
    pos_end = src.find('"', pos + 1)
    string = src[pos + 1 : pos_end]
    return (pos_end + 1, src), string


json_options = []
value = anyof(json_options)
true = literal("true", True)
false = literal("false", False)
null = literal("null", None)

elements = sep_by(literal(","), value)
array = rseq(seq(literal("["), elements), literal("]"))

pair = join([rseq(string, literal(":")), value])
pairs = sep_by(literal(","), pair)
object_ = map(dict, rseq(seq(literal("{"), pairs), literal("}")))

json_options.extend([true, false, null, number, string, array, object_])


def loads(text: str) -> object:
    """
    Carrega um documento JSON e retorna o valor Python correspondente.
    """
    st = (0, text)
    return value(st)[1]


# Exemplos
print(loads("true"))
print(loads("false"))
print(loads("null"))
print(loads("42"))
print(loads('"Hello World"'))
print(loads("[true,false,null,[1,2,3,[]]]"))
print(loads('{"answer":[1,2,[]]}'))
