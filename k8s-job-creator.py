from kubernetes import client, config
from pprint import pprint

if __name__ == '__main__':
    # Load k8s config file, containing target cluster configuration
    config.load_kube_config(config_file="kube_config")

    # Define the pi-container container spec. This container will calculate pi
    container = client.V1Container(name="pi-container", image="perl",
        command=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"])

    # Define pod spec to run pi container
    template = client.V1PodTemplateSpec(spec=client.V1PodSpec(containers=[container], restart_policy="Never"))

    # Define pi-job job spec. This job will create a pod to calculate pi
    job = client.V1Job(api_version="batch/v1", kind="Job",
        metadata=client.V1ObjectMeta(name="pi-job"),
        spec=client.V1JobSpec(template=template, backoff_limit=4))
    
    batch_v1 = client.BatchV1Api()

    # K8s API call that creates the pi-job, as specified in this program
    api_response = batch_v1.create_namespaced_job(body=job, namespace="default")

    # Print K8s API response, for debugging purposes
    pprint(api_response)

