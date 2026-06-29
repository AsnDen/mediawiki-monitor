FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock* .

RUN uv sync --no-install-project --no-dev

COPY . .

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "mediawiki_monitor.__main__:create_app()"]
