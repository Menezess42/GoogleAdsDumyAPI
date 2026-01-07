from typing import Any, List, Union

from astNodes_SearchQuery import (
    BetweenNode,
    ComparisonNode,
    FieldNode,
    FromNode,
    LimitNode,
    OrderByItemNode,
    OrderByNode,
    QueryNode,
    SelectNode,
    WhereNode,
)
from lexer_SearchQuery import Lexer
from token_SearchQuery import Token, TokenType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = (
            self.tokens[0] if tokens else Token(TokenType.EOF, None, -1)
        )

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, None, -1)

    def expect(self, token_type: TokenType) -> Any:
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
                f"Expected value (string or number) at position {self.current_token.position}"
            )

    def parse_condition(self) -> Union[ComparisonNode, BetweenNode]:
        field = self.parse_field()

        if self.current_token.type == TokenType.BETWEEN:
            self.advance()
            lower = self.parse_value()
            self.expect(TokenType.AND)
            upper = self.parse_value()
            return BetweenNode(field=field, lower=lower, upper=upper)

        elif self.current_token.type in [
            TokenType.EQUAL,
            TokenType.GREATER,
            TokenType.LESS,
        ]:
            operator = self.current_token.value
            self.advance()
            value = self.parse_value()
            return ComparisonNode(field=field, operator=operator, value=value)

        else:
            raise SyntaxError(
                f"Expected comparison operator (=, >, <, BETWEEN) at position {self.current_token.position}"
            )

    def parse_condition_list(self) -> List[Union[ComparisonNode, BetweenNode]]:
        conditions = [self.parse_condition()]

        while self.current_token.type == TokenType.AND:
            self.advance()
            conditions.append(self.parse_condition())

        return conditions

    def parse_where_clause(self) -> WhereNode:
        self.expect(TokenType.WHERE)
        conditions = self.parse_condition_list()

        return WhereNode(conditions=conditions)

    def parse_order_item(self) -> OrderByItemNode:
        field = self.parse_field()
        direction = "ASC"

        if self.current_token.type == TokenType.ASC:
            direction = "ASC"
            self.advance()
        elif self.current_token.type == TokenType.DESC:
            direction = "DESC"
            self.advance()

        return OrderByItemNode(field=field, direction=direction)

    def parse_order_list(self) -> List[OrderByItemNode]:
        items = [self.parse_order_item()]

        while self.current_token.type == TokenType.COMMA:
            self.advance()
            items.append(self.parse_order_item())

        return items

    def parse_order_by_clause(self) -> OrderByNode:
        self.expect(TokenType.ORDER_BY)
        items = self.parse_order_list()
        return OrderByNode(items=items)

    def parse_limit_clause(self) -> LimitNode:
        self.expect(TokenType.LIMIT)
        value = self.expect(TokenType.NUMBER)

        if not isinstance(value, int):
            raise SyntaxError(
                f"LIMIT value must be an integer, got {type(value).__name__}"
            )

        return LimitNode(value=value)

    def parse(self) -> QueryNode:
        self.expect(TokenType.SELECT)
        select_node = SelectNode(fields=self.parse_select_list())

        self.expect(TokenType.FROM)
        resource = self.expect(TokenType.IDENTIFIER)
        from_node = FromNode(resource=resource)

        where_node = None
        order_by_node = None
        limit_node = None

        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.WHERE:
                if where_node is not None:
                    raise SyntaxError(
                        f"Duplicate WHERE clause at position {self.current_token.position}"
                    )

                where_node = self.parse_where_clause()

            elif self.current_token.type == TokenType.ORDER_BY:
                if order_by_node is not None:
                    raise SyntaxError(
                        f"Duplicate ORDER BY clause at position {self.current_token.position}"
                    )
                order_by_node = self.parse_order_by_clause()

            elif self.current_token.type == TokenType.LIMIT:
                if limit_node is not None:
                    raise SyntaxError(
                        f"Duplicate LIMIT clause at position {self.current_token.position}"
                    )
                limit_node = self.parse_limit_clause()

            else:
                raise SyntaxError(
                    f"Unexpected token {self.current_token.type.value} at position {self.current_token.position}"
                )

        return QueryNode(
            select=select_node,
            from_clause=from_node,
            where=where_node,
            order_by=order_by_node,
            limit=limit_node,
        )


def parse_query(query_string: str) -> QueryNode:
    lexer = Lexer(query_string)
    tokens = lexer.tokenizer()
    parser = Parser(tokens)
    return parser.parse()
