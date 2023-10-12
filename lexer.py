import re


class TokenType:
    def __init__(self, title: str, regexp: str, is_strong: bool = False):
        self.title = title
        self.regexp = regexp
        self.is_strong = is_strong


TOKEN_TYPES = [
    TokenType("IF_STATEMENT", "if", True),
    TokenType("READ", "read", True),
    TokenType("OUTPUT", "output", True),
    TokenType("GOTO", "goto", True),
    TokenType("WHILE_STATEMENT", "while", True),

    TokenType("WHITESPACE", "[ \t]"),
    TokenType("STRING", '^"[а-яА-Яa-zA-Z ]*(")?'),
    TokenType("LABEL", ':[a-z]*'),
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

    def parse_string(self, line: str, char_index: int, line_tokens: list[Token]):
        last_mark = char_index + 1
        for tmp_char_index in range(last_mark, len(line)):
            if line[tmp_char_index] == '"':
                last_mark = tmp_char_index
        line_tokens.append(Token(
            TokenType("STRING", '^"[а-яА-Яa-zA-Z ]*(")?'),
            value=line[char_index:last_mark + 1]
        ))
        return last_mark + 1

    def analyze(self) -> list[list[Token]]:
        tokens = []
        line_index = 0
        for line in self.code.split("\n"):
            if not line:
                continue
            line_tokens = []
            char_index = 0
            while char_index < len(line):
                if line[char_index] == '"':
                    char_index = self.parse_string(line, char_index, line_tokens)
                for token_type in TOKEN_TYPES:
                    tmp_char_index = char_index
                    try:
                        if token_type.is_strong:
                            if re.fullmatch(token_type.regexp, line[char_index:char_index + len(token_type.regexp)]):
                                tmp_char_index = char_index + len(token_type.regexp)
                        else:
                            while re.fullmatch(token_type.regexp, line[char_index:tmp_char_index + 1]) and tmp_char_index < len(line):
                                tmp_char_index += 1
                    except re.error:
                        raise Exception(f"Ошибка")
                    if tmp_char_index != char_index and re.fullmatch(token_type.regexp, line[char_index:tmp_char_index]):
                        if token_type.title != "WHITESPACE":
                            line_tokens.append(Token(token_type, line[char_index:tmp_char_index]))
                            if token_type.title == "LABEL":
                                self.labels[line_tokens[-1].value[1:]] = line_index
                        char_index = tmp_char_index
                        break
            tokens.append(line_tokens)
            line_index += 1
        return tokens



