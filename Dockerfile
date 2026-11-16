FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

COPY README.md alembic.ini ./
COPY alembic ./alembic
COPY src ./src

RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn opsflow.main:app --host 0.0.0.0 --port 8000"]