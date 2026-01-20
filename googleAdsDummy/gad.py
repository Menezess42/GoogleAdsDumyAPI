from pydantic import validate_call, StrictFloat, StrictInt

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
        profile_rules: Profile_rules
    ) -> None:

        if seed and (not isinstance(seed, int) or seed < 0):
            raise ValueError("Seed should be an integer and more than 0")
        if not isinstance(num_campaigns, int) or num_campaigns < 1:
            raise ValueError("num_campaigns should be int and should be more than 1")
        if not isinstance(weekend_factor, float) or (
            weekend_factor < 0.0 or weekend_factor > 1.0
        ):
            raise ValueError("weekend_factor should be float in the range between [0, 1]")

        if not seed:
            seed = 42

        self.seed = seed
        self.num_campaigns = num_campaigns
        self.weekend_factor = weekend_factor
        self.date_period = date_period
        self.anomaly_rules = anomaly_rules
        self.profile_rules = profile_rules

    def create(self): ...
    def query(self): ...


if __name__ == "__main__":
    gad = Gad()
    gad.config(
        seed=42,
        num_campaigns=3,
        weekend_factor=0.5,
        date_period=("2024-01-01", "2025-05-01"),
        anomaly_rules=[True, 0.5, (0.5, 0.2)],
        profile_rules=[["A", "B", "C", "A"], ["A"], {"A": 0.1, "B": 0.3}]
    )
