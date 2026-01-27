SEARCH_QUERY_SCHEMA = {
    "resources": {
        "campaign": {
            "fields": {
                "id": {
                    "type": "string",
                    "static": True,
                    "filterable": True,
                    "orderable": True,
                },
                "name": {
                    "type": "string",
                    "static": True,
                    "filterable": True,
                    "orderable": True,
                },
                "budget_amount": {
                    "type": "float",
                    "static": True,
                    "filterable": True,
                    "orderable": True,
                },
            }
        },
        "metrics": {
            "fields": {
                "campaign_id": {
                    "type": "string",
                    "static": False,
                    "filterable": True,
                    "orderable": False,
                },
                "date": {
                    "type": "date",
                    "static": False,
                    "filterable": True,
                    "orderable": True,
                },
                "impressions": {
                    "type": "int",
                    "static": False,
                    "filterable": True,
                    "orderable": True,
                },
                "clicks": {
                    "type": "int",
                    "static": False,
                    "filterable": True,
                    "orderable": True,
                },
                "cost": {
                    "type": "float",
                    "static": False,
                    "filterable": True,
                    "orderable": True,
                },
                "conversions": {
                    "type": "int",
                    "static": False,
                    "filterable": True,
                    "orderable": True,
                },
                "cpa": {
                    "type": "float",
                    "static": False,
                    "filterable": False,
                    "orderable": True,
                },
            },
        },
    },
    "operators": {
        "comparison": ["=", ">", "<"],
        "between": True,
    },
    "clauses": {
        "select": True,
        "from_clause": True,
        "where": True,
        "order_by": True,
        "limit": True,
    }
}
