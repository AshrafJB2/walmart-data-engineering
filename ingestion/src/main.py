from loaders import load_customer_data, load_employees_data, load_products_data, load_stores_data, load_orders_data, load_order_items_data
import pandas as pd
from data_cleaner import clean_csv_directory
from pathlib import Path
from create_database import create_database_if_not_exists

def main():
    # Create the database if it does not exist
    create_database_if_not_exists()

    print("Starting data cleaning and loading process...")
    for output_path in clean_csv_directory(Path("walmart_dataset/data/raw"), Path("walmart_dataset/data/cleaned")):
        print(f"Cleaned: {output_path}")

    # Load cleaned data into the database
    try:
        load_customer_data(pd.read_csv("walmart_dataset/data/cleaned/customers.csv"))
        print("Customer data loaded successfully.")
        load_stores_data(pd.read_csv("walmart_dataset/data/cleaned/stores.csv"))
        print("Store data loaded successfully.")
        load_products_data(pd.read_csv("walmart_dataset/data/cleaned/products.csv"))
        print("Product data loaded successfully.")
        load_employees_data(pd.read_csv("walmart_dataset/data/cleaned/employees.csv"))
        print("Employee data loaded successfully.")
        load_orders_data(pd.read_csv("walmart_dataset/data/cleaned/orders.csv"))
        print("Order data loaded successfully.")
        load_order_items_data(pd.read_csv("walmart_dataset/data/cleaned/order_items.csv"))
        print("Order item data loaded successfully.")
    except Exception as e:
        print(f"An error occurred during data loading: {e}")

    



if __name__ == "__main__":
    main()