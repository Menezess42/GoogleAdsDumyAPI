from datetime import date, timedelta
from pprint import pprint
from typing import List, Union

from googleAdsDummy.engine.world import World
from googleAdsDummy.query.handlers import dictDispatch_handlers
from googleAdsDummy.query.searchQuery_schema import SEARCH_QUERY_SCHEMA
from googleAdsDummy.engine.generators import generate_metrics


class Executor:
    def __init__(self):
        self.OPERATORS = {
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            "=": lambda a, b: a == b,
            "==": lambda a, b: a == b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "!=": lambda a, b: a != b,
        }

    def consultData(self, world: World, ast: dict) -> dict:
        self.world = world
        self.ast = ast

        query_plan = []
        for key, value in ast.items():
            response = dictDispatch_handlers[key](value)
            query_plan.append(response)


        return self.execute_query_plan(query_plan)

    def execute_query_plan(self, query_plan):
        needs_metrics = self.has_metrics_reference(query_plan)

        items = self.fetch_base_items(query_plan)

        if needs_metrics:
            items = self.expand_with_metrics(items, query_plan)

        where_clause = self.get_clause_by_type(query_plan, "where")
        if where_clause:
            items = self.apply_filters(items, where_clause["conditions"])

        select_clause = self.get_clause_by_type(query_plan, "select")
        result = self.project_fields(items, select_clause["fields"])

        return result

    def has_metrics_reference(self, query_plan):
        for clause in query_plan:
            if clause["type"] == "select":
                if any(f["resource"] == "metrics" for f in clause["fields"]):
                    return True
            if clause["type"] == "where":
                if any(
                    c["field"]["resource"] == "metrics" for c in clause["conditions"]
                ):
                    return True
        return False

    def fetch_base_items(self, query_plan):
        from_clause = self.get_clause_by_type(query_plan, "from")
        resource = from_clause["resource"]
        
        if resource == "campaign":
            items = self.world.list_campaigns()
            return items
        else:
            raise ValueError(f"Resource {resource} not implemented yet")

    def expand_with_metrics(self, campaigns, query_plan):
        date_range = self._extract_date_range(query_plan)

        expanded = []
        for campaign in campaigns:
            for d in date_range:
                metrics = generate_metrics(self.world, campaign.id, d.isoformat())
                expanded.append({"campaign": campaign, "metrics": metrics})

        return expanded

    def _extract_date_range(self, query_plan):
        where_clause = self.get_clause_by_type(query_plan, "where")

        if where_clause:
            for condition in where_clause["conditions"]:
                field = condition["field"]
                if field["resource"] == "metrics" and field["field"] == "date":
                    if "lower" in condition and "upper" in condition:
                        start = date.fromisoformat(condition["lower"])
                        end = date.fromisoformat(condition["upper"])
                        return self._date_range(start, end)
        raise ValueError(
            "Query with metrics require a metrics.date BETWEEN clause"
        )

    def _date_range(self, start: date, end: date):
        days = (end - start).days
        return [start + timedelta(days=i) for i in range(days+1)]

    def apply_filters(self, items, conditions):
        filtered = []
        for item in items:
            if self.matches_all_conditions(item, conditions):
                filtered.append(item)

        return filtered

    def matches_all_conditions(self, item, conditions):
        for condition in conditions:
            if not self.evaluate_condition(item, condition):
                return False
        return True

    def evaluate_condition(self, item, condition):
        resource = condition["field"]["resource"]
        field_name = condition["field"]["field"]

        obj = item["campaign"] if isinstance(item, dict) else item

        if resource == "campaign":
            valor_real = getattr(obj, f"get_{field_name}")()
        elif resource == "metrics":
            valor_real = getattr(item["metrics"], field_name)

        if "lower" in condition and "upper" in condition:
            lower = condition["lower"]
            upper = condition["upper"]
            if isinstance(valor_real, date):
                lower = date.fromisoformat(lower)
                upper = date.fromisoformat(upper)
            return lower <= valor_real <= upper
        else:
            operator = condition["operator"]
            operador_func = self.OPERATORS[operator]
            value = condition["value"]
            return operador_func(valor_real, value)

    def project_fields(self, items, fields):
        columns = []
        for field_spec in fields:
            resource = field_spec["resource"]
            field_name = field_spec["field"]
            columns.append(f"{resource}.{field_name}")
        
        data = []
        for item in items:
            row = []
            for field_spec in fields:
                resource = field_spec["resource"]
                field_name = field_spec["field"]
                
                if resource == "campaign":
                    obj = item["campaign"] if isinstance(item, dict) else item
                    valor = getattr(obj, field_name)
                elif resource == "metrics":
                    valor = getattr(item["metrics"], field_name)
                
                row.append(valor)
            data.append(row)
    
        return {
            "columns": columns,
            "data": data,
            "count": len(data)
        }

    def get_clause_by_type(self, query_plan, clause_type):
        for clause in query_plan:
            if clause["type"] == clause_type: # Lógica errada, devo olhar isso aqui.
                return clause

        return None
