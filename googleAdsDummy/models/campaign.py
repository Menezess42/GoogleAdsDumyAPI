from pydantic import BaseModel


class Campaign(BaseModel):
    id: str
    name: str
    budget_amount: float

    def get_id(self):
        return self.id

    def get_budget_amount(self):
        return self.budget_amount
