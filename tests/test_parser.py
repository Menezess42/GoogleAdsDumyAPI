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

    def test_where_multiple_conditions(self):
        """WHERE com múltiplas condições (AND)"""
        query = """
        SELECT campaign.id FROM campaign
        WHERE campaign.status = 'ENABLED'
        AND campaign.budget > 1000
        AND campaign.type = 'SEARCH'
        """
        ast = parse_query(query)

        assert len(ast.where.conditions) == 3
        assert ast.where.conditions[0]A.value == "ENABLED"
        assert ast.where.conditions[1].value == 1000
        assert ast.where.conditions[2].value == "SEARCH"

    def test_where_between_with_floats(self):
        """WHERE BETWEEN com números decimais"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.ctr BETWEEN 0.5 AND 2.5"
        
        ast = parse_query(query)

        assert ast.where.conditions[0].lower == 0.5
        assert ast.where.conditions[0].upper == 2.5

    def test_where_mixed_conditions(self):
        """WHERE com condições mistas (comparação e BETWEEN)"""
        query = """
        SELECT campaign.id FROM campaign
        WHERE campaign.status = 'ENABLED'
        AND campaign.budget BETWEEN 1000 AND 5000
        """
        ast = parse_query(query)

        assert len(ast.where.conditions) == 2
        assert isinstance(ast.where.conditions[0], ComparisonNode)
        assert isinstance(ast.where.conditions[1], BetweenNode)
        

class TestOrderByClause:
    """Testes para cláusulas ORDER BY"""

    def test_order_by_default_asc(self):
        """ORDER BY sem especificar direção (padrão ASC)"""
        query = "SELECT campaign.id FROM campaign ORDER BY campaign.name"
        ast = parse_query(query)

        assert ast.order_by is not None
        assert len(ast.order_by.items) == 1
        assert ast.order_by.items[0].field.field == "name"
        assert ast.order_by.items[0].direction == "ASC"

    def test_order_by_explicit_asc(self):
        """ORDER BY com ASC explícito"""
        query = "SELECT campaign.id FROM campaign ORDER BY campaign.name ASC"
        ast = parse_query(query)

        assert ast.order_by.items[0].direction == "ASC"

    def test_order_by_desc(self):
        """ORDER BY com DESC"""
        query = "SELECT campaign.id FROM campaign ORDER BY campaign.budget DESC"
        ast = parse_query(query)

        assert ast.order_by.items[0].direction == "DESC"

    def test_order_by_multiple_fields(self):
        """ORDER BY com múltiplos campos"""
        query = """
        SELECT campaign.id FROM campaign
        ORDER BY campaign.name ASC, campaign.budget DESC, campaign.id
        """
        ast = parse_query(query)

        assert len(ast.order_by.items) == 3
        assert ast.order_by.items[0].direction == "ASC"
        assert ast.order_by.items[1].direction == "DESC"
        assert ast.order_by.items[2].direction == "ASC"

class TestLimitClause:
    """Testes par cláusulas LIMIT"""

    def test_limit_simple(self):
        """LIMIT com valor inteiro"""
        query = "SELECT campaign.id FROM campaign LIMIT 10"
        ast = parse_query(query)

        assert ast.limit is not None
        assert ast.limit.value == 10

    def test_limit_large_number(self):
        """LIMIT com número grande"""
        query = "SELECT campaign.id FROM campaign LIMIT 10000"
        ast = parse_query(query)

        assert ast.limit.value == 10000

class TestCombinedClauses:
    """Testes para queries com múltiplas cláusulas combinadas"""

    def test_where_and_limit(self):
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

    def test_where_and_order_by(self):
        """WHERE + ORDER BY"""
        query = """
        SELECT campaign.id FROM campaign
        WHERE campaign.budget > 1000
        ORDER BY campaign.name DESC
        """
        ast = parse_query(query)

        assert ast.where is not None
        assert ast.order_by is not None
        assert ast.limit is None

    def test_order_by_and_limit(self):
        """ORDER BY + LIMIT"""
        query = """
        SELECT campaign.id FROM campaign
        ORDER BY campaign.budget DESC
        LIMIT 20
        """
        ast = parse_query(query)

        assert ast.where is None
        assert ast.order_by is not None
        assert ast.limit is not None

    def test_all_clauses(self):
        """Query completa com todas as claúsulas"""
        query = """
        SELECT campaign.id, campaign.name, campaign.budget
        FROM campaign
        WHERE campaign.status = 'ENABLED'
        AND campaign.budget BETWEEN 1000 AND 10000
        ORDER BY campaign.budget DESC, campaign.name ASC
        LIMIT 100
        """
        ast = parse_query(query)

        assert len(ast.select.fields) == 3
        assert ast.from_clause.resource == "campaign"
        assert ast.where is not None
        assert len(ast.where.conditions) == 2
        assert ast.order_by is not None
        assert len(ast.order_by.items) == 2
        assert ast.limit is not None
        assert ast.limit.value == 100

    def test_clauses_different_order(self):
        """Cláusulas em ordem diferente (LIMIT antes de ORDER BY)"""
        query = """
        SELECT campaign.id FROM campaign
        WHERE campaign.status = 'ENABLED'
        LIMIT 50
        ORDER BY campaign.name ASC
        """

        ast = parse_query(query)

        assert ast.where is not None
        assert ast.order_by is not None
        assert ast.limit is not None

class TesetIdentifiers:
    """Testes para identificadores e nomes"""

    def test_identifiers_with_underscores(self):
        """identificadores com underscores"""
        query = "SELECT ad_group.campaign_id FROM ad_group"
        ast = parse_query(query)

        assert ast.select.fields[0].resource == "ad_group"
        assert ast.select.fields[0].field == "campaign_id"
        assert ast.from_clause.resource == "ad_group"

    def test_identifiers_with_numbers(self):
        """Identificadores com números"""
        query = "SELECT resource123.field456 FROM resource123"
        ast = parse_query(query)

        assert ast.select.fields[0]

        assert ast.select.fields[0].resource == "resource123"
        assert ast.select.fields[0].field == "field456"

class TestStringValues:
    """Testes para valores string"""

    def test_string_with_spaces(self):
        """String com espaços"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.name = 'My Campaign'"
        ast = parse_query(query)

        assert ast.where.conditions[0].value == "My Campaign"

    def test_string_with_numbers(self):
        """string com números"""
            query = "SELECT campaign.id FROM campaign WHERE campaign.code = '12345'"
            ast = parse_query(query)

            assert ast.where.conditions[0].value == "12345"

    def test_string_with_numbers(self):
        """string com hífen"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.name = 'test-campaign'"
        ast = parse_query(query)

        assert ast.where.conditions[0].value == "test-campaign"

class TestNumberValues:
    """Testes para valores numéricos"""

    def test_integer_values(self):
        """Valores inteiros"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.budget = 1000"
        ast = parse_query(query)

        assert ast.where.conditions[0].value == 1000
        assert isinstance(ast.where.conditions[0].value, int)

    def test_float_values(self):
        """Valores dcimais"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.ctr = 1.5"
        ast = parse_query(query)

        assert ast.where.conditions[0].value == 1.5
        assert isinstance(ast.where.conditions[0].value, flaot)

    def test_zero_values(self):
        """valor zero"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.cost = 0"
        ast = parse_query(query)

        assert ast.where.conditions[0].value == 0

class TestErrorCases:
    """Testes para casos de erros que devem falhar"""

    def test_missing_from(self):
        """Query sem FROM deve falhar"""
        query = "SELECT campaign.id"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_missing_select(self):
        """Query sem SELECT deve falhar"""
        query = "FROM campaign"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_missing_field_after_comma(self):
        """Vírgula sem campo após ela deve falhar"""
        query = "SELECT campaign.id, FROM campaign"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_missing_dot_in_field(self):
        """Campo sem ponto (resource.field) deve falhar"""
        query = "SELECT campaign FROM campaign"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_unterminated_string(self):
        """String não terminada deve falhar"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.name = 'test"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_invalid_operator(self):
        """Operador inválido deve falhar"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.budget != 1000"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_where_without_conditions(self):
        """WHERE sem condição deve falhar"""
        query = "SELECT campaign.id FROM campaign WHERE"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_order_by_without_field(self):
        """ORDER BY sem campo deve falhar"""
        query = "SELECT campaign.id FROM campaign ORDER BY"
        with pytest.raises(SyntaxError):
            parse_query(query)
    
    def test_limit_without_number(self):
        """LIMIT sem número deve falhar"""
        query = "SELECT campaign.id FROM campaign LIMIT"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_limit_with_float(self):
        """LIMIT com decimal deve falhar"""
        query = "SELECT campaign.id FROM campaign LIMIT 10.5"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_between_without_and(self):
        """BETWEEN sem AND deve falhar"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.budget BETWEEN 1000"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_duplicate_where(self):
        """múltiplas cláusulas WHERE devem falhar"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.status = 'ENABLED' WHERE campaign.budget > 1000"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_duplicate_order_by(self):
        """múltiplas cláusulas ORDER BY devem falhar"""
        query = "SELECT campaign.id FROM campaign ORDER BY campaign.name ORDER BY campaign.budget"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_duplicate_limit(self):
        """múltiplas cláusulas LIMIT devem falhar"""
        query = "SELECT campaign.id FROM campaign LIMIT 10 LIMIT 20"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_unexpected_token_after_query(self):
        """Token inesperado após query completa deve falhar"""
        query = "SELECT campaign.id FROM campaign LIMIT 10 EXTRA"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_invalid_character(self):
        """Caractere inválido deve falhar"""
        query = "SELECT campaign.id FROM campaign WHERE campaign.name = 'test' @ campaign.budget > 1000"
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_empty_query(self):
        """Query vazia deve falhar"""
        query = ""
        with pytest.raises(SyntaxError):
            parse_query(query)

    def test_only_whitespace(self):
        """query só com whitespace deve falhar"""
        query = " \n\t "
        with pytest.raises(SyntaxError):
            parse_query(query)


class TestCaseInsensitivity:
    """Testes para verificar case insensitivity das keywords"""

    def test_lowercase_keywords(self):
        """Keywords em minúsculo"""
        query = "select campaign.id from campaign where campaign.status = 'ENABLED' order by campaign.name limit 10"
        ast = parse_query(query)

        assert ast is not None
        assert ast.where is not None
        assert ast.order_by is not None
        assert ast.limit is not None

    def test_mixed_case_keywords(self):
        """Keywords em case misto"""
        query = "SeLeCt campaign.id FrOm campaign WhErE campaign.status = 'ENABLED'"
        ast = parse_query(query)

        assert ast is not None
        assert ast.where is not None


