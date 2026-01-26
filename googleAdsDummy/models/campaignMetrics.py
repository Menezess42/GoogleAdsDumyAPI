from pydantic import BaseModel
from datetime import date

class CampaignMetrics(BaseModel):
    campaign_id: str
    date: date
    impressions: int
    clicks: int
    cost: float
    conversions: int
    cpa: float
