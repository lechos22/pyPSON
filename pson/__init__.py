from typing import Any, Pattern, Iterator, Match

Dumpable = None | float | int | str | dict | list | tuple | set


class Lexer:
    import re
    RE_ANY: Pattern[str] = re.compile(
        r'(-)'  # UN_MIN
        r'|(=)'  # EQ
        r'|(\()'  # L_RND
        r'|(\))'  # R_RND
        r'|(\[)'  # L_SQ
        r'|(\])'  # R_SQ
        r'|(null)'  # NUL
        r'|([0-9]+\.[0-9]+)|(inf)|(nan)'  # FP
        r'|(0b[01]+)'  # INT(binary)
        r'|(0o[0-7]+)'  # INT(octal)
        r'|([0-9]+)'  # INT(decimal)
        r'|(0x[0-9a-fA-F]+)'  # INT(hexadecimal)
        r'|([a-zA-Z_]\w*)'  # NUC_ID | UC_ID
        r'|(\"(.*?[^\\])?\")'  # STR
    )

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        import re
        self.re_iter: Iterator[Match[str]] = re.finditer(Lexer.RE_ANY, self.src)
        return self

    def __next__(self) -> tuple[str, Any]:
        from math import nan, inf
        el: str = next(self.re_iter).group()
        if el == '-':
            return 'UN_MIN', None
        elif el == '(':
            return 'L_RND', None
        elif el == ')':
            return 'R_RND', None
        elif el == '[':
            return 'L_SQ', None
        elif el == ']':
            return 'R_SQ', None
        elif el == '=':
            return 'EQ', None
        elif el == 'null':
            return 'NUL', None
        elif el == 'inf':
            return 'FP', inf
        elif el == 'nan':
            return 'FP', nan
        elif el[0] == '"':
            return 'STR', el[1:-1]
        elif el.startswith('0b'):
            return 'INT', int(el[2:], 2)
        elif el.startswith('0o'):
            return 'INT', int(el[2:], 8)
        elif el.startswith('0x'):
            return 'INT', int(el[2:], 16)
        elif el[0].isnumeric():
            return ('FP', float(el)) if '.' in el else ('INT', int(el))
        elif el[0].isalpha():
            return ('UC_ID', el) if el == el.upper() else ('NUC_ID', el)
        else:
            raise Exception

    def __init__(self, src: str):
        self.src: str = src


class Parser:
    def reduce(self) -> bool:
        length: int = len(self.buf)
        if length >= 1 and self.buf[-1][0] == 'L_SQ':  # array -> L_SQ
            self.buf[-1] = 'array', []
        elif length >= 2 and self.buf[-2][0] == 'array' and self.buf[-1][0] == 'object':  # array -> array object
            self.buf[-2][1].append(self.buf[-1][1])
            del self.buf[-1]
        elif length >= 2 and self.buf[-2][0] == 'array' and self.buf[-1][0] == 'R_SQ':  # object -> array R_SQ
            self.buf[-2] = 'object', self.buf[-2][1]
            del self.buf[-1]
        elif length >= 1 and self.buf[-1][0] == 'L_RND':  # array -> L_SQ
            self.buf[-1] = 'map', {}
        elif (length >= 4 and self.buf[-4][0] == 'map' and self.buf[-3][0] == 'NUC_ID'
              and self.buf[-2][0] == 'EQ' and self.buf[-1][0] == 'object'):  # map -> map NUC_ID EQ object
            self.buf[-4][1][self.buf[-3][1]] = self.buf[-1][1]
            del self.buf[-3:]
        elif length >= 2 and self.buf[-2][0] == 'map' and self.buf[-1][0] == 'R_RND':  # object -> map R_RND
            self.buf[-2] = 'object', self.buf[-2][1]
            del self.buf[-1]
        elif length >= 2 and self.buf[-2][0] == 'UN_MIN' and self.buf[-1][0] == 'object':  # object -> UN_MIN object
            del self.buf[-2]
            self.buf[-1] = self.buf[-1][0], -self.buf[-1][1]
        elif length >= 1 and self.buf[-1][0] == 'STR':  # object -> STR
            self.buf[-1] = 'object', self.buf[-1][1]
        elif length >= 1 and self.buf[-1][0] == 'INT':  # object -> INT
            self.buf[-1] = 'object', self.buf[-1][1]
        elif length >= 1 and self.buf[-1][0] == 'UC_ID':  # object -> UC_ID
            self.buf[-1] = 'object', self.buf[-1][1]
        elif length >= 1 and self.buf[-1][0] == 'FP':  # object -> FP
            self.buf[-1] = 'object', self.buf[-1][1]
        elif length >= 1 and self.buf[-1][0] == 'NUL':  # object -> NUL
            self.buf[-1] = 'object', None
        else:
            return False
        return True

    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer
        self.buf: list[tuple[str, Any]] = []
        for t, v in self.lexer:
            self.buf.append((t, v))
            while self.reduce():
                pass
        self.result: Dumpable = self.buf[0][1] if self.buf else None
        del self.buf


class Dumper:
    @staticmethod
    def escape(s: str) -> str:
        return s.encode('unicode-escape').decode()

    @staticmethod
    def dumps(o: Dumpable) -> str:
        t = type(o)
        if o is None:
            return 'null'
        elif t in (float, int):
            return str(o)
        elif t is str:
            return f'"{Dumper.escape(o)}"'
        elif t in (list, tuple, set):
            return f'[{" ".join([Dumper.dumps(i) for i in o])}]'
        elif t is dict:
            return f'({" ".join([k + "=" + Dumper.dumps(v) for k, v in o.items()])})'


def loads(s: str) -> Any:
    ll = Lexer(s)
    yy = Parser(ll)
    return yy.result


dumps: type(Dumper.dumps) = Dumper.dumps
