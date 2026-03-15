FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
COPY apps ./apps
COPY db ./db
COPY configs ./configs
COPY artifacts ./artifacts
COPY legacy_snapshot ./legacy_snapshot
COPY docs ./docs
COPY instructs ./instructs
COPY .env.example ./

RUN mkdir -p /app/storage/uploads \
    /app/storage/runs \
    /app/storage/profiles \
    /app/storage/exports \
    /app/storage/logs

RUN pip install --upgrade pip && pip install -e .

EXPOSE 8501

CMD ["streamlit", "run", "apps/streamlit/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
