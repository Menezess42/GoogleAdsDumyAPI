from pydantic import validate_call

from googleAdsDummy.types import Anomaly_rules, Date_period, Profile_rules


class Gad:
    @validate_call
    def config(
        self,
        seed: int | None,
        num_campaigns: int,
        weekend_factor: float,
        date_period: Date_period,
        anomaly_rules: Anomaly_rules,
        profile_rules: Profile_rules,
    ) -> None:

        if seed and not isinstance(seed, int) and seed < 0:
            raise ValueError("Seed must be an integer and more than 0")
        if not isinstance(num_campaigns, int) and num_campaigns < 1:
            raise ValueError("Invalid type or value is less than 1")
        if not isinstance(weekend_factor, float) and weekend_factor < 0:
            raise ValueError("Invalid type or value is less than 0")

        if not seed:
            seed = 42

    def create(self): ...
    def query(self): ...


if __name__ == "__main__":
    gad = Gad()
    gad.config(
        42,
        3,
        0.3,
        ("2024-03-01", "2025-03-01"), # TODO: Validate if the start date is small that the end date; 2024 < 2025 ?
        [True, 0.2, (0.5, 0.3)],
        [["A", "B", "C"], ["A"], {"A": 0.5}],
    )
