from .carbon import get_carbon_forecast
from .energy import estimate_energy_kwh, calculate_co2e_kg
from .schemas import WorkloadRequest, WorkloadDecision
from .feedback import get_energy_factor


def decide_workload(workload: WorkloadRequest) -> WorkloadDecision:

    forecast = get_carbon_forecast()

    correction_factor = get_energy_factor(workload.name)

    energy = estimate_energy_kwh(
        cpu=workload.cpu,
        memory_gb=workload.memory_gb,
        runtime_minutes=workload.estimated_runtime_minutes,
        correction_factor=correction_factor,
    )

    # A workload can only be deferred if the entire
    # execution fits before its deadline.
    valid_windows = [
        window
        for window in forecast
        if window.delay_minutes + workload.estimated_runtime_minutes
        <= workload.deadline_minutes
    ]

    if not valid_windows:
        current = forecast[0]

        co2e = calculate_co2e_kg(
            energy,
            current.carbon_intensity,
        )

        return WorkloadDecision(
            workload=workload.name,
            decision="RUN",
            recommended_delay_minutes=0,
            predicted_energy_kwh=energy,
            predicted_co2e_kg=co2e,
            carbon_intensity_g_per_kwh=current.carbon_intensity,
            reason="Deadline does not allow a safer deferral window.",
        )

    best_window = min(
        valid_windows,
        key=lambda window: window.carbon_intensity,
    )

    co2e = calculate_co2e_kg(
        energy,
        best_window.carbon_intensity,
    )

    if best_window.delay_minutes == 0:
        decision = "RUN"
        reason = "Current execution window is already optimal within the deadline."
    else:
        decision = "DEFER"
        reason = (
            "A lower-carbon execution window is available "
            "without violating the deadline."
        )

    return WorkloadDecision(
        workload=workload.name,
        decision=decision,
        recommended_delay_minutes=best_window.delay_minutes,
        predicted_energy_kwh=energy,
        predicted_co2e_kg=co2e,
        carbon_intensity_g_per_kwh=best_window.carbon_intensity,
        reason=reason,
    )