import builtins
from datetime import date
from typing import List, Union

from googleAdsDummy.query.searchQuery_schema import SEARCH_QUERY_SCHEMA

allow_resources = SEARCH_QUERY_SCHEMA["resources"]
allow_comparison_operators = SEARCH_QUERY_SCHEMA["comparison_operators"]
allow_between_operators = SEARCH_QUERY_SCHEMA["between_operators"]
allow_clauses = SEARCH_QUERY_SCHEMA["clauses"]
allow_fields = {
    key: value
    for resources in SEARCH_QUERY_SCHEMA["resources"].values()
    for key, value in resources["fields"].items()
}

dictDispatch_handlers = {
    "where": lambda dictValue: handle_where(dictValue),
    "from_clause": lambda dictValue: handle_from(dictValue),
    "select": lambda dictValue: handle_select(dictValue),
}


def handle_from(dictValue):
    values = list(dictValue.values())
    if not all(value in allow_resources for value in values):
        raise ValueError(f"resouces {values} in FROM clause are not allowed")

    return {
        "type": "from",
        "resource": dictValue["resource"]
    }


def handle_where(dictValue):
    conditions = list(dictValue["conditions"])
    for value in conditions:
        verify_field(value["field"])
        operator2Verify = list(value.items())[1:]
        verify_operators(operator2Verify, value["field"]["field"])

    return {
        "type": "where",
        "conditions": conditions
    }


def handle_select(dictValue):
    for field in dictValue["fields"]:
        verify_field(field)

    return {
        "type": "select",
        "fields": dictValue["fields"]
    }

def verify_field(field):
    if field["resource"] not in allow_resources:
        raise ValueError(f"Unexpected column {field['resource']}")
    resource = field["resource"]
    if field["field"] not in allow_resources[resource]["fields"]:
        raise ValueError(f"Unexpected field {field['field']}")


def verify_operators(operators_list, field):
    lower_bound, upper_bound = operators_list

    if lower_bound[0] in allow_between_operators:

        if allow_fields[field]["type"] not in ["int", "float", "date"]:
            raise ValueError(
                f"Field of type {allow_fields[field]["type"]} can not be used in BETWEEN comparison"
            )

        response_loUp_chck = verify_lower_upper_limits(lower_bound[1], upper_bound[1])
        if not limitsType_compatible_with_field(response_loUp_chck, field):
            raise ValueError(f"Field and limits are not the same type")

    elif lower_bound[1] in allow_comparison_operators:
        if allow_fields[field]["type"] == "string" and lower_bound[1] != "=":
            raise ValueError(
                f"Field of type {allow_fields[field]['type']} doesn't work with the {lower_bound[1]} operator"
            )

    else:
        raise ValueError(f"Unexpected operator in WHERE clause")


def verify_lower_upper_limits(
    lower: Union[int, float, str], upper: Union[int, float, str]
) -> List:
    if type(lower) != type(upper):
        raise ValueError(
            f"Limits from BETWEEN clause has different types: {lower}, {upper}"
        )

    if isinstance(upper, (int, float)):
        if upper <= lower:
            raise ValueError(f"BETWEEN clause invalid limit: <{lower}|{upper}>")
    else:
        lower_date = date.fromisoformat(lower)
        upper_date = date.fromisoformat(upper)
        if upper_date <= lower_date:
            raise ValueError(f"BETWEEN clause invalid limit: <{lower}|{upper}>")

    return [lower, upper, type(lower).__name__]


def limitsType_compatible_with_field(limits, field) -> bool:
    field_type = allow_fields[field]["type"]

    limitsType = builtins.__dict__[limits[-1]]

    type_compatibility = {
        "int": {int},
        "float": {int, float},
        "date": {str},
        "str": {str},
    }

    allowed_types = type_compatibility.get(field_type, set())

    return limitsType in allowed_types


if __name__ == "__main__":
    verify_operators([("lower", "2024-01-01"), ("upper", "2025-01-02")], "date")
