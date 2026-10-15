# Walmart dbt project

This dbt project transforms the Walmart bronze source tables in Databricks into
staging, intermediate, and analytics mart models. The Airflow DAG runs
`dbt build` as its final task.

## Project configuration

- Project name and profile: `walmart_project`
- Profile type: Databricks
- Target: `dev`
- Source catalog/schema: `walmart.bronze`
- Configured output schema base: `dbt_schema`

The checked-in `profiles.yml` currently uses `VAR` placeholders for `host`,
`http_path`, and `token`. Replace those placeholders with valid Databricks
credentials before running the project. Prefer dbt `env_var()` references in
the profile and set the corresponding environment variables in the execution
environment rather than committing a token. For example:

```yaml
host: "{{ env_var('DATABRICKS_HOST') }}"
http_path: "{{ env_var('DATABRICKS_HTTP_PATH') }}"
token: "{{ env_var('DATABRICKS_TOKEN') }}"
```

## Model layers

| Layer | Models | Purpose |
| --- | --- | --- |
| Staging | `stg_walmart__customers`, `stg_walmart__orders`, `stg_walmart__order_items`, `stg_walmart__products`, `stg_walmart__stores` | Source-aligned models configured as incremental |
| Intermediate | `int_order_items_enriched`, `int_orders_with_totals` | Enrich order items with order/product attributes and compare source order totals with item-derived totals |
| Marts | `dim_customers`, `dim_products`, `dim_stores`, `fct_orders`, `fct_sales` | Analytics dimensions and facts |

Intermediate and mart models are configured as tables. dbt's default schema
generation combines the profile schema and custom model schema, resulting in
schemas such as `dbt_schema_staging`, `dbt_schema_intermediate`, and
`dbt_schema_marts`.

The project declares six bronze sources: customers, employees, orders,
order_items, products, and stores. There is currently no employees staging
model. Model properties define key uniqueness/not-null tests and selected
mart foreign-key relationship tests.

## Run dbt

From the repository root, after installing dependencies with `uv sync` and
configuring a working Databricks profile:

```powershell
uv run dbt debug --project-dir walmart_project --profiles-dir walmart_project
uv run dbt build --project-dir walmart_project --profiles-dir walmart_project
```

`dbt build` runs the selected models and their configured tests. Airflow runs
the equivalent command from the project directory with this profile path:

```text
dbt build --profiles-dir /opt/airflow/project/walmart_project
```

An incremental refresh can be forced with `--full-refresh` when appropriate:

```powershell
uv run dbt build --full-refresh --project-dir walmart_project --profiles-dir walmart_project
```

## Captured results

The Databricks catalog screenshot shows the bronze and dbt output schemas:

![Databricks catalog with bronze, dbt staging, intermediate, and marts schemas](../images/delta_database_schemas.png)

The Databricks ingestion pipeline's completed run is shown in
[`../images/databricks_ingest_pipeline.png`](../images/databricks_ingest_pipeline.png).
Saved schema/model result exports are in [`../data_modelisation`](../data_modelisation).
