from datetime import date
from typing import List, Union

from googleAdsDummy.engine.world import World
from googleAdsDummy.query.handlers import dictDispatch_handlers
from googleAdsDummy.query.searchQuery_schema import SEARCH_QUERY_SCHEMA


class Executor:
    def __init__(self):
        ...

    def consultData(self, world: World, ast: dict) -> dict:
        self.world = world
        self.ast = ast
        for key, value in ast.items():
            response = dictDispatch_handlers[key](value)

        return {}
