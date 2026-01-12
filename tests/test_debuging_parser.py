import pytest
from googleAdsDummy.searchQueryCompiler.astNodes_SearchQuery import (
    BetweenNode,
    ComparisonNode,
    QueryNode,
)
from googleAdsDummy.searchQueryCompiler.parser_SearchQuery import parse_query

# First test to fail the unity test from the test_parser.py
def test_where_and_limit():
    """WHERE + LIMIT"""
    query = """
    SELECT campaign.id FROM campaign
    WHERE campaign.status = 'ENABLED'
    LIMIT 50
    """
    ast = parse_query(query)

    assert ast.where is not None
    assert ast.limit is not None
    assert ast.order_by is None
