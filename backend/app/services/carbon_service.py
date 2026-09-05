from datetime import datetime, timedelta
import random


def get_current_carbon_intensity():
    """
    Returns current grid carbon intensity in gCO2e/kWh.
    Mock implementation for prototype.
    """

    intensity = random.randint(150, 600)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "carbon_intensity": intensity,
        "unit": "gCO2e/kWh"
    }


def get_carbon_forecast(hours=24):
    """
    Generates a mock 24-hour carbon-intensity forecast.
    """

    now = datetime.utcnow()
    forecast = []

    for i in range(hours):
        timestamp = now + timedelta(hours=i)

        # Simulated daily variation
        base = 350
        variation = random.randint(-150, 150)

        intensity = max(50, base + variation)

        forecast.append({
            "timestamp": timestamp.isoformat(),
            "carbon_intensity": intensity,
            "unit": "gCO2e/kWh"
        })

    return forecast