from pydantic import BaseModel

class Campaign(BaseModel):
    id: str
    name: str
    status: str = "PAUSED"
    budget_amount: float
