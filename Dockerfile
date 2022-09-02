ARG BUILD_FROM
FROM $BUILD_FROM

# FROM python:3.10-slim-buster
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN apk update \
  # Python
  && apk add --update --no-cache python3 g++ && ln -sf python3 /usr/bin/python \
  && python3 -m ensurepip \
  && pip3 install --no-cache --upgrade pip setuptools \
  && apk add --virtual build-deps gcc python3-dev

COPY requirements.txt ./tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN mkdir /exporter

WORKDIR /exporter
COPY . .

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]