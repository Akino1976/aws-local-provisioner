ARG ALPINE_VERSION=3.11
ARG PYTHON_VERSION=3.8.3
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} as base

WORKDIR /provisioner

COPY requirements.txt /provisioner/requirements.txt

RUN pip install --requirement requirements.txt

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

WORKDIR /provisioner

RUN mkdir -p /provisioner

COPY . /provisioner

COPY --from=base /usr/local/lib/python3.8/site-packages \
  /usr/local/lib/python3.8/site-packages

RUN mkdir -p /root/.aws; \
  cp /provisioner/assets/awsmock-credentials /root/.aws/credentials

ENTRYPOINT [ "python" ]

CMD [ "provisioner.py" ]

ENV AWS_SHARED_CREDENTIALS_FILE=/provisioner/awsmock-credentials
