from pydantic import BaseModel, Field


class WorkloadRequest(BaseModel):
    name: str = Field(..., description="Unique workload name")
    cpu: float = Field(..., gt=0, description="Requested CPU units")
    memory_gb: float = Field(..., gt=0, description="Requested memory in GB")
    estimated_runtime_minutes: int = Field(
        ...,
        gt=0,
        description="Estimated workload runtime in minutes",
    )
    deadline_minutes: int = Field(
        ...,
        gt=0,
        description="Maximum allowed delay/deadline in minutes",
    )


class WorkloadDecision(BaseModel):
    workload: str

    decision: str

    recommended_delay_minutes: int

    predicted_energy_kwh: float

    predicted_co2e_kg: float

    carbon_intensity_g_per_kwh: float

    reason: str

    execution_status: str | None = None

    kubernetes_job: str | None = None


class FeedbackRequest(BaseModel):
    workload_name: str

    predicted_energy_kwh: float

    actual_energy_kwh: float

    predicted_co2e_kg: float

    actual_co2e_kg: float


class FeedbackResponse(BaseModel):
    workload_name: str

    predicted_energy_kwh: float

    actual_energy_kwh: float

    energy_error_percent: float

    predicted_co2e_kg: float

    actual_co2e_kg: float

    co2e_error_percent: float

    updated_energy_factor: float

    message: str


class WorkloadProfile(BaseModel):
    workload_name: str

    energy_factor: float

    status: str