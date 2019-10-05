FROM python:3.7-alpine3.10 AS base

WORKDIR /provisioner

COPY requirements.txt /provisioner/requirements.txt

RUN pip install --requirement requirements.txt

FROM python:3.7-alpine3.10

WORKDIR /provisioner

RUN mkdir -p /provisioner

COPY . /provisioner

COPY --from=base /usr/local/lib/python3.7/site-packages \
  /usr/local/lib/python3.7/site-packages

RUN mkdir -p /root/.aws; \
  cp /provisioner/assets/awsmock-credentials /root/.aws/credentials

ENTRYPOINT [ "python" ]

CMD [ "provisioner.py" ]

ENV AWS_SHARED_CREDENTIALS_FILE=/provisioner/awsmock-credentials
