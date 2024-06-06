FROM nvidia/cuda:11.4.3-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \   
        python3-opencv \
        libglib2.0-0

COPY requirements.txt requirements.txt

RUN python3 -m pip install requirements.txt

WORKDIR .

COPY . .

ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app:app", "-n"]