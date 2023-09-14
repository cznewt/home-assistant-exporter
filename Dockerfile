FROM python:3.11-alpine

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --update --no-cache python3 g++ && ln -sf python3 /usr/bin/python \
    && python3 -m ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools \
    && apk add --virtual build-deps gcc git python3-dev

COPY requirements.txt ./tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt \
    && mkdir /app

WORKDIR /app
COPY . .

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]