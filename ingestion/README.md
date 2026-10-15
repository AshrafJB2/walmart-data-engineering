# Python ingestion

The Python ingestion task cleans the six Walmart CSV source files and loads
their records into the configured PostgreSQL-compatible database. In the
current project setup, Airflow runs it inside the repository's Airflow
container.

## What it does

`src/main.py` runs from the repository root (`/code` in the Airflow image) and:

1. Executes `walmart_dataset/ddl/walmart_schemas.sql` against the configured
   database. The SQL creates the six tables if they do not already exist; the
   target database itself must already exist.
2. Reads CSV files from `walmart_dataset/data/raw/`.
3. Trims text, converts recognized ID/quantity columns to integers, monetary
   columns to decimals, timestamp fields to timestamps, and `is_active` values
   to booleans. Empty text becomes null and exact duplicate rows are removed.
4. Writes cleaned copies to `/opt/airflow/data/cleaned/`.
5. Loads records in dependency order: customers, stores, products, employees,
   orders, then order items.

The expected source filenames are `customers.csv`, `stores.csv`,
`products.csv`, `employees.csv`, `orders.csv`, and `order_items.csv`. Their
column names and ordering must match the `INSERT` statements in
[`src/loaders.py`](src/loaders.py) and the schema in
[`../walmart_dataset/ddl/walmart_schemas.sql`](../walmart_dataset/ddl/walmart_schemas.sql).

## Configuration

The connection is made with `psycopg` using the following environment
variables. They are loaded from the root `.env` by the ingestion code:

| Variable | Purpose |
| --- | --- |
| `POSTGRES_HOST` | Database hostname |
| `POSTGRES_PORT` | Database port |
| `POSTGRES_DB` | Existing database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |

For example, create a private root-level `.env`:

```env
POSTGRES_HOST=your-database-host
POSTGRES_PORT=5432
POSTGRES_DB=your-database
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
```

The Airflow Dockerfile copies the root `.env` into the image at build time.
Keep credentials local and do not publish an image built from a real-secret
`.env`.

## Running it

The current code writes cleaned data to `/opt/airflow/data/cleaned`, so use the
Airflow task/container layout rather than running the script directly on a
host without adapting that path. Start the services as described in
[`../airflow/README.md`](../airflow/README.md), then run the `elt_pipeline`
DAG. The Python task is named `run_script`.

## Important behavior

- The loaders issue plain `INSERT` statements. They do not truncate, upsert, or
  deduplicate against records already in the destination tables. A subsequent
  run against the same populated tables can hit primary-key conflicts.
- Cleaned CSVs are overwritten each time the cleaner runs.
- Cleaning errors such as a missing input directory or missing CSV files are
  raised. The main script prints and catches database/table-loading errors;
  inspect the `run_script` task log to confirm that all six table loads
  succeeded.
