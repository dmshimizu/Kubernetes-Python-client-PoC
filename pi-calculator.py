from kubernetes import client, config
from pprint import pprint

def main():
    config.load_kube_config(config_file="kube_config")
    container = client.V1Container(name="pi", image="perl",
        command=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"])
    template = client.V1PodTemplateSpec(spec=client.V1PodSpec(containers=[container], restart_policy="Never"))
    job = client.V1Job(api_version="batch/v1", kind="Job",
        metadata=client.V1ObjectMeta(name="pi"),
        spec=client.V1JobSpec(template=template, backoff_limit=4))
    batch_v1 = client.BatchV1Api()
    api_response = batch_v1.create_namespaced_job(body=job, namespace="default")
    pprint(api_response)

if __name__ == '__main__':
    main()
