from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator

# 1. Define the DAG using the @dag decorator
@dag(
    dag_id="elt_pipeline",
    # start_date=datetime(2026, 1, 1),
    schedule="@once",
    catchup=False,
    tags=["elt", "taskflow"],
)
def my_elt_pipeline():



    run_script = BashOperator(
        task_id="run_script",
        bash_command="python /code/ingestion/src/main.py",
        cwd="/code",
    )

    ingest_neon_to_delta = DatabricksSubmitRunOperator(
        task_id="ingest_neon_to_delta",
        databricks_conn_id="databricks_default",
        pipeline_task={
            "pipeline_id": "SECRET" # Replace with pipeline ID
        },
    )

    run_dbt = BashOperator(
    task_id="run_dbt",
    bash_command="dbt build --profiles-dir /opt/airflow/project/walmart_project",
    cwd="/opt/airflow/project/walmart_project",
    )

    run_script >> ingest_neon_to_delta >> run_dbt


# Instantiate the DAG
my_elt_pipeline()
