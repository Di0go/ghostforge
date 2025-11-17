FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# deps
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# EN: This command uses netcat to wait for the db to respond and then migrates and starts.
# NOTE: netcat -z shutdowns the session when the connection is established
CMD sh -c "while ! nc -z ghostforge-db 5432; do sleep 0.1; done && \
           python manage.py migrate && \
           python manage.py runserver 0.0.0.0:8000"