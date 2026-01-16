from typing import Any, List, Optional, Union

from pydantic import BaseModel


class ASTNode(BaseModel):
    class Config:
        arbitrary_types_allowed = True


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
    conditions: List[Union[ComparisonNode, BetweenNode]]


class OrderByItemNode(ASTNode):
    field: FieldNode
    direction: str  # 'ASC' or 'DESC'


class OrderByNode(ASTNode):
    items: List[OrderByItemNode]


class LimitNode(ASTNode):
    value: int


class QueryNode(ASTNode):
    from_clause: FromNode
    where: Optional[WhereNode] = None
    select: SelectNode
    order_by: Optional[OrderByNode] = None
    limit: Optional[LimitNode] = None
