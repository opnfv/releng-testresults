#######################################################
#   Docker container for OPNFV-TESTAPI
#######################################################
# Purpose: run opnfv-testapi for gathering test results
#
# Maintained by SerenaFeng
# Build:
#    $ docker build -t opnfv/testapi:tag .
#
# Execution:
#    $ docker run -dti -p 8001:8000 \
#      -e "base_url=http://10.63.243.17:8001" \
#      -e "mongodb_url=mongodb://10.63.243.17:27017/" \
#      opnfv/testapi:tag
#
# NOTE: providing swagger_url, mongodb_url is optional.
#       If not provided, it will use the default one
#       configured in config.ini
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

FROM python:3.9.2-alpine3.13
MAINTAINER="Morgan Richomme <morgan.richomme@orange.com>"
LABEL version="v1.1" description="OPNFV TestAPI Docker container"

ENV HOME /home

# Packaged dependencies
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

COPY requirements.txt requirements.txt
RUN apk --no-cache add --update openssl bash && \
    apk --no-cache add --virtual .build-deps --update \
    gcc musl-dev linux-headers libressl-dev libffi-dev git

RUN pip install --upgrade requests

RUN git clone https://gerrit.opnfv.org/gerrit/releng-testresults /home/releng-testresults

RUN pwd
RUN ls -lah

WORKDIR /releng-testresults/testapi
RUN pip install -r requirements.txt

RUN python setup.py install
CMD ["bash", "docker/start-server.sh"]

