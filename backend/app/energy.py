def estimate_energy_kwh(
    cpu: float,
    memory_gb: float,
    runtime_minutes: int,
    correction_factor: float = 1.0,
) -> float:

    runtime_hours = runtime_minutes / 60

    cpu_power_w = cpu * 20
    memory_power_w = memory_gb * 2

    total_power_w = cpu_power_w + memory_power_w

    base_energy_kwh = (
        total_power_w * runtime_hours
    ) / 1000

    adjusted_energy_kwh = (
        base_energy_kwh * correction_factor
    )

    return round(adjusted_energy_kwh, 4)


def calculate_co2e_kg(
    energy_kwh: float,
    carbon_intensity_g_per_kwh: float,
) -> float:

    co2e_grams = (
        energy_kwh * carbon_intensity_g_per_kwh
    )

    return round(co2e_grams / 1000, 4)