import subprocess
import time
from dataclasses import dataclass


@dataclass
class ExecutionResult:
    workload_name: str
    status: str
    execution_time_seconds: float
    message: str


def execute_workload(
    workload_name: str,
    command: str,
) -> ExecutionResult:

    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
        )

        execution_time = round(
            time.time() - start_time,
            2,
        )

        if result.returncode == 0:
            return ExecutionResult(
                workload_name=workload_name,
                status="COMPLETED",
                execution_time_seconds=execution_time,
                message=result.stdout.strip()
                or "Workload executed successfully.",
            )

        return ExecutionResult(
            workload_name=workload_name,
            status="FAILED",
            execution_time_seconds=execution_time,
            message=result.stderr.strip()
            or "Workload execution failed.",
        )

    except subprocess.TimeoutExpired:

        execution_time = round(
            time.time() - start_time,
            2,
        )

        return ExecutionResult(
            workload_name=workload_name,
            status="TIMEOUT",
            execution_time_seconds=execution_time,
            message="Workload exceeded the execution timeout.",
        )

    except Exception as exc:

        execution_time = round(
            time.time() - start_time,
            2,
        )

        return ExecutionResult(
            workload_name=workload_name,
            status="ERROR",
            execution_time_seconds=execution_time,
            message=str(exc),
        )