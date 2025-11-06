FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# move /src into the container
COPY /src .

# change this to python manage.py runserver when we have django installed
CMD ["sleep", "infinity"]