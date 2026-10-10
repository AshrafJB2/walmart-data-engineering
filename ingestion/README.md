# Walmart CSV Ingestion

This script cleans the raw Walmart dataset CSV files and loads them into a
PostgreSQL database. It is part of the repository's data pipeline and uses the
project dependencies defined in the repository-root `pyproject.toml`.

## What it does

When run, `src/main.py`:

1. Reads CSV files from `walmart_dataset/data/raw/`.
2. Trims whitespace, normalizes known numeric, timestamp, and boolean columns,
   removes duplicate rows, and writes cleaned CSVs to
   `walmart_dataset/data/cleaned/`.
3. Loads the cleaned data into PostgreSQL in dependency order:
   customers, stores, products, employees, orders, and order items.

The input files are expected to be named `customers.csv`, `stores.csv`,
`products.csv`, `employees.csv`, `orders.csv`, and `order_items.csv`, with
columns in the order expected by the matching table definitions.

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/) for installing and running the project
- Docker Compose and PostgreSQL 17 (or a compatible PostgreSQL instance)

## Setup

Run these commands from the **repository root**, not from the `ingestion`
directory. The script uses paths relative to the repository root.

1. Create a root-level `.env` file for Docker Compose:

   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=choose-a-local-password
   POSTGRES_DB=walmart
   ```

   Keep `.env` private; do not commit real credentials.

2. Install the Python dependencies:

   ```powershell
   uv sync
   ```

3. Start PostgreSQL:

   ```powershell
   docker compose up -d postgres
   ```

4. Create the tables in a new, empty database:
   Use the schema in `walmart_dataset/ddl`

## Run

From the repository root:

```powershell
uv run --env-file .env python ingestion/src/main.py
```

The database connection reads these environment variables:

| Variable | Purpose |
| --- | --- |
| `POSTGRES_HOST` | PostgreSQL host; defaults to `localhost` |
| `POSTGRES_PORT` | PostgreSQL port; defaults to `5432` |
| `POSTGRES_DB` | Database name; defaults to `walmart` |
| `POSTGRES_USER` | Database user; defaults to `postgres` |
| `POSTGRES_PASSWORD` | Database password |

The script prints progress for the cleaning step and each table load. If
loading fails, it prints an error; check that PostgreSQL is running, the
connection settings are correct, the schema exists, and referenced parent
rows are present.

## Important behavior

- Loading uses `INSERT` statements; it does not truncate tables, upsert rows,
  or make repeated runs idempotent. Running it again against already-loaded
  data can fail on duplicate primary keys.
- Cleaned CSVs are overwritten when the script runs.
- The loader expects the CSV columns and their order to match the `INSERT`
  statements in `src/loaders.py` and the schema in
  `walmart_dataset/ddl/walmart_schemas.sql`.