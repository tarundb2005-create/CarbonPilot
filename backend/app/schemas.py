from pydantic import BaseModel, Field


class WorkloadRequest(BaseModel):
    name: str
    workload_type: str
    cpu: float = Field(gt=0)
    memory_gb: float = Field(gt=0)
    estimated_runtime_minutes: int = Field(gt=0)
    deadline_minutes: int = Field(gt=0)
    priority: int = Field(default=5, ge=1, le=10)


class WorkloadDecision(BaseModel):
    workload: str
    decision: str
    recommended_delay_minutes: int
    predicted_energy_kwh: float
    predicted_co2e_kg: float
    carbon_intensity_g_per_kwh: float
    reason: str


class FeedbackRequest(BaseModel):
    workload_name: str

    predicted_energy_kwh: float = Field(gt=0)
    actual_energy_kwh: float = Field(gt=0)

    predicted_co2e_kg: float = Field(gt=0)
    actual_co2e_kg: float = Field(gt=0)


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