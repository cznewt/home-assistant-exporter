FROM python:3.11-alpine

ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Build deps for the native extensions of aiohttp[speedups] / ujson. libstdc++
# is kept for runtime; the toolchain is dropped again after the install.
RUN apk add --no-cache libstdc++ \
    && apk add --no-cache --virtual .build-deps gcc g++ musl-dev python3-dev

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN pip3 install --no-cache-dir --no-deps . \
    && apk del .build-deps

EXPOSE 9878

# Plain Docker / Kubernetes image. Configure via HASS_URL / HASS_TOKEN env vars
# or CLI flags (see README). The Home Assistant OS add-on wraps this app in a
# separate repository with its own bashio entrypoint.
ENTRYPOINT ["home-assistant-exporter"]
