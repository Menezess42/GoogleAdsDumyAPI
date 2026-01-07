import pytest
from ..googleAdsDummy.searchQueryCompiler.parser_SearchQuery import parse_query 
from ..googleAdsDummy.searchQueryCompiler.astNodes_SearchQuery import (
        QueryNode, SelectNode, FromNode, WhereNode, OrderByNode, LimitNode, FieldNode, ComparisonNode, BetweenNode, OrderByItemNode)

class TestBasicQueries:
    """Testes para queries básicas e mínimas"""

    def test_minimal_query(self):
        """Query Minima: apenas SELECT e FROM"""
        query = "SELECT campaign.id FROm campaign"
        ast = parse_query(query)

        assert isinstance(ast, QueryNode)
        assert len(ast.select.fields) == 1
        assert ast.select.fields[0].resource == "campaign"
        assert ast.from_clause.resource == "campaign"
        assert ast.where is None
        assert ast.order_by is None
        assert ast.limit is None

    def test_multiple_fields(self):
        """Query com múltiplos campos no SELECT"""
        query = "SELECT campaign.id, campaign.name, campaign.status FROM campaign"
        ast = parse_query(query)

        assert len(ast.select.fields) == 3
        assert ast.select.fields[0].field == "id"
        assert ast.select.fields[1].field == "name"
        assert ast.select.fields[2].field == "status"

    def test_whitespace_handling(self):
        """Query com vários tipos de whitespace"""
        query = """
        SELECT campaign.id, campaign.name
        FROM campaign
        """
        ast = parse_query(query)

        assert len(ast.select.fields) == 2
        assert ast.from_clause.resource == "campaign"


class testWhereClause:
    """Testes para cláusulas WHERE"""

    def test_simple_where_equal(self):
        """WHERE com operador de igualdade"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.status = 'ENABLED'"
        ast = parse_query(query)

        assert ast.where is not None
        assert len(ast.where.conditions) == 1
        assert isinstance(ast.where.conditions[0], ComparisonNode)
        assert ast.where.conditions[0].operator == "="
        assert ast.where.conditions[0].value == "ENABLED"

    def test_where_greater_than(self):
        """WHERE com operador maior que"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.budget > 1000"
        ast = parse_query(query)

        assert ast.where.conditions[0].operator == ">"
        assert ast.where.conditions[0].value == 1000

    def test_where_less_than(self):
        """WHERE com operador menor que"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.budget < 5000"
        ast = parse_query(query)

        assert ast.where.conditions[0].operator == "<"
        assert ast.where.conditions[0].value == 5000
