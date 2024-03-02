# BASE
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt .


# PRODUCTION
FROM base AS production

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]


# TESTING
FROM base AS testing

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
COPY . .
CMD ["pytest", "-W", "ignore", "-v", "tests"]
