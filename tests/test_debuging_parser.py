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
        metrics.impressions,
        metrics.clicks
    FROM campaign
    WHERE
        campaign.status = 'ENABLED'
    ORDER BY
        metrics.cost_micros DESC
    LIMIT 100
    """
    ast = parse_query(query)
    print_query_tree(ast)
    for a in ast:
        print(a)

    # Verificações


if __name__ == "__main__":
    test_comprehensive_query()
