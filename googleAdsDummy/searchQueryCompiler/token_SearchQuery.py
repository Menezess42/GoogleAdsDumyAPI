# lexer_searchQuery.py
from typing import List, Any
from enum import Enum

class TokenType(Enum):
    # Keyword
    SELECT = "SELECT"
    FROM = "FROM"
    WHERE = "WHERE"
    AND = "AND"
    BETWEEN = "BETWEEN"
    ORDER_BY = "ORDER_BY"
    ASC = "ASC"
    DESC = "DESC"
    LIMIT = "LIMIT"

    # Punctuation
    DOT = "DOT"
    COMMA = "COMMA"
    EQUAL = "EQUAL"
    GREATER = "GREATER"
    LESS = "LESS"
    DASH = "DASH"
    APOSTROPHE = "APOSTROPHE"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Special
    EOF = "EOF"

class Token:
    def __init__(self, type: TokenType, value: Any, position: int):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.position})"
