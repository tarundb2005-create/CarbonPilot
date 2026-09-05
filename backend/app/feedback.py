from dataclasses import dataclass


# In-memory workload learning profiles.
# PostgreSQL will replace this later.
workload_profiles = {}


@dataclass
class FeedbackResult:
    predicted_energy_kwh: float
    actual_energy_kwh: float
    energy_error_percent: float

    predicted_co2e_kg: float
    actual_co2e_kg: float
    co2e_error_percent: float

    updated_energy_factor: float


def calculate_feedback(
    workload_name: str,
    predicted_energy_kwh: float,
    actual_energy_kwh: float,
    predicted_co2e_kg: float,
    actual_co2e_kg: float,
) -> FeedbackResult:

    if predicted_energy_kwh <= 0:
        raise ValueError(
            "Predicted energy must be greater than zero."
        )

    if predicted_co2e_kg <= 0:
        raise ValueError(
            "Predicted CO2e must be greater than zero."
        )

    if actual_energy_kwh < 0:
        raise ValueError(
            "Actual energy cannot be negative."
        )

    if actual_co2e_kg < 0:
        raise ValueError(
            "Actual CO2e cannot be negative."
        )

    energy_error = (
        (actual_energy_kwh - predicted_energy_kwh)
        / predicted_energy_kwh
    ) * 100

    co2e_error = (
        (actual_co2e_kg - predicted_co2e_kg)
        / predicted_co2e_kg
    ) * 100

    new_factor = (
        actual_energy_kwh
        / predicted_energy_kwh
    )

    workload_profiles[workload_name] = new_factor

    return FeedbackResult(
        predicted_energy_kwh=round(
            predicted_energy_kwh,
            4,
        ),
        actual_energy_kwh=round(
            actual_energy_kwh,
            4,
        ),
        energy_error_percent=round(
            energy_error,
            2,
        ),
        predicted_co2e_kg=round(
            predicted_co2e_kg,
            4,
        ),
        actual_co2e_kg=round(
            actual_co2e_kg,
            4,
        ),
        co2e_error_percent=round(
            co2e_error,
            2,
        ),
        updated_energy_factor=round(
            new_factor,
            4,
        ),
    )


def get_energy_factor(
    workload_name: str,
) -> float:
    """
    Return the learned correction factor.

    If CarbonPilot has never seen this workload,
    use 1.0.
    """

    return workload_profiles.get(
        workload_name,
        1.0,
    )


def get_workload_profiles():
    """
    Return all learned workload profiles.
    """

    return workload_profiles.copy()