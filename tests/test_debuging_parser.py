from googleAdsDummy.searchQueryCompiler.parser_SearchQuery import parse_query

from tests.printASTree import print_query_tree


# First test to fail the unity test from the test_parser.py
def test_where_and_limit():
    """WHERE + LIMIT"""
    query = """
    SELECT campaign.id FROM campaign
    WHERE campaign.status = 'ENABLED'
    LIMIT 50
    """
    ast = parse_query(query)
    print_query_tree(ast)
    assert ast.where is not None
    assert ast.limit is not None
    assert ast.order_by is None


def test_comprehensive_query():
    """Query completa usando todos os recursos da gramática"""
    query = """
    SELECT 
        campaign.id,
        campaign.name,
        campaign.status,
        ad_group.id,
        ad_group.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros
    FROM campaign
    WHERE 
        campaign.status = 'ENABLED'
        AND metrics.impressions > 1000
        AND metrics.clicks < 500
        AND metrics.cost_micros BETWEEN 1000000 AND 5000000
        AND campaign.budget_amount_micros > 100000
        AND ad_group.cpc_bid_micros BETWEEN 500000 AND 2000000
    ORDER BY 
        metrics.impressions DESC,
        metrics.clicks ASC,
        campaign.name,
        metrics.cost_micros DESC
    LIMIT 100
    """
    ast = parse_query(query)
    print_query_tree(ast)
    print(ast.from_clause)
    print(ast.select)
    print(type(ast))
    print(type(ast.from_clause))
    print(type(ast.select))

    # Verificações
    assert ast.select is not None
    assert len(ast.select.fields) == 8  # 8 campos no SELECT
    assert ast.from_clause is not None
    assert ast.where is not None
    assert len(ast.where.conditions) == 6  # 6 condições no WHERE
    assert ast.order_by is not None
    assert len(ast.order_by.items) == 4  # 4 itens no ORDER BY
    assert ast.limit is not None
    assert ast.limit.value == 100


if __name__ == "__main__":
    test_comprehensive_query()
