from datetime import date
from typing import List, Union

from googleAdsDummy.query.searchQuery_schema import SEARCH_QUERY_SCHEMA

allow_resources = SEARCH_QUERY_SCHEMA["resources"]
allow_operators = SEARCH_QUERY_SCHEMA["operators"]
allow_clauses = SEARCH_QUERY_SCHEMA["clauses"]

handlers_dictDispatch = {
    "where": lambda dictValue: handle_where(dictValue),
    "from_clause": lambda dictValue: handle_from(dictValue),
    "select": lambda dictValue: handle_select(dictValue),
}


def handle_from(dictValue):
    values = list(dictValue.values())
    if not all(value in allow_resources for value in values):
        raise ValueError(f"resouces {values} from FROM are not allowed")


def handle_where(dictValue):
    conditions = list(dictValue["conditions"])
    # Verify the fields
    for value in conditions:
        print(value)

        # verify the resources from the fields [X]
        # verify the identifiers from the fields [X]
        verify_field(value['field'])
    # Verify the operators
        # verify the values in relation to the operator
    # If operator between
    # Verify if upper limit is greater than lower
    # Verify if identifier is applicable to between operator
    # If comparison
    # Verify if identifier is aplicable to the operator

def verify_field(field):
    if field["resource"] not in allow_resources:
        raise ValueError(
            f"Unexpected column {field['resource']} in WHERE clause"
        )
    resource = field["resource"]
    if field["field"] not in allow_resources[resource]["fields"]:
        raise ValueError(
            f"Unexpected field {field['field']} in WHERE clause"
        )


def handle_select(dictValue): ...


def handle_identifiers(identifier: dict) -> List[str]:
    resource = identifier["resource"]

    if resource not in allow_resources:
        raise ValueError(f"unexpected resource {resource} at WHERE condition")

    field = identifier["field"]
    allowed_fields = allow_resources[resource]["fields"]
    if field not in allowed_fields:
        raise ValueError(f"unexpected field {field} at WHERE condition")

    return [resource, field, allowed_fields[field]["type"]]


def check_lower_upper(
    lower: Union[int, float, str], upper: Union[int, float, str]
) -> List:
    if type(lower) != type(upper):
        raise ValueError(f"BETWEEN clause limit different types: {lower}, {upper}")

    if isinstance(upper, (int, float)):
        if upper <= lower:
            raise ValueError(f"BETWEEN clause invalid limit: <{lower}|{upper}>")
    else:
        lower_date = date.fromisoformat(lower)
        upper_date = date.fromisoformat(upper)
        if upper_date <= lower_date:
            raise ValueError(f"BETWEEN clause invalid limit: <{lower}|{upper}>")

    return [lower, upper, type(lower).__name__]
