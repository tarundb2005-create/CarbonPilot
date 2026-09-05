from kubernetes import client, config
from kubernetes.client.rest import ApiException


def load_kubernetes_config():
    """
    Load Kubernetes configuration.

    When running locally, use the user's kubeconfig.
    When running inside Kubernetes, use in-cluster configuration.
    """

    try:
        config.load_kube_config()
    except Exception:
        config.load_incluster_config()


def create_workload_job(
    workload_name: str,
    runtime_minutes: int,
) -> dict:
    """
    Create a Kubernetes Job for a CarbonPilot workload.
    """

    load_kubernetes_config()

    batch_api = client.BatchV1Api()

    safe_name = workload_name.lower().replace("_", "-")

    job_name = f"carbonpilot-{safe_name}"

    job = client.V1Job(
        metadata=client.V1ObjectMeta(
            name=job_name,
            labels={
                "app": "carbonpilot",
                "workload": safe_name,
            },
        ),
        spec=client.V1JobSpec(
            backoff_limit=1,
            ttl_seconds_after_finished=300,
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={
                        "app": "carbonpilot-workload",
                        "workload": safe_name,
                    }
                ),
                spec=client.V1PodSpec(
                    restart_policy="Never",
                    containers=[
                        client.V1Container(
                            name="workload",
                            image="busybox:1.36",
                            command=[
                                "sh",
                                "-c",
                                (
                                    f'echo "CarbonPilot executing {workload_name}"; '
                                    f'echo "Simulated runtime: {runtime_minutes} minutes"; '
                                    'echo "Workload completed successfully"'
                                ),
                            ],
                        )
                    ],
                ),
            ),
        ),
    )

    try:
        response = batch_api.create_namespaced_job(
            namespace="default",
            body=job,
        )

        return {
            "status": "SUBMITTED",
            "job_name": response.metadata.name,
            "workload": workload_name,
        }

    except ApiException as error:
        if error.status == 409:
            return {
                "status": "ALREADY_EXISTS",
                "job_name": job_name,
                "workload": workload_name,
            }

        raise