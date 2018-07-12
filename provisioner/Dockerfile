FROM python:3.6-alpine3.7 AS base

WORKDIR /provisioner

COPY requirements.txt /provisioner/requirements.txt

RUN pip install --requirement requirements.txt

FROM python:3.6-alpine3.7

WORKDIR /provisioner

RUN mkdir -p /provisioner

COPY . /provisioner

COPY --from=base /usr/local/lib/python3.6/site-packages \
  /usr/local/lib/python3.6/site-packages

RUN mkdir -p /root/.aws; \
  cp /provisioner/assets/awsmock-credentials /root/.aws/credentials

ENTRYPOINT [ "python" ]

CMD [ "provisioner.py" ]
