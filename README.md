# Walmart Data Engineering Project

An end-to-end data engineering project based on a Walmart retail dataset.

The goal of this project is to build a complete data pipeline while practicing modern data engineering tools and concepts, from raw data ingestion and storage to transformation and orchestration.

## Project Status

🚧 **In progress**

Currently, the project is at the **source database / ingestion stage**:

* PostgreSQL running in Docker
* Database schema created
* Walmart CSV datasets loaded into PostgreSQL
* Docker volumes used for persistent database storage

Planned stages will add PySpark, dbt, Airflow, and a local S3-compatible data lake.

---

## Architecture

### Current

```text
CSV Files
    │
    ▼
Docker
    │
    ▼
PostgreSQL
    │
    ├── customers
    ├── stores
    ├── products
    ├── employees
    ├── orders
    └── order_items
```

### Planned

```text
                    ┌──────────────┐
                    │  CSV / Data  │
                    │    Source    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Python    │
                    │  Ingestion   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    MinIO     │
                    │  Data Lake   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   PySpark    │
                    │ Transformation│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ PostgreSQL / │
                    │   Warehouse  │
                    └──────┬───────┘
                           │
                           ▼
                       ┌───────┐
                       │  dbt  │
                       └───┬───┘
                           │
                           ▼
                    Analytics Layer

                    ↑
                    │
                 Airflow
              Orchestration
```

---

## Technologies

### Currently used

* **PostgreSQL** — relational database
* **Docker** — containerization
* **Docker Compose** — local infrastructure management
* **SQL** — database creation and data loading
* **CSV** — initial source data

### Planned

* **Python** — data ingestion
* **PySpark** — distributed data processing and transformation
* **MinIO** — local S3-compatible object storage / data lake
* **dbt** — analytics transformations and data modeling
* **Apache Airflow** — workflow orchestration
* **Git / GitHub** — version control and project documentation

---

## Dataset

The project uses a simulated Walmart retail dataset containing several related entities:

### Customers

Contains customer information.

| Column              | Description                |
| ------------------- | -------------------------- |
| `customer_id`       | Unique customer identifier |
| `first_name`        | Customer first name        |
| `last_name`         | Customer last name         |
| `email`             | Customer email             |
| `phone`             | Customer phone number      |
| `city`              | Customer city              |
| `province`          | Customer province/state    |
| `country`           | Customer country           |
| `created_timestamp` | Record creation timestamp  |
| `updated_timestamp` | Last update timestamp      |
| `is_active`         | Active record indicator    |

### Stores

Contains Walmart store information.

### Products

Contains product information.

### Employees

Contains employee information.

### Orders

Contains customer orders.

### Order Items

Contains individual products associated with each order.

---

## Database Schema

The PostgreSQL database currently contains six tables:

```text
customers
    │
    │
orders ──────────── order_items
    │                    │
    │                    │
stores              products
    │
employees
```

The main relationships are:

```text
customers.customer_id
        ↓
orders.customer_id

stores.store_id
        ↓
orders.store_id

stores.store_id
        ↓
employees.store_id

orders.order_id
        ↓
order_items.order_id

products.product_id
        ↓
order_items.product_id
```

---

## Project Structure

```text
walmart-data-engineering/
│
├── walmart-dataset/
|   └──data/
│       ├── customers.csv
│       ├── stores.csv
│       ├── products.csv
│       ├── employees.csv
│       ├── orders.csv
│       └── order_items.csv
│
├── ddl/
│   └── walmart_schemas.sql
│
├── docker-compose.yml
│
├── .env
│
└── README.md
```

As the project develops, additional directories will be added for Python ingestion, PySpark jobs, dbt models, and Airflow DAGs.

---

# PostgreSQL with Docker

PostgreSQL runs inside a Docker container rather than being installed directly on the host machine.

### Start PostgreSQL

```bash
docker compose up -d
```

### Check the container

```bash
docker compose ps
```

### View PostgreSQL logs

```bash
docker compose logs postgres
```

### Connect to PostgreSQL

```bash
docker exec -it walmart-postgres psql -U postgres -d walmart
```

### Stop the container

```bash
docker compose down
```

The PostgreSQL data is stored in a Docker volume so that removing the container does not remove the database.

---

## Environment Variables

Database credentials are stored in `.env`:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=walmart
```

The `.env` file should **not be committed to GitHub**.

Add it to `.gitignore`:

```gitignore
.env
```

For a production project, credentials should be managed using a proper secrets-management solution.

---

# Loading CSV Data

The CSV files are mounted into the PostgreSQL container through Docker Compose.

For example:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
  - ./data:/data
```

This makes the local `data/` directory available inside the container as `/data`.

Data can then be loaded using PostgreSQL's `\copy` command:

```sql
\copy customers FROM '/data/data/customers.csv' WITH (FORMAT csv, HEADER true);
```

The same approach is used for the other tables:

```sql
\copy stores FROM '/data/data/stores.csv' WITH (FORMAT csv, HEADER true);

\copy products FROM '/data/data/products.csv' WITH (FORMAT csv, HEADER true);

\copy employees FROM '/data/data/employees.csv' WITH (FORMAT csv, HEADER true);

\copy orders FROM '/data/data/orders.csv' WITH (FORMAT csv, HEADER true);

\copy order_items FROM '/data/data/order_items.csv' WITH (FORMAT csv, HEADER true);
```

---

# Development Roadmap

The project will be developed incrementally.

### Phase 1 — Source Database

* [x] Create PostgreSQL container
* [x] Configure PostgreSQL with Docker Compose
* [x] Create database
* [x] Create source tables
* [x] Mount CSV data into the container
* [x] Load CSV data into PostgreSQL

### Phase 2 — Python Ingestion

* [ ] Build Python ingestion script
* [ ] Read source data
* [ ] Validate incoming data
* [ ] Load data programmatically
* [ ] Handle errors
* [ ] Add logging

### Phase 3 — Data Lake

* [ ] Introduce MinIO
* [ ] Create raw data layer
* [ ] Store raw files in object storage
* [ ] Organize data using a suitable folder/partition structure

### Phase 4 — PySpark

* [ ] Introduce PySpark
* [ ] Read raw data
* [ ] Clean and transform data
* [ ] Handle data types
* [ ] Perform joins and aggregations
* [ ] Write processed data

### Phase 5 — Data Warehouse

* [ ] Design analytical data model
* [ ] Create fact and dimension tables
* [ ] Load transformed data into the warehouse
* [ ] Optimize queries

### Phase 6 — dbt

* [ ] Initialize dbt project
* [ ] Create staging models
* [ ] Create intermediate models
* [ ] Create analytical models
* [ ] Add tests
* [ ] Add documentation
* [ ] Implement incremental models where appropriate

### Phase 7 — Airflow

* [ ] Containerize Airflow
* [ ] Create DAGs
* [ ] Automate ingestion
* [ ] Automate Spark transformations
* [ ] Automate dbt transformations
* [ ] Add task dependencies
* [ ] Implement retries and failure handling

### Phase 8 — Final Pipeline

The final pipeline should be reproducible using Docker:

```text
Source
  ↓
Python
  ↓
Data Lake
  ↓
PySpark
  ↓
Warehouse
  ↓
dbt
  ↓
Analytics
```

with Airflow orchestrating the workflow.

---

# Learning Objectives

This project is intended to provide practical experience with:

* Relational databases
* SQL
* PostgreSQL
* Docker and Docker Compose
* Data ingestion
* ETL/ELT pipelines
* Data lakes
* Object storage
* PySpark
* Data transformation
* Data warehouses
* Dimensional modeling
* dbt
* Workflow orchestration
* Airflow
* Data quality
* Incremental processing
* Pipeline automation
* Git and GitHub

---

# Future Improvements

Potential improvements include:

* Incremental data ingestion
* Slowly Changing Dimensions (SCD Type 2)
* Data quality checks
* Schema validation
* Pipeline monitoring
* Logging
* Error handling
* Partitioning
* Query optimization
* Automated testing
* Backfilling historical data
* CI/CD
* Cloud deployment

---

## Goal

The goal is not simply to reproduce an existing tutorial.

This project is being adapted into an independent data engineering portfolio project, with an emphasis on understanding each component of the pipeline and being able to explain the architecture, design decisions, and implementation.

The final objective is a reproducible, Dockerized end-to-end data pipeline that demonstrates practical data engineering skills.