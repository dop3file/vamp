import re


class TokenType:
    def __init__(self, title: str, regexp: str):
        self.title = title
        self.regexp = regexp


TOKEN_TYPES = [
    TokenType("IF_STATEMENT", "^i(f)?$"),
    TokenType("WHITESPACE", "[ \t]"),
    TokenType("READ", "^r(e(a(d)?)?)?$"),
    TokenType("OUTPUT", r"^o(u(t(p(u(t)?)?)?)?)?$"),
    TokenType("STRING", '^"[а-яА-Яa-zA-Z ]*(")?'),
    TokenType("WHILE_STATEMENT", "^w(h(i(l(e)?)?)?)?$"),
    TokenType("LABEL", ':[a-z]*'),
    TokenType("GOTO", "^g(o(t(o)?)?)?$"),
    TokenType("VARIABLE", "[a-z]*"),
    TokenType("NUMBER", "[0-9]*"),
    TokenType("EQUAL", "\\="),
    TokenType("PLUS", "\\+"),
    TokenType("MINUS", "\\-"),
    TokenType("L_PAR", "\\("),
    TokenType("R_PAR", "\\)"),
    TokenType("COMP", "~"),
    TokenType("NEG_COMP", "!"),
    TokenType("L_BRACKET", "{"),
    TokenType("R_BRACKET", "}"),
    TokenType("MOD", "%")
]


class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type.title} {self.value}"


class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.labels = {}

    def analyze(self) -> list[list[Token]]:
        tokens = []
        line_index = 0
        for line in self.code.split("\n"):
            if not line:
                continue
            line_tokens = []
            char_index = 0
            while char_index < len(line):
                for token_type in TOKEN_TYPES:
                    tmp_char_index = char_index
                    try:
                        while re.fullmatch(token_type.regexp, line[char_index:tmp_char_index + 1]) and tmp_char_index < len(line):
                            tmp_char_index += 1
                    except re.error:
                        raise Exception(f"Ошибка")
                    if tmp_char_index != char_index:
                        if token_type.title != "WHITESPACE":
                            line_tokens.append(Token(token_type, line[char_index:tmp_char_index]))
                            if token_type.title == "LABEL":
                                self.labels[line_tokens[-1].value[1:]] = line_index
                        char_index = tmp_char_index
                        break
            tokens.append(line_tokens)
            line_index += 1
        return tokens



