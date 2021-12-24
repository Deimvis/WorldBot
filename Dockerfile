FROM python:3.7

WORKDIR /bot/world_bot
COPY apps/ apps/
COPY config.py .
COPY main.py .

COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
