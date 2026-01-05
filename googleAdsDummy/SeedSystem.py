from typing import Callable


def seedSystem(seed: int) -> Callable[[], float]:
    value = seed & 0xFFFFFFFF

    def generate() -> float:
        nonlocal value
        value = (value + 0x6D2B79F5) & 0xFFFFFFFF

        t = value
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t = (t ^ (t + ((t ^ (t >> 7)) * (t | 61)))) & 0xFFFFFFFF

        return (t ^ (t >> 14)) / 4294967296

    return generate
