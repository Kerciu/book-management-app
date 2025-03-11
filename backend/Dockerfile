FROM python:3.11-slim

ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=core.settings



RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8000
