import re
from enum import Enum
from typing import Any, List


class TokenType(Enum):
    SELECT = "SELECT"
    FROM = "FROM"
    WHERE = "WHERE"
    AND = "AND"
    BETWEEN = "BETWEEN"
    ORDER_BY = "ORDER_BY"
    ASC = "ASC"
    LIMIT = "LIMIT"

    DOT = "DOT"
    COMMA = "COMMA"
    IQUAL = "IQUAL"
    MORE = "MORE"
    LESS = "LESS"
    DASH = "DASH"
    APOSTROPHE = "APOSTROPHE"

    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    EOF = "EOF"


class Token:
    def __init__(self, type: TokenType, value: Any, position: int):
        self.type = type
        self.value = value
        self.position = position


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

        self.keywords = {
            "SELECT": TokenType.SELECT,
            "FROM": TokenType.FROM,
            "WHERE": TokenType.WHERE,
            "AND": TokenType.AND,
            "BETWEEN": TokenType.BETWEEN,
            "ASC": TokenType.ASC,
            "LIMIT": TokenType.LIMIT,
        }

        self.punctuation = {
            ".": TokenType.DOT,
            ",": TokenType.COMMA,
            "=": TokenType.IQUAL,
            ">": TokenType.MORE,
            "<": TokenType.LESS,
            "-": TokenType.DASH,
            "'": TokenType.APOSTROPHE,
        }

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in " \t\n\r":
            self.advance()

    def read_number(self):
        start_pos = self.pos
        num_str = ""

        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()

        if self.current_char == ".":
            num_str += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                num_str += self.current_char
                self.advance()

            return Token(TokenType.NUMBER, float(num_str), start_pos)

    def read_string(self):
        ...
