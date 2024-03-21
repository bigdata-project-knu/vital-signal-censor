FROM ubuntu:18.04
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
WORKDIR /main
COPY ./requirements.txt api/requirements.txt
RUN pip install -r requirements.txt
COPY . /main

CMD ['python','./main.py']