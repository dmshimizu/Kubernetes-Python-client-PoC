FROM python:3.8
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos "" worker
COPY --chown=worker:worker kube_config .
COPY --chown=worker:worker k8s-job-creator.py .
