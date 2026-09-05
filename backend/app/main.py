from fastapi import FastAPI
from .executor import execute_workload
from .feedback import (
    calculate_feedback,
    get_workload_profiles,
)

from .schemas import (
    FeedbackRequest,
    FeedbackResponse,
    WorkloadRequest,
    WorkloadDecision,
    WorkloadProfile,
)

from .scheduler import decide_workload


app = FastAPI(
    title="CarbonPilot",
    description="Carbon-aware workload scheduling engine",
    version="0.2.0",
)


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "CarbonPilot",
        "status": "running",
        "version": "0.2.0",
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "CarbonPilot",
    }


# ---------------------------------------------------------
# WORKLOAD SCHEDULING
# ---------------------------------------------------------

@app.post(
    "/workloads",
    response_model=WorkloadDecision,
)
def submit_workload(
    workload: WorkloadRequest,
):
    """
    Submit a workload to CarbonPilot.

    CarbonPilot evaluates the workload and decides
    whether it should run now, wait, or be scheduled
    according to carbon-aware policies.
    """

    decision = decide_workload(workload)

    return decision


# ---------------------------------------------------------
# WORKLOAD FEEDBACK
# ---------------------------------------------------------

@app.post(
    "/feedback",
    response_model=FeedbackResponse,
)
def submit_feedback(
    feedback: FeedbackRequest,
):
    """
    Submit actual workload measurements.

    CarbonPilot compares predicted and actual
    energy/carbon consumption and updates the
    workload's learned prediction profile.
    """

    result = calculate_feedback(
        workload_name=feedback.workload_name,
        predicted_energy_kwh=feedback.predicted_energy_kwh,
        actual_energy_kwh=feedback.actual_energy_kwh,
        predicted_co2e_kg=feedback.predicted_co2e_kg,
        actual_co2e_kg=feedback.actual_co2e_kg,
    )

    return FeedbackResponse(
        workload_name=feedback.workload_name,

        predicted_energy_kwh=result.predicted_energy_kwh,
        actual_energy_kwh=result.actual_energy_kwh,
        energy_error_percent=result.energy_error_percent,

        predicted_co2e_kg=result.predicted_co2e_kg,
        actual_co2e_kg=result.actual_co2e_kg,
        co2e_error_percent=result.co2e_error_percent,

        updated_energy_factor=result.updated_energy_factor,

        message=(
            "Prediction profile updated using "
            "actual workload measurements."
        ),
    )


# ---------------------------------------------------------
# LEARNED WORKLOAD PROFILES
# ---------------------------------------------------------

@app.get(
    "/profiles",
    response_model=list[WorkloadProfile],
)
def get_profiles():
    """
    Return the learned energy profiles
    for previously observed workloads.
    """

    profiles = get_workload_profiles()

    return [
        WorkloadProfile(
            workload_name=name,
            energy_factor=round(factor, 4),
            status="LEARNED",
        )
        for name, factor in profiles.items()
    ]
@app.post("/execute")
def execute(
    workload_name: str,
    command: str,
):
    result = execute_workload(
        workload_name=workload_name,
        command=command,
    )

    return {
        "workload_name": result.workload_name,
        "status": result.status,
        "execution_time_seconds": result.execution_time_seconds,
        "message": result.message,
    }