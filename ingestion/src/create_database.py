from database import get_connection

def create_database_if_not_exists():
    """
    Create the database if it does not exist.
    """
    try:
        # Connect to the default database to create the target database
        with get_connection() as conn:  # Enable autocommit mode
            with conn.cursor() as cur:
                with open("walmart_dataset/ddl/walmart_schemas.sql", "r") as f:
                    sql_commands = f.read()
                    cur.execute(sql_commands)
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")