from typing import Any, List, Optional

from pydantic import BaseModel


class ASTNode(BaseModel):
    pass


class FieldNode(ASTNode):
    resource: str
    field: str


class SelectNode(ASTNode):
    fields: List[FieldNode]


class FromNode(ASTNode):
    resource: str


class ComparisonNode(ASTNode):
    field: FieldNode
    operator: str
    value: Any


class BetweenNode(ASTNode):
    field: FieldNode
    lower: Any
    upper: Any


class WhereNode(ASTNode):
    conditions: List[Any]


class OrderByNode(ASTNode):
    fields: List[tuple]


class LimitNode(ASTNode):
    value: int


class QueryNode(ASTNode):
    select: SelectNode
    from_clause: FromNode
    where: Optional[WhereNode] = None
    order_by: Optional[OrderByNode] = None
    limit: Optional[LimitNode] = None
