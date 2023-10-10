from typing import Optional

from lexer import Token


class Parser:
    def __init__(self, tokens: list[list[Token]], context: Optional[dict] = None, labels: Optional[dict] = None):
        self.tokens: list[list[Token]] = tokens
        self.context = context or {}
        self.labels = labels or {}
        self.operators_map = {
            "+": lambda operand1, operand2: operand1 + operand2,
            "-": lambda operand1, operand2: int(operand1 - operand2),
            "~": lambda operand1, operand2: int(operand1 == operand2),
            "!": lambda operand1, operand2: int(operand1 != operand2),
            "%": lambda operand1, operand2: int(operand1 % operand2),
        }

    def eval(self, expression: list[Token], variables: dict) -> int:
        operators = []
        operands = []
        self.parse_expression(expression, variables, operators, operands)
        if not operators:
            return operands[0]
        operands = operands[::-1]
        operators = operators[::-1]

        while len(operands) > 1:
            curr_operator = operators.pop()
            operand1 = operands.pop()
            operand2 = operands.pop()
            operands.append(self.operators_map[curr_operator](operand1, operand2))

        return operands[0]

    def parse_expression(self, expression: list[Token], context: dict, operators: list[str], operands: list[int | str]):
        token_index = 0
        while token_index < len(expression):
            token = expression[token_index]
            match token.type.title:
                case "NUMBER":
                    operands.append(int(token.value))
                case "STRING":
                    operands.append(token.value[1:-1])
                case "PLUS" | "MINUS" | "COMP" | "NEG_COMP" | "MOD":
                    operators.append(token.value)
                case "VARIABLE":
                    operands.append(context[token.value])
                case "READ":
                    operands.append(input())
                case "L_PAR":
                    local_expression = []
                    while expression[token_index + 1].type.title != "R_PAR":
                        token_index += 1
                        local_expression.append(expression[token_index])
                    token_index += 1
                    operands.append(self.eval(local_expression, context))

            token_index += 1

    def find_scope(self, start_line_index: int):
        count_open_bracket = 0
        for line_index in range(start_line_index + 1, len(self.tokens)):
            if count_open_bracket == 0 and self.tokens[line_index][-1].type.title == "R_BRACKET":
                return line_index
            if self.tokens[line_index][-1].type.title == "L_BRACKET":
                count_open_bracket += 1
            if self.tokens[line_index][-1].type.title == "R_BRACKET":
                count_open_bracket -= 1
        raise Exception

    def execute(self):
        line_index = 0
        while line_index != len(self.tokens):
            token_line = self.tokens[line_index]
            if token_line[0].type.title == "VARIABLE":
                self.context[token_line[0].value] = self.eval(token_line[2:], self.context)
            if token_line[0].type.title == "OUTPUT":
                print(self.eval(token_line[1:], self.context))
            if token_line[0].type.title == "IF_STATEMENT":
                if not self.eval(token_line[1:], self.context):
                    line_index = self.find_scope(line_index)
            if token_line[0].type.title == "WHILE_STATEMENT":
                right_bracket_pos = self.find_scope(line_index)
                if self.eval(token_line[1:], self.context):
                    parser = Parser(self.tokens[line_index + 1:right_bracket_pos + 1], self.context)
                    parser.execute()
                    line_index -= 1
                else:
                    line_index = right_bracket_pos
            if token_line[0].type.title == "GOTO":
                line_index = self.labels[token_line[1].value]
            line_index += 1
