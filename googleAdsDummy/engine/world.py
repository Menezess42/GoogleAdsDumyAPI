from pydantic import StrictFloat, StrictInt
from googleAdsDummy.models.campaign import Campaign

from googleAdsDummy.types import Anomaly_rules, Date_period, Profile_rules, WorldRulesSnapshot


class World:
    def __init__(
        self,
        seed: StrictInt | None,
        num_campaigns: StrictInt,
        weekend_factor: StrictFloat,
        date_period: Date_period,
        anomaly_rules: Anomaly_rules,
        profile_rules: Profile_rules,
    ) -> None:
        self.seed = seed
        self.num_campaigns = num_campaigns
        self.weekend_factor = weekend_factor
        self.date_period = date_period
        self.anomaly_rules = anomaly_rules
        self.profile_rules = profile_rules

    def __repr__(self): ...  # Last thing  to be done

    def _create_campaigns(self):
        ...

    def list_campaigns(self) -> list[Campaign]:
        ...

    def campaign_exists(self, id) -> bool:
        ...

    def get_campaign(self, id) -> Campaign:
        ...

    def is_date_valid(self, date) -> bool:
        ...

    def get_rules_snapshot(self) -> WorldRulesSnapshot:
        ...


