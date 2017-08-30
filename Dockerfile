FROM debian

RUN apt-get update && \
    apt-get install -y build-essential libffi-dev python python-dev python-pip libfuzzy-dev \
        debhelper tar gzip python-stdeb devscripts && \
    pip install tox && \
    rm -rf /var/cache/apt/archives/*

ADD . /opt/
WORKDIR /opt/

CMD tox
