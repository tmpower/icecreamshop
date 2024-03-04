# BASE
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    gcc \
    postgresql-client \
    python3-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .


# PRODUCTION
FROM base AS production

RUN pip install --no-cache-dir -r requirements.txt
COPY . .


# TESTING
FROM base AS testing

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
COPY . .
CMD ["pytest", "-W", "ignore", "-v", "tests"]
