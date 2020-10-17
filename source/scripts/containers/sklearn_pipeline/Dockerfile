FROM ubuntu:latest
MAINTAINER Ben Weber

ARG PROJECT_ID

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    python3-pip\
    python3-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
  pandas \
  scikit-learn \
  pandas_gbq

COPY pipeline.py pipeline.py
COPY dsdemo.json dsdemo.json

ENV GOOGLE_PROJECT_ID=$PROJECT_ID
ENV GOOGLE_APPLICATION_CREDENTIALS=/dsdemo.json

ENTRYPOINT ["python3","pipeline.py"]
