from datetime import date
from typing import Union, List
from googleAdsDummy.engine.world import World
from googleAdsDummy.query.searchQuery_schema import SEARCH_QUERY_SCHEMA


class Executor:
    def __init__(self):
        self.dictDispatch = {
            "from_clause": self.handle_from,
            "where": self.handle_where,
            "select": self.handle_select,
        }
        self.allow_resources = SEARCH_QUERY_SCHEMA["resources"]
        self.allow_operators = SEARCH_QUERY_SCHEMA["operators"]
        self.allow_clauses = SEARCH_QUERY_SCHEMA["clauses"]

    def consultData(self, world: World, ast: dict) -> dict:
        self.world = world
        self.ast = ast
        for key, value in ast.items():
            handler = self.dictDispatch[key]
            handler(value)

        return {}

    def handle_from(self, dictValue):
        values = list(dictValue.values())
        if not all(value in self.allow_resources for value in values):
            raise ValueError(f"resouces {values} from FROM are not allowed")

    def handle_where(self, dictValue):
        print(dictValue)

    def check_lower_upper(self, lower: Union[int, float, str], upper: Union[int, float, str]) -> List:
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

    def handle_identifiers(self, identifier: dict) -> List[str]:
        resource = identifier["resource"]

        if resource not in self.allow_resources:
            raise ValueError(
                f"unexpected resource {resource} at WHERE condition"
            )
        
        field = identifier["field"]
        allowed_fields = self.allow_resources[resource]["fields"]
        
        if field not in allowed_fields:
            raise ValueError(
                f"unexpected field {field} at WHERE condition"
            )
        
        return [
            resource,
            field,
            allowed_fields[field]["type"]
        ]

    def handle_select(self, dictValue): ...
