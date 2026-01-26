from pydantic import StrictFloat, StrictInt, validate_call

from googleAdsDummy.engine.world import World
from googleAdsDummy.types import Anomaly_rules, Date_period, Profile_rules


class Gad:
    @validate_call
    def config(
        self,
        seed: StrictInt | None,
        num_campaigns: StrictInt,
        weekend_factor: StrictFloat,
        date_period: Date_period,
        anomaly_rules: Anomaly_rules,
        profile_rules: Profile_rules,
    ) -> None:

        if seed is not None and seed < 1:
            raise ValueError("Seed should be an integer greater than or equal to 1")

        if num_campaigns < 1:
            raise ValueError(
                "num_campaigns should be an integer greater than or equal to 1"
            )

        if not (0.0 <= weekend_factor <= 1.0):
            raise ValueError("weekend_factor should be a float in the range [0, 1]")

        if not seed:
            seed = 42

        self.seed = seed
        self.num_campaigns = num_campaigns
        self.weekend_factor = weekend_factor
        self.date_period = date_period
        self.anomaly_rules = anomaly_rules
        self.profile_rules = profile_rules

    def create(self):
        self.world = World(
            self.seed,
            self.num_campaigns,
            self.weekend_factor,
            self.date_period,
            self.anomaly_rules,
            self.profile_rules,
        )

    def query(self, searchQuery: str): ...


if __name__ == "__main__":
    gad = Gad()
    gad.config(
        seed=42,
        num_campaigns=3,
        weekend_factor=0.5,
        date_period=("2024-01-01", "2025-05-01"),
        anomaly_rules=[True, 0.5, (0.5, 0.2)],
        profile_rules=[["A", "B", "C"], ["A"], {"A": 0.25, "B": 0.50}],
    )
    gad.create()
    campaign_lists = gad.world.list_campaigns()
    print(campaign_lists[0])
