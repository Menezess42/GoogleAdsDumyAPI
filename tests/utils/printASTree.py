from typing import Any


def print_query_tree(query, use_colors: bool = True):
    """
    Imprime a árvore AST da query no terminal com formato hierárquico.

    Args:
        query: O QueryNode a ser visualizado
        use_colors: Se True, usa cores ANSI no terminal (padrão: True)
    """

    if use_colors:
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        CYAN = "\033[96m"
        MAGENTA = "\033[95m"
        RESET = "\033[0m"
        BOLD = "\033[1m"
    else:
        BLUE = GREEN = YELLOW = CYAN = MAGENTA = RESET = BOLD = ""

    def format_value(value: Any) -> str:
        """Formata valores para exibição"""
        if isinstance(value, str):
            return f'"{value}"'
        return str(value)

    def print_node(node: Any, prefix: str = "", is_last: bool = True, label: str = ""):
        """Função recursiva para imprimir nós da árvore"""
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "

        node_name = type(node).__name__

        if label:
            print(
                f"{prefix}{connector}{BOLD}{CYAN}{label}:{RESET} {BLUE}{node_name}{RESET}"
            )
        else:
            print(f"{prefix}{connector}{BLUE}{node_name}{RESET}")

        new_prefix = prefix + extension

        if node_name == "QueryNode":
            print_node(
                node.from_clause,
                new_prefix,
                node.where is None and node.order_by is None and node.limit is None,
                "FROM",
            )
            if node.where:
                print_node(
                    node.where,
                    new_prefix,
                    node.order_by is None and node.limit is None,
                    "WHERE",
                )
            print_node(node.select, new_prefix, False, "SELECT")
            if node.order_by:
                print_node(node.order_by, new_prefix, node.limit is None, "ORDER BY")
            if node.limit:
                print_node(node.limit, new_prefix, True, "LIMIT")

        elif node_name == "SelectNode":
            for i, field in enumerate(node.fields):
                is_last_field = i == len(node.fields) - 1
                print_node(field, new_prefix, is_last_field, f"Field {i+1}")

        elif node_name == "FieldNode":
            print(
                f"{new_prefix}├── {GREEN}resource:{RESET} {format_value(node.resource)}"
            )
            print(f"{new_prefix}└── {GREEN}field:{RESET} {format_value(node.field)}")

        elif node_name == "FromNode":
            print(
                f"{new_prefix}└── {GREEN}resource:{RESET} {format_value(node.resource)}"
            )

        elif node_name == "WhereNode":
            for i, condition in enumerate(node.conditions):
                is_last_cond = i == len(node.conditions) - 1
                print_node(condition, new_prefix, is_last_cond, f"Condition {i+1}")

        elif node_name == "ComparisonNode":
            print_node(node.field, new_prefix, False, "field")
            print(
                f"{new_prefix}├── {GREEN}operator:{RESET} {YELLOW}{node.operator}{RESET}"
            )
            print(f"{new_prefix}└── {GREEN}value:{RESET} {format_value(node.value)}")

        elif node_name == "BetweenNode":
            print_node(node.field, new_prefix, False, "field")
            print(f"{new_prefix}├── {GREEN}lower:{RESET} {format_value(node.lower)}")
            print(f"{new_prefix}└── {GREEN}upper:{RESET} {format_value(node.upper)}")

        elif node_name == "OrderByNode":
            for i, item in enumerate(node.items):
                is_last_item = i == len(node.items) - 1
                print_node(item, new_prefix, is_last_item, f"Item {i+1}")

        elif node_name == "OrderByItemNode":
            print_node(node.field, new_prefix, False, "field")
            print(
                f"{new_prefix}└── {GREEN}direction:{RESET} {MAGENTA}{node.direction}{RESET}"
            )

        elif node_name == "LimitNode":
            print(f"{new_prefix}└── {GREEN}value:{RESET} {format_value(node.value)}")

    print(f"\n{BOLD}{BLUE}Query AST{RESET}")
    print_node(query)
    print()
