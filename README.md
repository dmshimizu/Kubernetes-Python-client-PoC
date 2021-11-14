## About the project

This project was created as a proof of concept for a specific Kubernetes Python client use case.
The project is suitable for educational purposes but can also be used as starting point for other projects based on similar concepts.

The project steps are:
1. create a Python script capable of creating a Kubernetes job, using the Kubernetes Python client;
2. create a Docker image containing the Python script created in step #1, and capable of running it;
3. create a Kubernetes job which creates a pod that runs the image created in step #2 and triggers the Python script execution;
4. observe the job created by the Python script executed in step #3.

## This project uses

* [Python](https://www.python.org/)
* [Dockerfile](https://docs.docker.com/engine/reference/builder/)
* [Docker local registry](https://docs.docker.com/registry/deploying/)
* [Kubernetes](https://kubernetes.io)
* [Kubernetes Python client](https://github.com/kubernetes-client/python/)

## Requirements

This project requires Docker and Kubernetes cluster available in your environment.
A possible approach to fulfill this requirement is installing [Docker Desktop](https://www.docker.com/get-started)

## Getting started

1. Copy your kubernetes config file to project root directory (the command below assumes it is located in ~/.kube/config, default for Docker Desktop):

```bash
$ cp ~/.kube/config ./kube_config
```
> :warning: Avoid committing your kube_config file. That file contains configuration specific to your local k8s cluster and may be useless for others.

2. Build the k8s-job-creator Docker image, tagging it to localhost:5000 repository:
```bash
$ docker build -t localhost:5000/k8s-job-creator:1.0 .
```

3. Start Docker local registry (in case you don't have one already started):
```bash
$ docker run -d -p 5000:5000 --restart always --name registry registry:2
```

4. Push k8s-job-creator Docker image to local registry:
```bash
$ docker push localhost:5000/k8s-job-creator:1.0
```

5. Create Kubernetes job:
```bash
$ kubectl apply -f k8s-job-creator.yaml
```

After completing the steps successfully, you may see two jobs created, similar to below:
```bash
$ kubectl get jobs
NAME              COMPLETIONS   DURATION   AGE
k8s-job-creator   1/1           6s         92s
pi-job            1/1           18s        88s
```

The `k8s-job-creator` job was manually created by `kubectl apply -f k8s-job-creator.yaml` command.
The `pi-job` job was created by the Python script executed in the pod corresponding to `k8s-job-creator` job.
The `pi-job` creates a pod that calculates pi.
Final results can be verified similarly to below:

```bash
$ kubectl get pods
NAME                    READY   STATUS      RESTARTS   AGE
k8s-job-creator-jmgr7   0/1     Completed   0          6m14s
pi-job-cprs6            0/1     Completed   0          6m10s

$ kubectl logs pi-job-cprs6
3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989380952572010654858632788659361533818279682303019520353018529689957736225994138912497217752834791315155748572424541506959508295331168617278558890750983817546374649393192550604009277016711390098488240128583616035637076601047101819429555961989467678374494482553797747268471040475346462080466842590694912933136770289891521047521620569660240580381501935112533824300355876402474964732639141992726042699227967823547816360093417216412199245863150302861829745557067498385054945885869269956909272107975093029553211653449872027559602364806654991198818347977535663698074265425278625518184175746728909777727938000816470600161452491921732172147723501414419735685481613611573525521334757418494684385233239073941433345477624168625189835694855620992192221842725502542568876717904946016534668049886272327917860857843838279679766814541009538837863609506800642251252051173929848960841284886269456042419652850222106611863067442786220391949450471237137869609563643719172874677646575739624138908658326459958133904780275901
```
