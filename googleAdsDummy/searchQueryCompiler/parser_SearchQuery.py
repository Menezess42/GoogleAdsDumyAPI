from typing import Any, List

from astNodes_SearchQuery import (
    BetweenNode,
    ComparisonNode,
    FieldNode,
    FromNode,
    LimitNode,
    OrderByNode,
    QueryNode,
    SelectNode,
    WhereNode,
)
from lexer_SearchQuery import Lexer, Token, TokenType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

        else:
            self.current_token = Token(TokenType.EOF, None, -1)

    def expect(self, token_type: TokenType):
        if self.current_token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.value}, got {self.current_token.type.value} "
                f"at position {self.current_token.position}"
            )

        value = self.current_token.value
        self.advance()
        return value

    def parse_field(self) -> FieldNode:
        resource = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.DOT)
        field = self.expect(TokenType.IDENTIFIER)
        return FieldNode(resource=resource, field=field)

    def parse_select_list(self) -> List[FieldNode]:
        fields = [self.parse_field()]

        while self.current_token.type == TokenType.COMMA:
            self.advance()
            fields.append(self.parse_field())

        return fields

    def parse_value(self) -> Any:
        if self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.advance()
            return value
        elif self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.advance()
            return value
        else:
            raise SyntaxError(
                f"Expected value at position {self.current_token.position}"
            )

    def parse_condition(self):
        field = self.parse_field()

        if self.current_token.type == TokenType.BETWEEN:
            self.advance()
            lower = self.parse_value()
            self.expect(TokenType.AND)
            upper = self.parse_value()

            return BetweenNode(field=field, lower=lower, upper=upper)

    def parse_where_clause(self) -> WhereNode:
        self.expect(TokenType.WHERE)
        conditions = [self.parse_condition()]

        while self.current_token.type == TokenType.AND:
            self.advance()
            conditions.append(self.parse_condition())

        return WhereNode(conditions=conditions)

    def parse_order_by_clause(self) -> OrderByNode:
        self.expect(TokenType.ORDER_BY)
        order_items = []

        field = self.parse_field()
        ascending = True

        if self.current_token.type == TokenType.ASC:
            self.advance()

        order_items.append((field, ascending))

        while self.current_token.type == TokenType.COMMA:
            self.advance()
            field = self.parse_field()

            if self.current_token.type == TokenType.ASC:
                self.advance()

            order_items.append((field, ascending))

        return OrderByNode(fields=order_items)

    def parse_limit_clause(self) -> LimitNode:
        self.expect(TokenType.LIMIT)
        value = self.expect(TokenType.NUMBER)
        return LimitNode(value=int(value))

    def parse(self) -> QueryNode:
        self.expect(TokenType.SELECT)
        select_node = SelectNode(fields=self.parse_select_list())

        self.expect(TokenType.FROM)
        resource = self.expect(TokenType.IDENTIFIER)
        from_node = FromNode(resource=resource)

        where_node = None
        if self.current_token.type == TokenType.WHERE:
            where_node = self.parse_where_clause()

        order_by_node = None
        if self.current_token.type == TokenType.ORDER_BY:
            order_by_node = self.parse_order_by_clause()

        limit_node = None
        if self.current_token.type == TokenType.LIMIT:
            limit_node = self.parse_limit_clause()

        self.expect(TokenType.EOF)

        return QueryNode(
            select=select_node,
            from_clause=from_node,
            where=where_node,
            order_by=order_by_node,
            limit=limit_node,
        )


def parse_query(query_string: str) -> QueryNode:
    lexer = Lexer(query_string)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
