from pydantic import BaseModel


class Campaign(BaseModel):
    id: str
    name: str
    budget_amount: float
