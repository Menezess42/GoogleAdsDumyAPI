from datetime import date

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated
from typing import Dict


class Anomaly_effects(BaseModel):
    spike_conversions: float = Field(ge=0.0, le=1.0)
    drop_conversions: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="before")
    @classmethod
    def accept_tuple(cls, v):
        if isinstance(v, tuple):
            return {"spike_conversions": v[0], "drop_conversions": v[1]}
        return v


class Anomaly_rules(BaseModel):
    enabled: bool
    probability: float = Field(ge=0.0, le=1.0)
    efects: Anomaly_effects

    @model_validator(mode="before")
    @classmethod
    def accept_list(cls, v):
        if isinstance(v, list):
            return {"enabled": v[0], "probability": v[1], "efects": v[2]}
        return v


class Profile_rules(BaseModel):
    allow_profiles: set[str] = Field(min_length=1)
    ensure_at_least_one: set[str] | None = None
    distribution: dict[str, Annotated[float, Field(ge=0.0, le=1.0)]] | None = Field(
        default=None, min_length=1
    )

    @model_validator(mode="before")
    @classmethod
    def accept_list(cls, v):
        if isinstance(v, list):
            if v[1] == []:
                v[1] = None
            return {
                "allow_profiles": v[0],
                "ensure_at_least_one": v[1],
                "distribution": v[2] if len(v) > 2 else None,
            }
        return v

    @model_validator(mode="before")
    @classmethod
    def validate_values(cls, v):
        allow_profiles, ensure_at_least_one, distribution = v

        allow_profiles = {x.upper() for x in allow_profiles}

        ensure_at_least_one = (
            {x.upper() for x in ensure_at_least_one} if ensure_at_least_one else None
        )

        distribution = (
            {k.upper(): v for k, v in distribution.items()} if distribution else None
        )

        if ensure_at_least_one and not ensure_at_least_one.issubset(allow_profiles):
            raise ValueError(
                "ensure_at_least_one contains values that are not present in allow_profile"
            )

        if distribution:
            if not set(distribution).issubset(allow_profiles):
                raise ValueError(
                    "distribution contains keys not present in allow_profiles"
                )

            if sum(distribution.values()) > 1.0:
                raise ValueError(
                    "distribution has poorly distributed values. The sum of all the values surpasses 1.0"
                )

        return {
            "allow_profiles": allow_profiles,
            "ensure_at_least_one": ensure_at_least_one,
            "distribution": distribution,
        }


class Date_period(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="before")
    @classmethod
    def accept_tuple(cls, v):
        if isinstance(v, tuple):
            return {"start_date": v[0], "end_date": v[1]}
        return v

    @model_validator(mode="after")
    def mustBe_greaterThan_startDate(self):
        if self.start_date >= self.end_date:
            raise ValueError("start_date should be less than end_date")
        return self

class WorldRulesSnapshot(BaseModel):
    seed: int
    num_campaigns: int
    weekend_factor: float
    date_period: Date_period
    anomaly_rules: Anomaly_rules
    profile_rules: Profile_rules

    campaign_profiles: Dict[str, str]
