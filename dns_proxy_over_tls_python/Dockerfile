FROM python:alpine3.7

ENV PROXY_PORT 53
ENV CA_CERT_PATH "/etc/ssl/cert.pem"

RUN apk update \
  && apk upgrade \
  && rm -rf /var/cache/apk/*
COPY . /app
WORKDIR /app
CMD [ "sh", "-c", "python dns_proxy_over_tls.py --port $PROXY_PORT --ca_path $CA_CERT_PATH" ]
