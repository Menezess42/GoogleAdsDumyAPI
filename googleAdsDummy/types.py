from datetime import date

from pydantic import BaseModel, Field, model_validator


class Anomaly_effects(BaseModel):
    spike_conversions: float
    drop_conversions: float

    @model_validator(mode="before")
    @classmethod
    def accept_tuple(cls, v):
        if isinstance(v, tuple):
            return {
                "spike_conversions": v[0],
                "drop_conversions": v[1]
            }
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
    allow_profiles: list[str]
    ensure_at_least_one: list[str]
    distribution: dict[str, float] | None = None
    @model_validator(mode="before")
    @classmethod
    def accept_list(cls, v):
        if isinstance(v, list):
            return {
                "allow_profiles": v[0],
                "ensure_at_least_one": v[1],
                "distribution": v[2]
            }
        return v



class Date_period(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="before")
    @classmethod
    def accept_tuple(cls, v):
        if isinstance(v, tuple):
            return {"start_date": v[0], "end_date": v[1]}
        return v
