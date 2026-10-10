from database import get_connection
import pandas

def load_customer_data(data: pandas.DataFrame):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO customers (customer_id, first_name, last_name, email, phone, city, province, country, created_timestamp, updated_timestamp, is_active)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, data.itertuples(index=False, name=None))
        conn.commit()


def load_employees_data(data: pandas.DataFrame):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO employees (employee_id, store_id, first_name, last_name, email, job_title, salary, created_timestamp, updated_timestamp, is_active)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, data.itertuples(index=False, name=None))
        conn.commit()

def load_products_data(data: pandas.DataFrame):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO products (product_id, product_name, category, brand, price, created_timestamp, updated_timestamp, is_active)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, data.itertuples(index=False, name=None))
        conn.commit()

def load_stores_data(data: pandas.DataFrame):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO stores (store_id, store_name, city, province, country, created_timestamp, updated_timestamp, is_active)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, data.itertuples(index=False, name=None))
        conn.commit()

def load_orders_data(data: pandas.DataFrame):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO orders (order_id, customer_id, store_id, order_timestamp, payment_method, order_status, total_amount, created_timestamp, updated_timestamp, is_active)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, data.itertuples(index=False, name=None))
        conn.commit()

def load_order_items_data(data: pandas.DataFrame):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price, line_amount, created_timestamp, updated_timestamp, is_active)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, data.itertuples(index=False, name=None))
        conn.commit()