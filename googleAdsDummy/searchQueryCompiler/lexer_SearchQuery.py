from enum import Enum
from typing import Any, List

from .token_SearchQuery import Token, TokenType


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
                "DESC": TokenType.DESC,
                "LIMIT": TokenType.LIMIT,
                }

        self.punctuation = {
                ".": TokenType.DOT,
                ",": TokenType.COMMA,
                "=": TokenType.EQUAL,
                ">": TokenType.GREATER,
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

    def peek(self, offset=1):
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in ' \t\n\r':
            self.advance()

    def read_number(self):
        start_pos = self.pos
        num_str = ''

        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()

        if self.current_char == '.':
            num_str += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                num_str += self.current_char
                self.advance()

            return Token(TokenType.NUMBER, float(num_str), start_pos)

        return Token(TokenType.NUMBER, int(num_str), start_pos)

    def read_string(self):
        start_pos = self.pos
        self.advance()

        string_value = ''
        while self.current_char is not None and self.current_char != "'":
            string_value += self.current_char
            self.advance()

        if self.current_char != "'":
            raise SyntaxError(f"Unterminated string at position {start_pos}")

        self.advance()
        return Token(TokenType.STRING, string_value, start_pos)

    def read_identifier(self):
        start_pos = self.pos
        identifier = ''

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()

        if identifier.upper() == 'ORDER':
            saved_pos = self.pos
            self.skip_whitespace()

            if self.current_char is not None and self.current_char.isalpha():
                next_word = ''
                while self.current_char is not None and self.current_char.isalpha():
                    next_word += self.current_char
                    self.advance()

                if next_word.upper() == 'BY':
                    return Token(TokenType.ORDER_BY, 'ORDER_BY', start_pos)
                else:
                    self.pos = saved_pos
                    self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

        upper_identifier = identifier.upper()
        if upper_identifier in self.keywords:
            return Token(self.keywords[upper_identifier], identifier.upper(), start_pos)

        return Token(TokenType.IDENTIFIER, identifier, start_pos)

    def tokenizer(self) -> List[Token]:
        tokens = []
        
        while self.current_char is not None:
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                tokens.append(self.read_number())
                continue

            if self.current_char == "'":
                tokens.append(self.read_number())
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.read_identifier())
                continue
            
            if self.current_char in self.punctuation:
                tokens.append(Token(
                    self.punctuation[self.current_char],
                    self.current_char,
                    self.pos
                    ))
                self.advance()
                continue

            raise SyntaxError(f"Unexpected character '{self.current_char}' at position {self.pos}")

        tokens.append(Token(TokenType.EOF, None, self.pos))
        return tokens
