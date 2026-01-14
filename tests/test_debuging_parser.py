from googleAdsDummy.searchQueryCompiler.parser_SearchQuery import parse_query
from .printASTree import print_query_tree


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


if __name__ == "__main__":
    test_where_and_limit()
