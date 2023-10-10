import sys

from lexer import Lexer
from parser import Parser

from utils import read_file


lexer = Lexer(read_file("program.vamp"))
parser = Parser(tokens=lexer.analyze(), labels=lexer.labels)
parser.execute()