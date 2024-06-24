FROM python:3.12.4-slim-bullseye

WORKDIR /code

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ARG POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | \
            POETRY_VERSION=${POETRY_VERSION} \
            POETRY_HOME=/opt/poetry \
            python3 - && cd /usr/local/bin && ln -s /opt/poetry/bin/poetry && \
            poetry config virtualenvs.create false


COPY local.env /code/
COPY pyproject.toml poetry.lock* /code/
COPY /app /code/app

RUN poetry install --no-dev

ENTRYPOINT ["poetry", "run", "python", "-m", "app.main"]