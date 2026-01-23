from typing import get_args
from pprint import pprint
from pydantic import StrictFloat, StrictInt
from datetime import date
from googleAdsDummy.engine.generators import generate_campaign, generate_campaign_profiles
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
        if len(profile_rules.ensure_at_least_one) > self.num_campaigns:
            raise ValueError("Number of profile ensurment can't be greateer that the number of campaigns")

    def _create_campaigns(self):
        campaigns = generate_campaign(self.seed, self.num_campaigns)
        self.campaigns = {obj.id: obj for obj in campaigns}

        campaigns_id = list(self.campaigns)
        self.campaign_profiles = generate_campaign_profiles(self.seed, campaigns_id, self.profile_rules)

        pprint(self.campaigns)
        pprint(self.campaign_profiles)

    def list_campaigns(self) -> list[Campaign]:
        return list(self.campaigns.values())

    def campaign_exists(self, id: str) -> bool:
        return id in self.campaigns

    def get_campaign(self, id: str) -> Campaign:
        if self.campaign_exists(id):
            return self.campaigns[id]
        else:
            raise ValueError("Incorrect Id or Campaign do not exist")

    def is_date_valid(self, date_tobe_check: str) -> bool:
        date_tobe_check = date.fromisoformat(date_tobe_check)

        return self.date_period.start_date <= date_tobe_check <= self.date_period.end_date

    def get_rules_snapshot(self) -> WorldRulesSnapshot:...
        # return WorldRulesSnapshot(seed=self.seed,
        #                           num_campaigns=self.num_campaigns,
        #                           weekend_factor=self.weekend_factor,
        #                           date_period=self.date_period,
        #                           anomaly_rules=self.anomaly_rules,
        #                           profile_rules=self.profile_rules,
        #                           campaign_profiles=...)

    def __repr__(self): ...  # Last thing  to be done
