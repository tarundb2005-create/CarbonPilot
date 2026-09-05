from fastapi import FastAPI, HTTPException

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
from .executor import create_workload_job


app = FastAPI(
    title="CarbonPilot",
    description="Carbon-aware Kubernetes workload scheduling engine",
    version="0.4.0",
)


@app.get("/")
def root():
    return {
        "service": "CarbonPilot",
        "status": "running",
        "version": "0.4.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "CarbonPilot",
    }


@app.post(
    "/workloads",
    response_model=WorkloadDecision,
)
def submit_workload(
    workload: WorkloadRequest,
):
    """
    Carbon-aware workload submission.

    The scheduler decides whether the workload should
    RUN immediately or DEFER to a lower-carbon window.
    """

    decision = decide_workload(workload)

    if decision.decision == "RUN":
        try:
            job_result = create_workload_job(
                workload_name=workload.name,
                runtime_minutes=workload.estimated_runtime_minutes,
            )

            decision.execution_status = job_result["status"]
            decision.kubernetes_job = job_result["job_name"]

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Kubernetes execution failed: {error}",
            )

    else:
        decision.execution_status = "DEFERRED"
        decision.kubernetes_job = None

    return decision


@app.post(
    "/execute",
    response_model=WorkloadDecision,
)
def execute_workload(
    workload: WorkloadRequest,
):
    """
    Carbon-aware execution endpoint.

    The workload first passes through CarbonPilot's
    scheduling decision.

    RUN:
        Create a Kubernetes Job.

    DEFER:
        Do not create a Kubernetes Job yet.
    """

    decision = decide_workload(workload)

    if decision.decision == "DEFER":
        decision.execution_status = "DEFERRED"
        decision.kubernetes_job = None

        return decision

    try:
        job_result = create_workload_job(
            workload_name=workload.name,
            runtime_minutes=workload.estimated_runtime_minutes,
        )

        decision.execution_status = job_result["status"]
        decision.kubernetes_job = job_result["job_name"]

        return decision

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Kubernetes execution failed: {error}",
        )


@app.post(
    "/feedback",
    response_model=FeedbackResponse,
)
def submit_feedback(
    feedback: FeedbackRequest,
):
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


@app.get(
    "/profiles",
    response_model=list[WorkloadProfile],
)
def get_profiles():
    profiles = get_workload_profiles()

    return [
        WorkloadProfile(
            workload_name=name,
            energy_factor=round(factor, 4),
            status="LEARNED",
        )
        for name, factor in profiles.items()
    ]