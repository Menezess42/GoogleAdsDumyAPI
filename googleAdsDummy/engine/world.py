from pprint import pprint
from typing import get_args

from pydantic import StrictFloat, StrictInt

from googleAdsDummy.engine.generators import generate_campaign
from googleAdsDummy.models.campaign import Campaign
from googleAdsDummy.models.profiles import ProfileType
from googleAdsDummy.types import (
    Anomaly_rules,
    Date_period,
    Profile_rules,
    WorldRulesSnapshot,
)


class World:
    def __init__(
        self,
        seed: StrictInt,
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

        self._allowed_profiles(profile_rules)
        self.profile_rules = profile_rules

        self._create_campaigns()

    def _allowed_profiles(self, profile_rules: Profile_rules) -> None:
        if not profile_rules.allow_profiles.issubset(set(get_args(ProfileType))):
            raise ValueError("allowed_profiles should have only existent profiles")

    def _create_campaigns(self):
        self.campaigns = generate_campaign(self.seed, self.num_campaigns)

        pprint(self.campaigns)

    def __repr__(self): ...  # Last thing  to be done

    def list_campaigns(self) -> list[Campaign]: ...

    def campaign_exists(self, id) -> bool: ...

    def get_campaign(self, id) -> Campaign: ...

    def is_date_valid(self, date) -> bool: ...

    def get_rules_snapshot(self) -> WorldRulesSnapshot:
        pprint(f"seed={self.seed}")
        pprint(f"num_campaigns={self.num_campaigns}")
        pprint(f"weekend_factor={self.weekend_factor}")
        pprint(self.date_period)
        pprint(self.anomaly_rules)
        pprint(self.profile_rules)



