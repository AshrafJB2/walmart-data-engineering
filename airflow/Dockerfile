
FROM apache/airflow:3.3.2

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /code

COPY --chown=airflow:root pyproject.toml .python-version uv.lock .env ./

COPY --chown=airflow:root ingestion/ ./ingestion/
COPY --chown=airflow:root walmart_dataset/ ./walmart_dataset/

USER root
RUN chown -R airflow:root /code && chmod -R u+w /code
USER airflow

RUN uv sync --locked

ENV PATH="/code/.venv/bin:$PATH"
