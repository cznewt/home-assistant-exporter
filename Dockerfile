FROM python:3.10-slim-buster


COPY requirements.txt ./tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser
COPY . .

CMD [ "python", "./home_assistant_exporter/main.py" ]
