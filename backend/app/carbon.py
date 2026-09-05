from dataclasses import dataclass


@dataclass
class CarbonWindow:
    delay_minutes: int
    carbon_intensity: float


def get_carbon_forecast() -> list[CarbonWindow]:
    return [
        CarbonWindow(0, 520),
        CarbonWindow(30, 480),
        CarbonWindow(60, 390),
        CarbonWindow(90, 300),
        CarbonWindow(120, 250),
    ]