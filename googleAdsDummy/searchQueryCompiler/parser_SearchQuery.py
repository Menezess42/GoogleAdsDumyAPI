from typing import List, Any, Union
from token_SearchQuery import Token, TokenType
from lexer_SearchQuery import Lexer
from astNodes_SearchQuery import (
        FieldNode, SelectNode, FromNode, ComparisonNode,
        BetweenNode, WhereNode, OrderByNode, OrderByItemNode,
        LimitNode, QueryNode
        )

class Parser:
    def __init__(self, tokens: List[Token]):
        ...

    def advance(self):
        ...

    def expect(self, token_type: TokenType) -> Any:
        ...

    def parser_field(self) -> FieldNode:
        ...

    def parse_select_list(self) -> List[FieldNode]:
        ...

    def parse_value(self) -> Any:
        ...

    def parse_condition(self) -> union[ComparisonNode, BetweenNode]:
        ...

    def parse_condition_list(self) -> List[Union[ComparisonNode, BetweenNode]]:
        ...

    def parse_where_clause(self) -> WhereNode:
        ...

    def parse_order_item(self) -> OrderByItemNode:
        ...

    def parse_order_list(self) -> List[OrderByItemNode]:
        ...

    def parse_order_by_clause(self) -> OrderByItemNode:
        ...


