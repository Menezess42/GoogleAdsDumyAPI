from datetime import date
from typing import List, Union

from googleAdsDummy.engine.world import World
from googleAdsDummy.query.handlers import handlers_dictDispatch
from googleAdsDummy.query.searchQuery_schema import SEARCH_QUERY_SCHEMA


class Executor:
    def __init__(self):
        self.allow_resources = SEARCH_QUERY_SCHEMA["resources"]
        self.allow_operators = SEARCH_QUERY_SCHEMA["operators"]
        self.allow_clauses = SEARCH_QUERY_SCHEMA["clauses"]

    def consultData(self, world: World, ast: dict) -> dict:
        self.world = world
        self.ast = ast
        for key, value in ast.items():
            response = handlers_dictDispatch[key](value)

        return {}
