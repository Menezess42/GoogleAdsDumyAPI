from typing import Literal, TypedDict

ProfileType = Literal["A", "B", "C"]


class ProfileBehavior(TypedDict):
    ctr_mean: float
    ctr_std: float
    conv_rate_mean: float
    conv_rate_std: float
    volume_factor: float


PROFILE_BEHAVIOR: dict[ProfileType, ProfileBehavior] = {
    "A": {
        "ctr_mean": 0.055,
        "ctr_std": 0.012,
        "conv_rate_mean": 0.075,
        "conv_rate_std": 0.02,
        "volume_factor": 1.2,
    },
    "B": {
        "ctr_mean": 0.035,
        "ctr_std": 0.01,
        "conv_rate_mean": 0.04,
        "conv_rate_std": 0.015,
        "volume_factor": 1.0,
    },
    "C": {
        "ctr_mean": 0.018,
        "ctr_std": 0.008,
        "conv_rate_mean": 0.015,
        "conv_rate_std": 0.01,
        "volume_factor": 0.75,
    },
}
