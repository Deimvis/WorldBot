FROM python:3.11.2

WORKDIR /bot

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src     /bot/src
COPY files   /bot/files
COPY lib     /bot/lib
COPY scripts /bot/scripts
COPY main.py /bot/main.py

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./scripts/run"]
